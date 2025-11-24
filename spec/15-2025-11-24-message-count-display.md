# Feature: Message Count Display

**Date:** 2025-11-24
**Status:** Implemented

## Description
Display the number of messages in the title bar when viewing a queue's message list.

## Requirements
- **Normal Display**: Show total message count (e.g., "10 messages")
- **Filtered Display**: Show filtered count and total (e.g., "5/10 (filtering)")
- **Singular/Plural**: Handle grammar correctly (1 message vs 2 messages)
- **Dynamic Update**: Update count as filter changes

## Implementation
- Added `update_title()` method to MessageListScreen
- Tracks both total messages (`messages_data`) and visible messages (`messages_map`)
- Called after `update_table()` to keep count in sync

## UI/UX
- Displayed in the title Static widget at top of message list screen
- Format: "Messages in Queue: {queue_name} - {count}"
- Filtering format: "Messages in Queue: {queue_name} - {visible}/{total} (filtering)"
