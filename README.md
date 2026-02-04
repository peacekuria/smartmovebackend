SmartMove Backend
==================

Flask backend for SmartMove.

Deploying to Railway
--------------------

These steps will get the app deployed on Railway (https://railway.app). The repo includes a `Procfile` and `runtime.txt` so Railway's Python buildpack can detect and start the app.

1. Create a Railway project and connect your GitHub repo
	- Go to Railway and create a new project.
	- Connect your GitHub repository (this repo).

2. Build & Start command
	- This repo includes a `Procfile` with the web process:
	  - `web: gunicorn run:app --bind 0.0.0.0:$PORT --workers 3 --log-file -`
	- Railway will detect Python from `runtime.txt` and `requirements.txt` and run the start command from the `Procfile`.

3. Required environment variables
	- Open your Railway project > Settings > Variables and set at minimum:
	  - `SECRET_KEY` — a secure random string for Flask.
	  - `DATABASE_URL` — a Postgres connection string if you provision a database (Railway Postgres plugin provides this automatically).
	- Optional/other env vars your instance needs (e.g., `FLASK_ENV`, external API keys).

4. Provision a database (optional but recommended)
	- In Railway, add the Postgres plugin to your project.
	- Railway will populate `DATABASE_URL` automatically; confirm it is present in Environment Variables.

5. Run database migrations / initialization
		- This repo has a `migrations/` folder. Use the included programmatic migration helper to apply migrations that use the Flask app's DB URL:
			- Locally: `python scripts/run_migrations.py`
			- On Railway (recommended via the project console): `railway run python scripts/run_migrations.py`
		- The script uses Alembic's programmatic API and reads `SQLALCHEMY_DATABASE_URI` from the Flask app config. If you prefer the raw Alembic CLI, you can also run:
			- `railway run alembic upgrade head`
		- If you have other initialization scripts, you can run them similarly:
			- `railway run python scripts/init_db.py` or `railway run python scripts/seed_data.py`.
		- You can run those commands from the Railway CLI or the project console in the web UI.

6. Check logs and verify
	- Use the Railway UI to view logs and confirm the `gunicorn` process started and is listening on the `$PORT` Railway provides.

Local testing
-------------

1. Create a virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set environment variables locally (example):

```bash
export SECRET_KEY="my-local-secret"
export DATABASE_URL="sqlite:///app.db"
```

3. Run locally:

```bash
gunicorn run:app --bind 0.0.0.0:8000
```

Notes and troubleshooting
-------------------------
- Railway exposes the port in `$PORT`. The `Procfile` uses this variable so the service will bind correctly.
- If you prefer Docker, there's an existing `Dockerfile` and `docker-compose.yml` in the repo; you can instruct Railway to deploy from Docker instead of buildpack-based deploy.
- If migrations or initialization scripts are empty or not configured, confirm which management commands this repo expects and add them to `scripts/` or update the README accordingly.

If you'd like, I can also add a small Railway-specific helper (like a `railway.json` or documented `railway` CLI commands) or wire up a sample `alembic` command here—tell me which you'd prefer.
