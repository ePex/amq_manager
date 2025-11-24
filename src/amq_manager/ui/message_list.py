from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Static
from amq_manager.client import ActiveMQClient
from amq_manager.ui.message_detail import MessageDetailScreen

class MessageListScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, queue_name: str):
        super().__init__()
        self.queue_name = queue_name
        self.messages_map = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"Messages in Queue: {self.queue_name}", id="title")
        yield DataTable(cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Timestamp", "Priority", "Redelivered")
        self.load_messages()

    def load_messages(self) -> None:
        app = self.app
        if not hasattr(app, "active_config") or not app.active_config:
            return

        client = ActiveMQClient(
            app.active_config.host,
            app.active_config.port,
            app.active_config.user,
            app.active_config.password
        )
        messages = client.browse_messages(self.queue_name)
        table = self.query_one(DataTable)
        table.clear()
        
        for msg in messages:
            # Jolokia returns message details
            msg_id = msg.get("JMSMessageID", "Unknown")
            timestamp = msg.get("JMSTimestamp", "")
            priority = str(msg.get("JMSPriority", ""))
            redelivered = str(msg.get("JMSRedelivered", ""))
            
            table.add_row(msg_id, str(timestamp), priority, redelivered, key=msg_id)
            self.messages_map[msg_id] = msg

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        msg_id = event.row_key.value
        if msg_id in self.messages_map:
            self.app.push_screen(MessageDetailScreen(self.messages_map[msg_id], self.queue_name))
