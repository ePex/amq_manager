from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, DataTable, Button, Input, Label, Checkbox
from textual.containers import Grid, Container, Horizontal
from amq_manager.config import ConfigManager, ConnectionConfig

class ConnectionEditor(ModalScreen):
    CSS = """
    ConnectionEditor {
        align: center middle;
    }
    Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: auto auto auto auto auto auto auto;
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
    Checkbox {
        column-span: 2;
    }
    """

    def __init__(self, config: ConnectionConfig = None):
        super().__init__()
        self.config = config
        self.is_edit = config is not None

    def compose(self) -> ComposeResult:
        title = "Edit Connection" if self.is_edit else "New Connection"
        yield Grid(
            Label(title),
            Input(placeholder="Name", value=self.config.name if self.config else "", id="name"),
            Input(placeholder="Host", value=self.config.host if self.config else "localhost", id="host"),
            Input(placeholder="Port", value=str(self.config.port) if self.config else "8161", id="port", type="integer"),
            Input(placeholder="User", value=self.config.user if self.config else "admin", id="user"),
            Input(placeholder="Password", value=self.config.password if self.config else "admin", id="password", password=True),
            Checkbox("Use SSL", value=self.config.ssl if self.config else False, id="ssl"),
            Checkbox("Default", value=self.config.is_default if self.config else False, id="default"),
            Horizontal(
                Button("Cancel", variant="error", id="cancel"),
                Button("Save", variant="primary", id="save"),
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss()
        elif event.button.id == "save":
            self.save_connection()

    def save_connection(self) -> None:
        name = self.query_one("#name", Input).value
        host = self.query_one("#host", Input).value
        port = int(self.query_one("#port", Input).value)
        user = self.query_one("#user", Input).value
        password = self.query_one("#password", Input).value
        ssl = self.query_one("#ssl", Checkbox).value
        is_default = self.query_one("#default", Checkbox).value

        new_config = ConnectionConfig(name, host, port, user, password, is_default, ssl)
        self.dismiss(new_config)

class ConnectionScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("a", "add_connection", "Add"),
        ("e", "edit_connection", "Edit"),
        ("d", "delete_connection", "Delete"),
        ("enter", "select_connection", "Select"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Manage Connections", id="title")
        yield DataTable(cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Name", "Host", "Port", "User", "SSL", "Default")
        self.refresh_list()

    def refresh_list(self) -> None:
        config_manager = ConfigManager()
        table = self.query_one(DataTable)
        table.clear()
        for c in config_manager.connections:
            table.add_row(
                c.name, c.host, str(c.port), c.user, "Yes" if c.ssl else "No", "Yes" if c.is_default else "",
                key=c.name
            )

    def action_add_connection(self) -> None:
        def handle_add(config: ConnectionConfig):
            if config:
                ConfigManager().add_connection(config)
                self.refresh_list()
        self.app.push_screen(ConnectionEditor(), handle_add)

    def action_edit_connection(self) -> None:
        table = self.query_one(DataTable)
        if not table.cursor_row is None:
            name = table.get_row_at(table.cursor_row)[0] # Name is first column
            # Find config object
            config_manager = ConfigManager()
            config = next((c for c in config_manager.connections if c.name == name), None)
            
            def handle_edit(new_config: ConnectionConfig):
                if new_config:
                    config_manager.update_connection(name, new_config)
                    self.refresh_list()
            
            if config:
                self.app.push_screen(ConnectionEditor(config), handle_edit)

    def action_delete_connection(self) -> None:
        table = self.query_one(DataTable)
        if not table.cursor_row is None:
            name = table.get_row_at(table.cursor_row)[0]
            ConfigManager().delete_connection(name)
            self.refresh_list()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.action_select_connection()

    def action_select_connection(self) -> None:
        table = self.query_one(DataTable)
        if not table.cursor_row is None:
            name = table.get_row_at(table.cursor_row)[0]
            config_manager = ConfigManager()
            config = next((c for c in config_manager.connections if c.name == name), None)
            if config:
                self.dismiss(config)
