# Feature Request: Display All Message Headers

**Date:** 2025-11-24
**Status:** Planned

## Description
The user wants to see all available headers and properties of a message in the Message Detail view, rather than just a selected few.

## Requirements
- **Message Detail UI**:
  - Iterate through all keys returned by the broker for the message.
  - Display them in a structured format (e.g., Key-Value list or Table).
  - Exclude the message body/text from this list as it is displayed separately.
  - Handle formatting for timestamps or complex objects if necessary.

## UI/UX
- **Properties Section**: Replace the current `str(self.message)` dump with a clean list or table of all properties.
