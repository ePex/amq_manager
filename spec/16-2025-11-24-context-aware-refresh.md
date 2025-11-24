# Feature: Context-Aware Refresh

**Date:** 2025-11-24
**Status:** Implemented

## Description
Make the refresh (`r`) key context-aware based on the current screen.

## Requirements
- **Queue List Screen**: `r` key refreshes the list of queues
- **Message List Screen**: `r` key refreshes the list of messages in the current queue
- **No Conflict**: Local screen bindings override global app bindings

## Implementation
- Added `r` binding to MessageListScreen BINDINGS
- Implemented `action_refresh()` in MessageListScreen
- Calls `load_messages()` and shows notification

## UI/UX
- Consistent `r` key behavior across screens
- Shows "Messages refreshed" notification in message list
- Shows "Refreshed X queues" notification in queue list
