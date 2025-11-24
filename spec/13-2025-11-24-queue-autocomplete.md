# Feature Request: Queue Autocomplete in Move Operations

**Date:** 2025-11-24
**Status:** Planned

## Description
Add autocomplete/suggestion functionality to the move message modal to help users quickly select target queues.

## Requirements
- **Autocomplete Source**: Fetch available queue names from the current broker
- **UI Component**: Use a suggestion dropdown or similar widget
- **Behavior**:
  - Show suggestions as user types
  - Filter suggestions based on input
  - Allow selection via arrow keys and Enter
  - Still allow manual input for queues not yet created
- **Apply to**: Both single message move and batch move modals

## UI/UX
- Dropdown appears below the input field
- Suggestions filtered by substring match (case-insensitive)
- Visual highlight on selected suggestion
