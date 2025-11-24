from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button
from textual.containers import Grid, Vertical
from amq_manager.client import ActiveMQClient

class BatchMoveModal(ModalScreen):
    CSS = """
    BatchMoveModal {
        align: center middle;
    }
    Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto auto auto auto;
        padding: 2;
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }
    Label {
        column-span: 2;
        text-align: center;
    }
    Input {
        column-span: 2;
    }
    """

    def __init__(self, message_ids: list, source_queue: str):
        super().__init__()
        self.message_ids = message_ids
        self.source_queue = source_queue

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"Move {len(self.message_ids)} messages"),
            Label(f"from {self.source_queue}"),
            Input(placeholder="Target Queue Name", id="target_queue"),
            Button("Cancel", variant="error", id="cancel"),
            Button("Move", variant="primary", id="move"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(False)
        elif event.button.id == "move":
            target_queue = self.query_one("#target_queue", Input).value
            if target_queue:
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
