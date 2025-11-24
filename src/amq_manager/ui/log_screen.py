from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, RichLog
from textual.binding import Binding
import os

class LogScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("r", "refresh_log", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(highlight=True, markup=True, id="log_view")
        yield Footer()

    def on_mount(self) -> None:
        self.action_refresh_log()

    def action_refresh_log(self) -> None:
        log_view = self.query_one(RichLog)
        log_view.clear()
        
        log_file = "amq_manager.log"
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    # Read last 1000 lines to avoid memory issues
                    lines = f.readlines()[-1000:]
                    for line in lines:
                        log_view.write(line.strip())
            except Exception as e:
                log_view.write(f"[red]Error reading log file: {e}[/red]")
        else:
            log_view.write("[yellow]No log file found.[/yellow]")
