"""Example ingestion script for the SQLite POC.
Replace fetch_vehicle_data() with real API calls or scraping logic.
"""
import sqlite3, json, time
from datetime import datetime

DB = 'vehicles_poc.db'

def fetch_vehicle_data():
    # Mock function: return a list of vehicle dicts.
    # Replace with API calls or scraping as needed.
    return [
        {
            'make': 'Toyota',
            'country': 'Japan',
            'model': 'Corolla',
            'year': 2023,
            'trim': 'LE',
            'drivetrain': 'FWD',
            'curb_weight_lbs': 2840,
            'horsepower': 139,
            'engine_options': [
                {'engine_name': '1.8L I4', 'displacement_l': '1.8L', 'fuel_type': 'Gasoline', 'horsepower': 139, 'torque': '126 lb-ft'}
            ],
            'dimensions': {'wheelbase_in': 106, 'length_in': 182, 'width_in': 70, 'height_in': 57},
            'source': 'mock_api',
            'source_url': 'https://example.com/corolla-2023'
        }
    ]

def upsert(conn, item):
    cur = conn.cursor()
    # upsert make
    cur.execute('INSERT OR IGNORE INTO makes (name, country) VALUES (?,?)', (item['make'], item.get('country')))
    cur.execute('SELECT id FROM makes WHERE name=?', (item['make'],))
    make_id = cur.fetchone()[0]

    # upsert model
    cur.execute('''INSERT OR IGNORE INTO models (make_id,name,year,trim,drivetrain,curb_weight_lbs,horsepower)
                   VALUES (?,?,?,?,?,?,?)''',
                (make_id, item['model'], item['year'], item.get('trim'), item.get('drivetrain'), item.get('curb_weight_lbs'), item.get('horsepower')))
    cur.execute('SELECT id FROM models WHERE make_id=? AND name=? AND year=? AND trim=?', (make_id, item['model'], item['year'], item.get('trim')))
    model_id = cur.fetchone()[0]

    # engine options
    for e in item.get('engine_options', []):
        cur.execute('''INSERT INTO engine_options (model_id, engine_name, displacement_l, fuel_type, horsepower, torque)
                       VALUES (?,?,?,?,?,?)''', (model_id, e.get('engine_name'), e.get('displacement_l'), e.get('fuel_type'), e.get('horsepower'), e.get('torque')))

    # dimensions
    d = item.get('dimensions', {})
    if d:
        cur.execute('''INSERT INTO vehicle_dimensions (model_id, wheelbase_in, length_in, width_in, height_in)
                       VALUES (?,?,?,?,?)''', (model_id, d.get('wheelbase_in'), d.get('length_in'), d.get('width_in'), d.get('height_in')))

    # raw snapshot
    cur.execute('INSERT INTO raw_snapshots (source, source_url, json_payload) VALUES (?,?,?)',
                (item.get('source'), item.get('source_url'), json.dumps(item)))

    conn.commit()

def run_once():
    conn = sqlite3.connect(DB)
    data = fetch_vehicle_data()
    for item in data:
        upsert(conn, item)
    conn.close()

if __name__ == '__main__':
    # simple loop - run every 15 minutes in production you may want a proper scheduler
    while True:
        try:
            print('Fetching data...', datetime.utcnow().isoformat())
            run_once()
            print('Done. Sleeping 900s...')
        except Exception as e:
            print('Error during ingestion:', e)
        time.sleep(900)
