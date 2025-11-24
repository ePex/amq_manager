# ActiveMQ Manager - Implementation Plan

## Goal Description
Build a Terminal User Interface (TUI) application to manage ActiveMQ brokers. The tool will support connecting to both local and AWS-hosted brokers. Key features include listing queues, viewing messages, and performing actions like moving or deleting messages.

## User Review Required
> [!IMPORTANT]
> I am proposing a **Python TUI (Terminal User Interface)** using the `textual` library. This offers a rich, interactive experience (like a GUI but in the terminal) which is ideal for browsing queues and managing messages efficiently.
>
> **Tech Stack:**
> - Language: Python 3.10+
> - UI Library: `textual`
> - Connection: `stomp.py` (for messaging operations) and/or `requests` (for Jolokia REST API if needed for management stats). *Decision needed: STOMP is standard for messaging, but Jolokia is often better for "management" (listing queues, etc.). I will likely use a hybrid or just Jolokia if enabled.*

## Proposed Changes

### Project Structure
- `amq_manager/`: Main package
    - `main.py`: Entry point
    - `config.py`: Configuration manager (NEW)
    - `ui/`: TUI components (Screens, Widgets)
        - `connection_screen.py`: Connection management (NEW)
    - `client/`: ActiveMQ client wrapper (handling STOMP/Jolokia)

### Configuration System
- **Storage**: `~/.amq_manager/config.json`
- **Structure**:
  ```json
  {
    "connections": [
      {"name": "Local", "host": "localhost", "port": 8161, "user": "admin", "password": "...", "default": true},
      {"name": "AWS Dev", "host": "...", ...}
    ]
  }
  ```
- **Runtime Switching**: The App will hold a reference to the `current_connection` and re-initialize the `ActiveMQClient` when switched.

### Logging System
- **File**: `amq_manager.log`
- **Format**: `YYYY-MM-DD HH:MM:SS - Logger - Level - Message`
- **UI**: `LogScreen` (RichLog widget) to view logs within the app.

### Dependencies
- `textual`
- `stomp.py` (or `requests` if using Jolokia)

## Verification Plan
### Automated Tests
- Unit tests for the `client` wrapper.

### Manual Verification
- Connect to a local ActiveMQ instance (user provided or Docker).
- Create test queues and messages.
- Verify listing, viewing, moving, and deleting messages via the TUI.
