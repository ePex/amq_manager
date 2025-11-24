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
        ("r", "refresh", "Refresh"),
        ("space", "toggle_selection", "Select"),
        ("a", "select_all", "Select All"),
        ("n", "clear_selection", "Clear"),
        ("D", "batch_delete", "Delete Selected"),
        ("M", "batch_move", "Move Selected"),
    ]

    def __init__(self, queue_name: str):
        super().__init__()
        self.queue_name = queue_name
        self.messages_map = {}
        self.messages_data = []
        self.selected_messages = set()  # Track selected message IDs

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"Messages in Queue: {self.queue_name}", id="title")
        yield Static("", id="selection_status")
        yield DataTable(cursor_type="row")
        yield Input(placeholder="Filter by ID, Date, or Type...", id="filter")
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
            
            # Filter across multiple fields: ID, Timestamp, Type
            if filter_text:
                id_match = filter_text in msg_id.lower()
                timestamp_match = filter_text in str(timestamp).lower()
                type_match = filter_text in jms_type.lower()
                
                if not (id_match or timestamp_match or type_match):
                    continue
            
            # Add selection marker
            checkbox = "[✓] " if msg_id in self.selected_messages else "[ ] "
            display_id = checkbox + msg_id
            
            table.add_row(display_id, str(timestamp), priority, redelivered, jms_type, key=msg_id)
            self.messages_map[msg_id] = msg
        
        self.update_selection_status()

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

    def update_selection_status(self) -> None:
        status = self.query_one("#selection_status", Static)
        count = len(self.selected_messages)
        if count > 0:
            status.update(f"✓ {count} message{'s' if count != 1 else ''} selected")
        else:
            status.update("")

    def action_toggle_selection(self) -> None:
        table = self.query_one(DataTable)
        cursor_coord = table.cursor_coordinate
        if cursor_coord.row is None:
            return
        
        # Get the row key from the cursor coordinate
        cell_key = table.coordinate_to_cell_key(cursor_coord)
        msg_id = cell_key.row_key.value
        
        if msg_id in self.selected_messages:
            self.selected_messages.remove(msg_id)
        else:
            self.selected_messages.add(msg_id)
        
        # Save cursor position
        current_row = cursor_coord.row
        
        self.update_table()
        
        # Restore cursor position
        table.move_cursor(row=current_row, column=0)

    def action_select_all(self) -> None:
        self.selected_messages = set(self.messages_map.keys())
        self.update_table()

    def action_clear_selection(self) -> None:
        self.selected_messages.clear()
        self.update_table()

    def action_batch_delete(self) -> None:
        if not self.selected_messages:
            self.notify("No messages selected", severity="warning")
            return
        
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
        total = len(self.selected_messages)
        for msg_id in list(self.selected_messages):
            if client.delete_message(msg_id, self.queue_name):
                success_count += 1
        
        self.selected_messages.clear()
        self.load_messages()
        self.notify(f"Deleted {success_count}/{total} messages")

    def action_batch_move(self) -> None:
        if not self.selected_messages:
            self.notify("No messages selected", severity="warning")
            return
        
        from amq_manager.ui.batch_move_modal import BatchMoveModal
        
        def handle_move(success_count):
            if success_count:
                total = len(self.selected_messages)
                self.selected_messages.clear()
                self.load_messages()
                self.notify(f"Moved {success_count}/{total} messages")
        
        self.app.push_screen(BatchMoveModal(list(self.selected_messages), self.queue_name), handle_move)

    def action_refresh(self) -> None:
        self.load_messages()
        self.notify("Messages refreshed")

