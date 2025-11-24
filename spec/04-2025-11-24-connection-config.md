# Feature Request: Connection Configuration

**Date:** 2025-11-24
**Status:** Partially Implemented (Hardcoded Defaults)

## Description
The application must support connecting to different ActiveMQ brokers, including local instances and AWS-hosted brokers.

## Requirements
- Support connecting via HTTP/HTTPS (Jolokia).
- Support Basic Authentication (Username/Password).
- **Current State**: Defaults to `localhost:8161` with `admin/admin`.
- **Future Requirement**: Allow configuration via:
  - Environment Variables
  - Command Line Arguments
  - Configuration File (e.g., `~/.amq_manager/config.toml`)
  - Interactive Login Screen

## UI/UX
- Ideally, a startup screen asking for connection details if not provided via config.
