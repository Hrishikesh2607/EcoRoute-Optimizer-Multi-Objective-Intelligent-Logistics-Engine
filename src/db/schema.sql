CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    segment_name VARCHAR(100),
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326)
);

CREATE TABLE segments (
    id SERIAL PRIMARY KEY,
    source_node INTEGER REFERENCES nodes(id),
    target_node INTEGER REFERENCES nodes(id),
    is_rush_hour BOOLEAN NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    avg_speed DOUBLE PRECISION,
    avg_duration_min DOUBLE PRECISION,
    avg_fuel_cost DOUBLE PRECISION,
    congestion_factor DOUBLE PRECISION,
    pred_duration DOUBLE PRECISION,
    pred_fare DOUBLE PRECISION,
    UNIQUE(source_node, target_node, is_rush_hour, is_weekend)
);

CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    start_node INTEGER REFERENCES nodes(id),
    end_node INTEGER REFERENCES nodes(id),
    timestamp TIMESTAMP DEFAULT NOW(),
    weight_time FLOAT,
    weight_cost FLOAT,
    optimized_cost DOUBLE PRECISION,
    optimized_duration DOUBLE PRECISION,
    actual_cost DOUBLE PRECISION,
    route_path INTEGER[]
);

CREATE INDEX idx_nodes_geom ON nodes USING GIST (geom);
CREATE INDEX idx_segments_source ON segments (source_node);
CREATE INDEX idx_segments_target ON segments (target_node);