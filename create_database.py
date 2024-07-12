import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('table_tennis_stats.db')
cursor = conn.cursor()

# Create Players table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Players (
    id INTEGER PRIMARY KEY,
    given_name TEXT NOT NULL
)
''')

# Create Matches table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Matches (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    opponent_id INTEGER,
    match_date TEXT,
    match_number INTEGER,
    best_of INTEGER,
    FOREIGN KEY (player_id) REFERENCES Players (id),
    FOREIGN KEY (opponent_id) REFERENCES Players (id)
)
''')

# Create Games table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Games (
    id INTEGER PRIMARY KEY,
    match_id INTEGER,
    game_number INTEGER,
    initial_server_id INTEGER,
    player_score INTEGER,
    opponent_score INTEGER,
    FOREIGN KEY (match_id) REFERENCES Matches (id),
    FOREIGN KEY (initial_server_id) REFERENCES Players (id)
)
''')

# Create ServeTypes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ServeTypes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# Create OpeningShotTypes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OpeningShotTypes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

# Create Points table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Points (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    point_number INTEGER,
    server_id INTEGER,
    serve_type_id INTEGER,
    receiver_id INTEGER,
    opening_shot_player_id INTEGER,
    opening_shot_type_id INTEGER,
    winner_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES Games (id),
    FOREIGN KEY (server_id) REFERENCES Players (id),
    FOREIGN KEY (serve_type_id) REFERENCES ServeTypes (id),
    FOREIGN KEY (receiver_id) REFERENCES Players (id),
    FOREIGN KEY (opening_shot_player_id) REFERENCES Players (id),
    FOREIGN KEY (opening_shot_type_id) REFERENCES OpeningShotTypes (id),
    FOREIGN KEY (winner_id) REFERENCES Players (id)
)
''')

# Insert default serve types
serve_types = [
    "Pendulum", "Backhand", "Tomohawk", "Punch", "Reverse pendulum", "Fault"
]
cursor.executemany("INSERT INTO ServeTypes (name) VALUES (?)", [(st,) for st in serve_types])

# Insert default opening shot types
opening_shot_types = [
    "Forehand loop", "Backhand loop", "Forehand flick", "Backhand flick",
    "Forehand loop error", "Backhand loop error", "Forehand flick error",
    "Backhand flick error", "Push Error"
]
cursor.executemany("INSERT INTO OpeningShotTypes (name) VALUES (?)", [(ost,) for ost in opening_shot_types])

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully!")