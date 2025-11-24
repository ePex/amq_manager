from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button, OptionList
from textual.widgets.option_list import Option
from textual.containers import Grid, Vertical
from amq_manager.client import ActiveMQClient

class BatchMoveModal(ModalScreen):
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "move", "Move"),
    ]
    CSS = """
    BatchMoveModal {
        align: center middle;
    }
    Vertical {
        padding: 2;
        width: 60%;
        min-width: 80;
        max-width: 120;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }
    Label {
        text-align: center;
        margin-bottom: 1;
    }
    Input {
        margin-bottom: 1;
    }
    OptionList {
        max-height: 10;
        margin-bottom: 1;
    }
    Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto;
    }
    """

    def __init__(self, message_ids: list, source_queue: str):
        super().__init__()
        self.message_ids = message_ids
        self.source_queue = source_queue
        self.all_queues = []

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Move {len(self.message_ids)} messages"),
            Label(f"from {self.source_queue}"),
            Input(placeholder="Target Queue Name", id="target_queue"),
            OptionList(id="queue_suggestions"),
            Grid(
                Button("Cancel", variant="error", id="cancel"),
                Button("Move", variant="primary", id="move"),
            ),
        )

    def on_mount(self) -> None:
        self.load_queues()

    def load_queues(self) -> None:
        app = self.app
        if not hasattr(app, "active_config") or not app.active_config:
            return

        client = ActiveMQClient(
            app.active_config.host,
            app.active_config.port,
            app.active_config.user,
            app.active_config.password,
            app.active_config.ssl,
            app.active_config.context_path
        )
        try:
            queues = client.list_queues()
            # Exclude the source queue from suggestions
            self.all_queues = [q.get("Name", "") for q in queues if q.get("Name") and q.get("Name") != self.source_queue]
            self.update_suggestions("")
        except Exception:
            pass

    def update_suggestions(self, filter_text: str) -> None:
        option_list = self.query_one("#queue_suggestions", OptionList)
        option_list.clear_options()
        
        filter_text = filter_text.lower()
        matching_queues = [q for q in self.all_queues if filter_text in q.lower()]
        
        for queue in matching_queues[:10]:  # Limit to 10 suggestions
            option_list.add_option(Option(queue, id=queue))

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "target_queue":
            self.update_suggestions(event.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Pressing Enter in the input field triggers move
        if event.input.id == "target_queue":
            self.action_move()

    def on_key(self, event) -> None:
        # Allow arrow keys to navigate to the suggestion list
        if event.key in ("down", "up") and self.query_one("#target_queue").has_focus:
            option_list = self.query_one("#queue_suggestions", OptionList)
            if option_list.option_count > 0:
                option_list.focus()
                event.prevent_default()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # Set the selected queue name in the input and refocus it
        inp = self.query_one("#target_queue", Input)
        inp.value = event.option.prompt
        inp.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.action_cancel()
        elif event.button.id == "move":
            self.action_move()

    def action_cancel(self) -> None:
        self.dismiss(False)

    def action_move(self) -> None:
        target_queue = self.query_one("#target_queue", Input).value
        if not target_queue:
            return
        
        if target_queue == self.source_queue:
            self.notify("Cannot move messages to the same queue", severity="warning")
            return
        
        self.move_messages(target_queue)

    def move_messages(self, target_queue: str) -> None:
        app = self.app
        if not hasattr(app, "active_config") or not app.active_config:
            return

        client = ActiveMQClient(
            app.active_config.host,
            app.active_config.port,
            app.active_config.user,
            app.active_config.password,
            app.active_config.ssl,
            app.active_config.context_path
        )
        
        success_count = 0
        for msg_id in self.message_ids:
            if client.move_message(msg_id, self.source_queue, target_queue):
                success_count += 1
        
        self.dismiss(success_count)
