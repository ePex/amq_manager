# Feature Request: Enhanced Message Filtering

**Date:** 2025-11-24
**Status:** Planned

## Description
Enhance the message list filtering to support multiple fields instead of just JMSType.

## Requirements
- **Filter Fields**:
  - Message ID (JMSMessageID)
  - Timestamp (JMSTimestamp) - date/time matching
  - JMSType
- **Filter Logic**: Search across all three fields (OR logic - match if any field contains the filter text)
- **UI**: Same `/` hotkey and input field, but filter checks all three columns

## UI/UX
- **Filter Input**: Shows "Filter by ID, Date, or Type..." as placeholder
- **Matching**: Case-insensitive substring match across all three fields
