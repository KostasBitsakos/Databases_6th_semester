import os
import json
import MySQLdb

DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_USER = os.getenv("MYSQL_USER", "demo_user")
DB_PASS = os.getenv("MYSQL_PASSWORD", "demo_pass")
DB_NAME = os.getenv("MYSQL_DB", "demo")

ARCHETYPE_VECTORS = {
    "pacey winger":              [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "creative playmaker":        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "target striker":            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "pressing forward":          [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "ball-winning midfielder":   [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "deep-lying playmaker":      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "overlapping full-back":     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "defensive full-back":       [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    "ball-playing centre-back":  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
    "physical centre-back":      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    "shot-stopping goalkeeper":  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    "sweeper keeper":            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
}

def pad_to_384(v):
    return v + [0.0] * (384 - len(v))

def connect():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASS,
        db=DB_NAME,
        charset="utf8mb4"
    )

def main():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id, archetype FROM player_reviews")
    rows = cur.fetchall()

    updated = 0
    for review_id, archetype in rows:
        if archetype not in ARCHETYPE_VECTORS:
            continue

        vec = pad_to_384(ARCHETYPE_VECTORS[archetype])
        vec_json = json.dumps(vec)

        cur.execute(
            "UPDATE player_reviews SET embedding = VEC_FromText(%s) WHERE id = %s",
            (vec_json, review_id)
        )
        updated += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Updated embeddings for {updated} reviews.")

if __name__ == "__main__":
    main()