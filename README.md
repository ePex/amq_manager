# ActiveMQ Manager

A Terminal User Interface (TUI) tool for managing ActiveMQ brokers. This tool allows you to view queues, browse messages, and perform management actions like moving or deleting messages, all from your terminal.

## Features

- **Queue Dashboard**: View all queues with real-time statistics (pending messages, consumers, enqueued/dequeued counts).
- **Message Browser**: Browse messages within any queue.
- **Message Inspector**: View full message details, including headers (JMSMessageID, Timestamp, Priority, etc.) and body content.
- **Management Actions**:
    - **Delete**: Remove individual messages from a queue.
    - **Move**: Move messages from one queue to another (e.g., for reprocessing DLQ messages).
- **Multi-Connection Support**: Manage and switch between multiple brokers (Local, AWS, etc.) at runtime.
- **Secure Connections**: Support for HTTPS/SSL connections.
- **Filtering**: Quickly find queues (by name) or messages (by type) using the `/` hotkey.
- **Logging**: Built-in log viewer to diagnose issues.
- **Cross-Platform**: Runs on any system with Python support.

## Prerequisites

- Python 3.10 or higher
- Access to an ActiveMQ broker (default: `localhost:8161` via Jolokia)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Install dependencies**:
   It is recommended to use a virtual environment.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install .
   ```
   *Alternatively, install directly:*
   ```bash
   pip install textual requests stomp.py
   ```

## Usage

### Running the Application

If installed via `pip install .`:
```bash
amq-manager
```

Or running from source:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 src/amq_manager/main.py
```

### Navigation & Controls

| Context | Key | Action |
| :--- | :--- | :--- |
| **Global** | `Ctrl+c` | Quit Application |
| **Queue List** | `↑` / `↓` | Navigate Queues |
| | `Enter` | Open Selected Queue |
| | `r` | Refresh Queue List |
| | `/` | **Filter** Queues |
| **Message List** | `↑` / `↓` | Navigate Messages |
| | `Enter` | View Message Details |
| | `Esc` | Back to Queue List |
| | `/` | **Filter** Messages (by JMSType) |
| **Message Detail** | `d` | **Delete** Message |
| | `m` | **Move** Message |
| | `Esc` | Back to Message List |
| **Connection Manager** | `c` | Open **Connections** (from Queue List) |
| | `a` | **Add** Connection |
| | `e` | **Edit** Connection |
| | `d` | **Delete** Connection |
| | `Enter` | **Select/Switch** Connection |
| **Log Viewer** | `l` | Open **Logs** (from Queue List) |
| | `r` | **Refresh** Logs |
| | `Esc` | Back to Queue List |

## Configuration

The application stores configuration in `~/.amq_manager/config.json`.

You can manage connections directly within the application by pressing `c` on the main screen.
- **Add**: Create a new broker connection.
- **Edit**: Modify an existing connection.
- **Select**: Switch to a different broker immediately.


## Development

### Project Structure

- `src/amq_manager/`: Source code
    - `main.py`: Entry point
    - `client.py`: ActiveMQ Jolokia client wrapper
    - `ui/`: Textual UI components
        - `app.py`: Main application and Queue List
        - `message_list.py`: Message browsing screen
        - `message_detail.py`: Message inspection screen
        - `move_modal.py`: Modal for moving messages

### Running Tests
*(Placeholder for test instructions)*
```bash
# python -m pytest tests/
```
