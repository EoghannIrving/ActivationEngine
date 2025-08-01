# Known Issues

The following are potential bugs or design concerns identified in the current code base.

1. **Mutable default for lists** – Both `Context.projects_active` and `Task.tags` set an empty list directly as a default. This can lead to shared mutable state between model instances. Pydantic's `default_factory` should be used instead.
2. **Unhandled YAML parse errors** – `load_weights()` only handles `FileNotFoundError`. If `weights.yaml` exists but contains invalid YAML, the application will crash when loading.
3. **Relative path lookup for weights** – `load_weights()` opens `weights.yaml` using a relative path. Running the application from another directory will fail to locate the file.
4. **Unused scoring weight** – `context_match_weight` is defined in `weights.yaml` and loaded but never referenced in the scoring logic, so it has no effect.
5. **Incorrect default logic with `or`** – In `rank_tasks()`, the use of `task.energy_cost or 3` and `task.executive_cost or 3` treats zero values as missing, preventing valid zero-cost tasks.
6. **Non‑deterministic tag order** – `get_tags()` converts the list of tags to a `set` and back to a list, which loses order and may produce different results for the same input.
7. **Imported but unused module** – `os` is imported in `main.py` but never used.
8. **Lack of input validation** – `UserState.energy`, `Task.energy_cost` and `Task.executive_cost` are expected to be in a 1–5 range, but no validation enforces this, allowing nonsensical values.
