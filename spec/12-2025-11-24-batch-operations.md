# Feature Request: Batch Message Operations

**Date:** 2025-11-24
**Status:** Planned

## Description
Enable multi-select capability in the message list to perform batch operations (move/delete) on multiple messages.

## Requirements
- **Selection Mode**:
  - Space bar to toggle selection on current message
  - Visual indicator for selected messages (checkbox or highlight)
  - Display count of selected messages
- **Batch Operations**:
  - `D` (uppercase) to delete all selected messages
  - `M` (uppercase) to move all selected messages to a target queue
  - Operations should iterate through selected messages and report success/failure count
- **Keyboard Shortcuts**:
  - `Space` - Toggle selection
  - `a` - Select all visible messages
  - `n` - Clear all selections
  - `D` - Delete selected
  - `M` - Move selected

## UI/UX
- **Visual**: Selected rows highlighted or with a checkbox indicator
- **Status Bar**: Show "X messages selected" when selections exist
- **Confirmation**: Prompt confirmation before bulk delete/move operations
