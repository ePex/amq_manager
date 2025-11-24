from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, DataTable
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from typing import Dict, Any
from amq_manager.client import ActiveMQClient
from amq_manager.ui.move_modal import MoveMessageModal

class MessageDetailScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("d", "delete_message", "Delete Message"),
        ("m", "move_message", "Move Message"),
        Binding("/", "noop", "", show=False),
    ]
    CSS = """
    .header {
        text-style: bold;
        margin-top: 1;
    }
    .content {
        margin-bottom: 1;
    }
    """

    def __init__(self, message: Dict[str, Any], queue_name: str):
        super().__init__()
        self.message = message
        self.queue_name = queue_name

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Label("Message Details", classes="header"),
            self.create_properties_table(),
            
            Label("Body", classes="header"),
            Static(str(self.message.get("Text", self.message.get("Body", "No Text Content"))), classes="content"),
        )
        yield Footer()

    def create_properties_table(self) -> DataTable:
        table = DataTable()
        table.add_columns("Property", "Value")
        
        # Exclude body fields from properties list
        exclude = {"Text", "Body"}
        
        for key, value in self.message.items():
            if key not in exclude:
                table.add_row(str(key), str(value))
        return table

    def action_delete_message(self) -> None:
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
        msg_id = self.message.get("JMSMessageID")
        if client.delete_message(msg_id, self.queue_name):
            self.app.pop_screen()
            self.notify("Message deleted")
        else:
            self.notify("Failed to delete message", severity="error")

    def action_move_message(self) -> None:
        msg_id = self.message.get("JMSMessageID")
        
        def check_move(moved: bool) -> None:
            if moved:
                self.app.pop_screen()
                self.notify("Message moved")

        self.app.push_screen(MoveMessageModal(msg_id, self.queue_name), check_move)

    def action_noop(self) -> None:
        pass
