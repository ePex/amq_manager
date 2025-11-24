# Feature Request: View Messages

**Date:** 2025-11-24
**Status:** Implemented

## Description
The user needs to inspect the messages within a specific queue to debug issues or verify message content.

## Requirements
- **Message List**:
  - Browse messages for a selected queue.
  - Display summary info: Message ID, Timestamp, Priority, Redelivered status.
- **Message Detail**:
  - View full details of a single selected message.
  - Display all JMS headers (e.g., JMSMessageID, JMSTimestamp, JMSPriority, JMSRedelivered, JMSType).
  - Display the message body/text.

## UI/UX
- **List View**: A secondary screen showing a table of messages.
- **Detail View**: A dedicated screen showing key-value pairs for headers and a text block for the body.
