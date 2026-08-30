import sqlite3, os

db_path = os.path.join(os.getcwd(), 'db.sqlite3')
print('DB exists:', os.path.exists(db_path), db_path)
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print('tables:', tables)
    table_names = [t[0] for t in tables]
    if 'movie_movie' in table_names:
        cur.execute('SELECT count(*) FROM movie_movie')
        print('movie_movie count:', cur.fetchone()[0])
        cur.execute('PRAGMA table_info(movie_movie)')
        print('schema:', cur.fetchall())
    conn.close()
