from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Static, Input
from amq_manager.client import ActiveMQClient
from amq_manager.ui.message_detail import MessageDetailScreen

class MessageListScreen(Screen):
    CSS = """
    #filter {
        display: none;
        dock: bottom;
        height: 3;
    }
    """
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("/", "toggle_filter", "Filter"),
    ]

    def __init__(self, queue_name: str):
        super().__init__()
        self.queue_name = queue_name
        self.messages_map = {}
        self.messages_data = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"Messages in Queue: {self.queue_name}", id="title")
        yield DataTable(cursor_type="row")
        yield Input(placeholder="Filter by JMSType...", id="filter")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Timestamp", "Priority", "Redelivered", "Type")
        self.load_messages()

    def load_messages(self) -> None:
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
        self.messages_data = client.browse_messages(self.queue_name)
        self.update_table()

    def update_table(self, filter_text: str = "") -> None:
        table = self.query_one(DataTable)
        table.clear()
        self.messages_map = {}
        
        filter_text = filter_text.lower()
        
        for msg in self.messages_data:
            # Jolokia returns message details
            msg_id = msg.get("JMSMessageID", "Unknown")
            timestamp = msg.get("JMSTimestamp", "")
            priority = str(msg.get("JMSPriority", ""))
            redelivered = str(msg.get("JMSRedelivered", ""))
            jms_type = str(msg.get("JMSType", ""))
            
            if filter_text and filter_text not in jms_type.lower():
                continue
            
            table.add_row(msg_id, str(timestamp), priority, redelivered, jms_type, key=msg_id)
            self.messages_map[msg_id] = msg

    def on_input_changed(self, event: Input.Changed) -> None:
        self.update_table(event.value)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.query_one("#filter").display = False
        self.query_one(DataTable).focus()

    def action_toggle_filter(self) -> None:
        inp = self.query_one("#filter")
        inp.display = not inp.display
        if inp.display:
            inp.focus()
        else:
            inp.value = ""
            self.query_one(DataTable).focus()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        msg_id = event.row_key.value
        if msg_id in self.messages_map:
            self.app.push_screen(MessageDetailScreen(self.messages_map[msg_id], self.queue_name))
