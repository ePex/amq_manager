from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Container
from amq_manager.client import ActiveMQClient
from amq_manager.config import ConfigManager, ConnectionConfig
from amq_manager.ui.message_list import MessageListScreen
from amq_manager.ui.connection_screen import ConnectionScreen
from amq_manager.ui.log_screen import LogScreen
import logging

logger = logging.getLogger(__name__)

class QueueList(Static):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Queue Name", "Pending", "Consumers", "Enqueued", "Dequeued")
        self.refresh_queues()

    def refresh_queues(self) -> None:
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
            table = self.query_one(DataTable)
            table.clear()
            
            for q in queues:
                table.add_row(
                    q.get("Name", "Unknown"),
                    str(q.get("QueueSize", 0)),
                    str(q.get("ConsumerCount", 0)),
                    str(q.get("EnqueueCount", 0)),
                    str(q.get("DequeueCount", 0)),
                    key=q.get("Name")
                )
            self.app.notify(f"Refreshed {len(queues)} queues")
            logger.info(f"Refreshed {len(queues)} queues")
        except Exception as e:
            error_msg = f"Error refreshing queues: {str(e)}"
            logger.error(error_msg)
            self.app.notify(error_msg, severity="error", timeout=10)
            table = self.query_one(DataTable)
            table.clear()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        queue_name = event.row_key.value
        self.app.push_screen(MessageListScreen(queue_name))

class ActiveMQManagerApp(App):
    CSS = """
    QueueList {
        height: 1fr;
    }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("c", "manage_connections", "Connections"),
        ("l", "show_logs", "Logs"),
    ]

    def on_mount(self) -> None:
        config_manager = ConfigManager()
        self.active_config = config_manager.get_default_connection()
        if self.active_config:
            self.title = f"ActiveMQ Manager - {self.active_config.name}"
        else:
            self.action_manage_connections()

    def compose(self) -> ComposeResult:
        yield Header()
        yield QueueList()
        yield Footer()

    def action_refresh(self) -> None:
        self.query_one(QueueList).refresh_queues()

    def action_manage_connections(self) -> None:
        def handle_select(config: ConnectionConfig):
            if config:
                self.active_config = config
                self.title = f"ActiveMQ Manager - {config.name}"
                self.query_one(QueueList).refresh_queues()
                self.notify(f"Switched to {config.name}")
        
        self.push_screen(ConnectionScreen(), handle_select)

    def action_show_logs(self) -> None:
        self.push_screen(LogScreen())

if __name__ == "__main__":
    app = ActiveMQManagerApp()
    app.run()
