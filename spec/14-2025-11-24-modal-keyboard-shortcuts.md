# Feature: Modal Keyboard Shortcuts

**Date:** 2025-11-24
**Status:** Implemented

## Description
Enhanced keyboard navigation for all modal dialogs (connection editor, move message modals).

## Requirements
- **Enter Key**: Confirms/saves the modal action
  - In connection editor: saves the connection
  - In move modals: executes the move operation
- **Esc Key**: Cancels and closes the modal
- **Tab Key**: Navigates between form fields
- **Input Submit**: Pressing Enter in any input field triggers the save/confirm action

## Implementation
- Added BINDINGS to all modal screens
- Added `action_cancel()` and `action_save()`/`action_move()` methods
- Implemented `on_input_submitted()` handlers to trigger actions on Enter

## UI/UX
- Keyboard shortcuts shown in footer
- Standard modal interaction patterns
- Smooth workflow without requiring mouse clicks
