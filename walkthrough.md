# ActiveMQ Manager TUI - Walkthrough

I have built a Terminal User Interface (TUI) for managing ActiveMQ brokers.

## Features
- **Queue List**: View all queues with pending message counts, consumer counts, etc.
- **Message List**: Browse messages within a queue.
- **Message Details**: View full message headers and body.
- **Management**: Move or Delete messages directly from the UI.
- **Connections**: Manage multiple broker connections and switch at runtime.

## How to Run
1. Ensure you have Python 3.10+ installed.
2. Install dependencies:
   ```bash
   pip install textual requests stomp.py
   ```
3. Run the application:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
   python3 src/amq_manager/main.py
   ```

## Usage
- **Navigation**: Use arrow keys to navigate lists.
- **Select**: Press `Enter` to select a queue or message.
- **Back**: Press `Esc` to go back.
- **Filter**: Press `/` to filter queues or messages.
- **Refresh**: Press `r` to refresh the queue list.
- **Connections**: Press `c` to open the Connection Manager.
- **Logs**: Press `l` to open the Log Viewer.
- **Delete**: Press `d` in Message Detail view to delete a message.
- **Move**: Press `m` in Message Detail view to move a message.

## Managing Connections
1. Press `c` on the main screen.
2. Press `a` to add a new connection.
3. Enter details (Name, Host, Port, User, Password).
4. Check **Use SSL** if connecting to a secure broker (e.g., AWS).
5. Press `Save`.
6. Select the new connection and press `Enter` to switch.

