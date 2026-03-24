import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'data.db'

def sync_data():
    """Synchronize local data with remote source"""
    try:
        # Load remote data
        response = requests.get('https://api.example.com/data')
        remote_data = response.json()
    except requests.exceptions.RequestException:
        # Fetch from local cache if remote is unavailable
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT data, last_sync FROM cache WHERE id = 1')
        row = c.fetchone()
        if row:
            remote_data = json.loads(row[0])
            last_sync = datetime.fromisoformat(row[1])
            if datetime.now() - last_sync < timedelta(hours=1):
                print('Using cached data from last hour')
                return remote_data
        raise Exception('Unable to fetch data')

    # Store remote data in local cache
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cache (id INTEGER PRIMARY KEY, data TEXT, last_sync TEXT)')
    c.execute('DELETE FROM cache WHERE id = 1')
    c.execute('INSERT INTO cache (id, data, last_sync) VALUES (1, ?, ?)', (json.dumps(remote_data), datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return remote_data

def main():
    if not os.path.exists(DB_PATH):
        # Initialize local cache
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('CREATE TABLE cache (id INTEGER PRIMARY KEY, data TEXT, last_sync TEXT)')
        conn.commit()
        conn.close()

    data = sync_data()
    print(data)

if __name__ == '__main__':
    main()