# Repository Guidelines

## Project Structure & Module Organization
This directory is currently empty, but it is inside the parent `ai_project` Git repository. The active application code lives in `../x_monitor/`. Backend code is organized by domain: `twitter/`, `stock/`, `polymarket/`, `binance_hot/`, and `hyperliquid/`, with shared auth, database, crypto, and notification helpers in `shared/`. The FastAPI entrypoint is `main.py`; configuration is in `config.py`. Frontend source is in `frontend/src/` using Vue 3 and Vite. Built frontend assets are emitted to `static/`. Tests are under `tests/`; generated runtime data appears in `logs/`, `backups/`, and `dumps/`.

## Build, Test, and Development Commands
Run commands from `../x_monitor/` unless noted.

- `python -m venv .venv`: create a local Python virtual environment.
- `source .venv/bin/activate`: activate the environment.
- `pip install -r requirements.txt`: install backend dependencies.
- `python main.py`: start the FastAPI app, defaulting to port `8777`.
- `pytest`: run the backend test suite in `tests/`.
- `cd frontend && npm install`: install frontend dependencies.
- `cd frontend && npm run dev`: start the Vite development server.
- `cd frontend && npm run build`: compile production frontend assets into `static/`.

## Coding Style & Naming Conventions
Use 4-space indentation for Python. Prefer `snake_case` for modules, functions, variables, and database helpers. Keep API routes in domain `routes.py` files and persistence logic in `storage.py` files. Use type hints for new backend interfaces. Vue components should use PascalCase filenames for reusable components, camelCase variables in scripts, and the existing Composition API style in `frontend/src/views/`.

## Testing Guidelines
Use `pytest` for backend tests. Name tests `test_<feature>.py` and place shared fixtures in `tests/conftest.py`. Add focused tests for scoring, storage, API routes, and copy-trading behavior when changing business logic. For frontend work, run `npm run build` before submitting to catch compile errors.

## Commit & Pull Request Guidelines
Recent commits use short, task-focused Chinese subjects such as `增加hyperliquid跟单功能` and `数据准确性修复`. Keep commits atomic and concise; a useful pattern is `<module>: <change>`, for example `hyperliquid: 修复book订阅状态`. Pull requests should describe scope, user-visible changes, configuration or schema changes, verification commands, and screenshots for UI updates.

## Security & Configuration Tips
Do not commit secrets, private keys, API tokens, webhook URLs, local databases, logs, dumps, or backups. Use environment variables and `.env` for local configuration, and document any new required variable in the project README.
