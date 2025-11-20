import sqlite3
import os

# Path to your database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, 'warchest_secure.db')

def migrate_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Add monthly_budget column to user table
        print("Adding monthly_budget column to user table...")
        cursor.execute("ALTER TABLE user ADD COLUMN monthly_budget REAL DEFAULT 0")
        print("✓ monthly_budget column added")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ monthly_budget column already exists")
        else:
            print(f"Error adding monthly_budget: {e}")
    
    try:
        # Create budget table
        print("\nCreating budget table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category VARCHAR(50) NOT NULL,
                limit_amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        ''')
        print("✓ Budget table created")
    except sqlite3.OperationalError as e:
        print(f"Error creating budget table: {e}")
    
    try:
        # Create goal table
        print("\nCreating goal table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(100) NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                deadline DATETIME,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        ''')
        print("✓ Goal table created")
    except sqlite3.OperationalError as e:
        print(f"Error creating goal table: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database migration completed successfully!")
    print("You can now restart your Flask app.")

if __name__ == '__main__':
    print("=== War Chest Database Migration ===\n")
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Database file not found: {DB_FILE}")
        print("The database will be created automatically when you run app.py")
    else:
        print(f"Database found: {DB_FILE}")
        migrate_database()