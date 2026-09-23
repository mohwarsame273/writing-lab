# Phase 0 Architecture Decisions

- **Persistence**: While `rx.Model` is configured, it is largely bypassed by `lab_state.py`. We will formalize PostgreSQL/SQLite persistent storage and create full domain models with Alembic migrations in Phase 1.
- **State Management**: State currently lives entirely in `LabState`. We will move the persistence logic correctly into the services layer while maintaining `LabState` as the UI bridge.
