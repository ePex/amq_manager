from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button
from textual.containers import Grid
from amq_manager.client import ActiveMQClient

class MoveMessageModal(ModalScreen):
    CSS = """
    MoveMessageModal {
        align: center middle;
    }
    Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto auto auto;
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

    def __init__(self, message_id: str, source_queue: str):
        super().__init__()
        self.message_id = message_id
        self.source_queue = source_queue

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"Move Message {self.message_id}"),
            Input(placeholder="Target Queue Name", id="target_queue"),
            Button("Cancel", variant="error", id="cancel"),
            Button("Move", variant="primary", id="move"),
        )

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
            app.active_config.password
        )
        if client.move_message(self.message_id, self.source_queue, target_queue):
            self.dismiss(True)
        else:
            self.notify("Failed to move message", severity="error")
