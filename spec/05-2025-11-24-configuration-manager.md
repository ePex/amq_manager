# Feature Request: Configuration Manager & Connection Switching

**Date:** 2025-11-24
**Status:** Implemented

## Description
The user needs to manage multiple ActiveMQ broker connections (e.g., Local, AWS Dev, AWS Prod) and switch between them at runtime without restarting the application.

## Requirements
- **Configuration Storage**:
  - Save connections to a persistent file (e.g., `~/.amq_manager/config.json`).
  - Support fields: Name, Host, Port, User, Password, Default flag.
- **Connection Management UI**:
  - List all saved connections.
  - Add new connections.
  - Edit existing connections.
  - Delete connections.
- **Runtime Switching**:
  - Allow selecting a connection from the list to make it active immediately.
  - Refresh the queue list upon switching.

## UI/UX
- **Access**: Accessed via a hotkey (e.g., 'c') from the main Queue List.
- **Screen**: A modal or dedicated screen with a table of connections and action buttons (Add, Edit, Delete).
- **Editor**: A form to input connection details.
