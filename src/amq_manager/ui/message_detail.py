from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Container, VerticalScroll
from typing import Dict, Any
from amq_manager.client import ActiveMQClient
from amq_manager.ui.move_modal import MoveMessageModal

class MessageDetailScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("d", "delete_message", "Delete Message"),
        ("m", "move_message", "Move Message"),
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
            Static(f"ID: {self.message.get('JMSMessageID')}", classes="content"),
            Static(f"Timestamp: {self.message.get('JMSTimestamp')}", classes="content"),
            Static(f"Type: {self.message.get('JMSType')}", classes="content"),
            Static(f"Redelivered: {self.message.get('JMSRedelivered')}", classes="content"),
            
            Label("Properties", classes="header"),
            Static(str(self.message), classes="content"), # TODO: Format nicely
            
            Label("Body", classes="header"),
            Static(str(self.message.get("Text", "No Text Content")), classes="content"), # Jolokia might return 'Text' or 'Body'
        )
        yield Footer()

    def action_delete_message(self) -> None:
        app = self.app
        if not hasattr(app, "active_config") or not app.active_config:
            return

        client = ActiveMQClient(
            app.active_config.host,
            app.active_config.port,
            app.active_config.user,
            app.active_config.password
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
