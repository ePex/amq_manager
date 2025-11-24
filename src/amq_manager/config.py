import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

CONFIG_DIR = os.path.expanduser("~/.amq_manager")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

@dataclass
class ConnectionConfig:
    name: str
    host: str
    port: int
    user: str
    password: str
    is_default: bool = False
    ssl: bool = False

class ConfigManager:
    def __init__(self):
        self.connections: List[ConnectionConfig] = []
        self.load_config()

    def load_config(self) -> None:
        if not os.path.exists(CONFIG_FILE):
            # Create default config
            self.connections = [
                ConnectionConfig("Local", "localhost", 8161, "admin", "admin", True, False)
            ]
            self.save_config()
            return

        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.connections = [ConnectionConfig(**c) for c in data.get("connections", [])]
        except Exception as e:
            print(f"Error loading config: {e}")
            self.connections = []

    def save_config(self) -> None:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        
        data = {
            "connections": [asdict(c) for c in self.connections]
        }
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_default_connection(self) -> Optional[ConnectionConfig]:
        for c in self.connections:
            if c.is_default:
                return c
        return self.connections[0] if self.connections else None

    def add_connection(self, config: ConnectionConfig) -> None:
        if config.is_default:
            for c in self.connections:
                c.is_default = False
        self.connections.append(config)
        self.save_config()

    def update_connection(self, old_name: str, new_config: ConnectionConfig) -> None:
        if new_config.is_default:
            for c in self.connections:
                c.is_default = False
        
        for i, c in enumerate(self.connections):
            if c.name == old_name:
                self.connections[i] = new_config
                break
        self.save_config()

    def delete_connection(self, name: str) -> None:
        self.connections = [c for c in self.connections if c.name != name]
        self.save_config()
