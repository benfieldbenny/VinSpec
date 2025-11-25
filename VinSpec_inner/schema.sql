
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS makes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make_id INTEGER NOT NULL REFERENCES makes(id),
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    trim TEXT,
    drivetrain TEXT,
    curb_weight_lbs INTEGER,
    horsepower INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(make_id, name, year, trim)
);

CREATE TABLE IF NOT EXISTS engine_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL REFERENCES models(id),
    engine_name TEXT,
    displacement_l TEXT,
    fuel_type TEXT,
    horsepower INTEGER,
    torque TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vehicle_dimensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL REFERENCES models(id),
    wheelbase_in INTEGER,
    length_in INTEGER,
    width_in INTEGER,
    height_in INTEGER,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    source_url TEXT,
    json_payload TEXT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
