# Feature Request: Manage Messages (Move/Delete)

**Date:** 2025-11-24
**Status:** Implemented

## Description
The user needs to perform administrative actions on messages, specifically moving them (e.g., from a DLQ to a processing queue) or deleting them.

## Requirements
- **Delete Message**:
  - Allow the user to delete a specific message from the broker.
  - Provide feedback on success or failure.
- **Move Message**:
  - Allow the user to move a message to a different queue.
  - Prompt the user for the destination queue name.
  - Provide feedback on success or failure.

## UI/UX
- **Delete**: Triggered via a hotkey (e.g., 'd') in the Message Detail view.
- **Move**: Triggered via a hotkey (e.g., 'm') in the Message Detail view, opening a modal dialog to input the target queue.
