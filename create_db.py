import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if __name__ == '__main__':
    try:
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='password'")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT datname FROM pg_database;")
        dbs = [row[0] for row in cursor.fetchall()]
        
        if 'po_db' not in dbs:
            cursor.execute('CREATE DATABASE po_db;')
            print("Database created successfully")
        else:
            print("Database already exists")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
