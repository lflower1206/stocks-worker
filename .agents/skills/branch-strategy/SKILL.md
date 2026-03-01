---
name: "branch-strategy"
description: "A standardized workflow for managing git branches based on the type of work being done. Activates when starting a new task, feature, bug fix, or any significant change that requires working on a separate branch."
---

# Branch Strategy AgentSkill

When beginning a new unit of work (feature, fix, chore, etc.), you **MUST** ensure the work is done on appropriately named branches rather than directly on the `main` branch.

## Branch Naming Conventions

Follow these prefixes based on the work purpose:

- **feature/**: For new features or significant enhancements (e.g., `feature/user-authentication`).
- **fix/**: For bug fixes (e.g., `fix/login-crash`).
- **chore/**: For routine tasks, maintenance, or dependency updates (e.g., `chore/update-dependencies`).
- **docs/**: For documentation-only changes (e.g., `docs/api-readme-update`).
- **refactor/**: For code refactoring without changing behavior (e.g., `refactor/extract-database-client`).

## Workflow Steps

1. **Identify the Work Type**: Determine the nature of the task (feature, fix, etc.).
2. **Checkout Branch**: Use `git checkout -b <prefix>/<descriptive-name>` to create and switch to the new branch before making any code changes or beginning implementation planning.
3. **Keep Branches Focused**: Ensure the work on the branch remains aligned with its prefix and scope.
