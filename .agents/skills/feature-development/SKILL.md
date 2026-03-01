---
name: "feature-development"
description: "A standardized workflow for developing new features. Activates when the user asks to create a new feature, add significant functionality, or design a new component. Enforces a spec-first, design-first approach with mandatory user review."
---

# Feature Development AgentSkill

When the user requests to create a new feature or modify an existing one significantly, you **MUST** follow this design-first workflow:

## 1. Information Gathering

- Review existing documentation in the `docs/` directory (e.g., `ETL_SPEC.md`, `DATABASE_SPEC.md`, `AIRFLOW_SPEC.md`).
- Examine relevant codebase components to understand the current context and constraints.
- Identify the core components that will need to be touched.

## 2. Specification & Implementation Design

- Write a detailed specification and implementation plan.
- Explain the new expected data flow, architecture changes, and database modifications.
- Use Mermaid diagrams if applicable to visualize data flows or architectural changes.
- Document this plan clearly (e.g., in a temporary artifact like `implementation_plan.md`).

## 3. Review Checkpoint

- Present the specification and implementation design to the USER.
- **CRITICAL**: Do **not** write any implementation code yet.
- Use the `notify_user` tool (with `BlockedOnUser: true`) to ask for their explicit review and approval of the design.
- Wait for the user's explicit approval before proceeding.

## 4. Implementation

- Once the user approves the spec, proceed with writing the code (Python scripts, Airflow DAGs, etc.).
- Ensure the implementation strictly matches the approved specification.

## 5. Documentation Updating

- After the code is finalized and tested, ensure that the core documentation files in `docs/` (`ETL_SPEC.md`, `DATABASE_SPEC.md`, `AIRFLOW_SPEC.md`) are updated to reflect the new implementation.
