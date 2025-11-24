# Feature Request: HTTPS Support

**Date:** 2025-11-24
**Status:** Planned

## Description
The user needs to connect to ActiveMQ brokers that are secured via SSL/TLS (HTTPS), specifically for AWS and internal dev environments.

## Requirements
- **Configuration**:
  - Add an `ssl` (boolean) flag to the connection configuration.
  - Default to `False` (HTTP) for backward compatibility.
- **Client**:
  - Update the network client to use `https://` scheme when the SSL flag is true.
  - Ensure SSL verification is handled (default to verifying, but maybe allow insecure for self-signed certs if needed later).
- **UI**:
  - Add a "Use SSL" checkbox to the Connection Editor screen.

## UI/UX
- **Connection Editor**: A new checkbox labeled "Use SSL" below the Port input.
