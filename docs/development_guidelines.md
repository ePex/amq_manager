# Development Guidelines

## Task Completion Rules

To ensure high quality and maintainability of the `amq-manager` project, please adhere to the following rules when completing tasks:

1.  **Feature Specifications**:
    - Always document new features in the `spec/` directory **before** or **immediately after** implementation.
    - Follow the naming convention: `%d-yyyy-mm-dd-%s.md` (e.g., `01-2025-11-01-feature-name.md`).
    - Include Description, Requirements, and UI/UX details.

2.  **Documentation Maintenance**:
    - **README.md**: Update the Features and Usage sections whenever a user-facing change is made.
    - **implementation_plan.md**: Keep the plan up to date with the current architecture and progress.
    - **task.md**: Track progress by marking tasks as completed (`[x]`).
    - **walkthrough.md**: Update the walkthrough to reflect new workflows or UI changes.

3.  **Code Quality**:
    - Ensure new code is typed (using Python type hints).
    - Follow the existing project structure (`src/amq_manager/`).

4.  **Verification**:
    - Verify changes against a local broker (or appropriate environment) before marking a task as done.
