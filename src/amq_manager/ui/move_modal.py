from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button, OptionList
from textual.widgets.option_list import Option
from textual.containers import Grid, Vertical
from amq_manager.client import ActiveMQClient

class MoveMessageModal(ModalScreen):
    CSS = """
    MoveMessageModal {
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

    def __init__(self, message_id: str, source_queue: str):
        super().__init__()
        self.message_id = message_id
        self.source_queue = source_queue
        self.all_queues = []

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Move Message {self.message_id}"),
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
            self.all_queues = [q.get("Name", "") for q in queues if q.get("Name")]
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

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # Set the selected queue name in the input
        self.query_one("#target_queue", Input).value = event.option.prompt

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss()
        elif event.button.id == "move":
            target_queue = self.query_one("#target_queue", Input).value
            if target_queue:
                self.move_message(target_queue)

    def move_message(self, target_queue: str) -> None:
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
        if client.move_message(self.message_id, self.source_queue, target_queue):
            self.dismiss(True)
        else:
            self.notify("Failed to move message", severity="error")

