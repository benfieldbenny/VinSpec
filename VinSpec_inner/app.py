"""Minimal FastAPI app to query the SQLite POC database."""
from fastapi import FastAPI, HTTPException
import sqlite3, json
from pydantic import BaseModel
from typing import List, Optional

DB = 'vehicles_poc.db'
app = FastAPI(title='Vehicle POC API')

class ModelOut(BaseModel):
    id: int
    make: str
    name: str
    year: int
    trim: Optional[str]
    drivetrain: Optional[str]
    curb_weight_lbs: Optional[int]
    horsepower: Optional[int]

@app.get('/models', response_model=List[ModelOut])
def list_models(make: Optional[str] = None, year: Optional[int] = None):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    q = 'SELECT m.id, mk.name, m.name, m.year, m.trim, m.drivetrain, m.curb_weight_lbs, m.horsepower FROM models m JOIN makes mk ON m.make_id=mk.id'
    clauses = []
    params = []
    if make:
        clauses.append('mk.name = ?'); params.append(make)
    if year:
        clauses.append('m.year = ?'); params.append(year)
    if clauses:
        q += ' WHERE ' + ' AND '.join(clauses)
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({'id': r[0], 'make': r[1], 'name': r[2], 'year': r[3], 'trim': r[4], 'drivetrain': r[5], 'curb_weight_lbs': r[6], 'horsepower': r[7]})
    return results

@app.get('/models/{model_id}')
def get_model(model_id: int):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT m.id, mk.name, m.name, m.year, m.trim, m.drivetrain, m.curb_weight_lbs, m.horsepower FROM models m JOIN makes mk ON m.make_id=mk.id WHERE m.id=?', (model_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail='Model not found')
    cur.execute('SELECT engine_name, displacement_l, fuel_type, horsepower, torque FROM engine_options WHERE model_id=?', (model_id,))
    engines = [{'engine_name': e[0], 'displacement_l': e[1], 'fuel_type': e[2], 'horsepower': e[3], 'torque': e[4]} for e in cur.fetchall()]
    cur.execute('SELECT wheelbase_in, length_in, width_in, height_in FROM vehicle_dimensions WHERE model_id=?', (model_id,))
    dims = cur.fetchone()
    conn.close()
    return {
        'id': row[0],
        'make': row[1],
        'name': row[2],
        'year': row[3],
        'trim': row[4],
        'drivetrain': row[5],
        'curb_weight_lbs': row[6],
        'horsepower': row[7],
        'engine_options': engines,
        'dimensions': {'wheelbase_in': dims[0] if dims else None, 'length_in': dims[1] if dims else None, 'width_in': dims[2] if dims else None, 'height_in': dims[3] if dims else None}
    }
