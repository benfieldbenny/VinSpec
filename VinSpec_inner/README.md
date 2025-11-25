# Vehicle AI Project (POC)
This package contains a proof-of-concept pipeline for ingesting vehicle data (make, model, year, trims, engine options, dimensions, horsepower, drivetrain, curb weight) and serving it via a minimal API.

**What's included**
- `vehicles_poc.db` - SQLite database filled with sample records (Camry, Civic).
- `schema.sql` - SQL schema used for the database.
- `ingest.py` - Example ingestion script that shows how to upsert records into the SQLite DB. Currently uses a mock fetch function; replace with real API/scraper code.
- `app.py` - Minimal FastAPI app to query the database and return models/specs.
- `agent.py` - Simple orchestrator/agent that runs the ingestion periodically and can be extended to call external APIs or LLMs.
- `requirements.txt` - Python dependencies.
- `run_local.sh` - Convenience script to run the app and agent (for development).

## Quick start (local)
1. Install Python 3.10+
2. Create a venv: `python -m venv venv && source venv/bin/activate` (use `venv\Scripts\activate` on Windows)
3. Install deps: `pip install -r requirements.txt`
4. Run the API: `uvicorn app:app --reload --port 8000`
5. In a separate terminal, run the agent (simple loop): `python agent.py`

## Notes
- This is a POC. The ingestion logic is intentionally minimal and does not call external APIs by default (so you can run without keys).
- When you want it to pull live data, edit `ingest.py`'s `fetch_vehicle_data()` to call actual APIs or scraping logic and respect terms of service.
- Backup the DB: `cp vehicles_poc.db vehicles_poc.db.bak`
