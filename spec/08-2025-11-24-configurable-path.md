# Feature Request: Configurable Jolokia Context Path

**Date:** 2025-11-24
**Status:** Planned

## Description
The user is connecting to a broker where the Jolokia API might not be at the standard `/api/jolokia` path (or is returning HTML, suggesting a path mismatch). The application needs to allow configuring the API path.

## Requirements
- **Configuration**:
  - Add `context_path` string field to `ConnectionConfig`.
  - Default to `/api/jolokia`.
- **UI**:
  - Add "API Path" input to the Connection Editor.
- **Client**:
  - Use the configured path when constructing the base URL.

## UI/UX
- **Connection Editor**: Add input field for "API Path" (e.g., `/api/jolokia` or `/jolokia`).
