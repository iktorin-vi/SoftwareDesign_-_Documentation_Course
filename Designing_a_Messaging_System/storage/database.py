import sqlite3

def get_connection():
    conn = sqlite3.connect('messenger.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Таблиці згідно з Minimal Data Model
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        conversationId INTEGER,
                        senderId INTEGER, 
                        text TEXT, 
                        status TEXT, -- 'sent', 'delivered', 'read'
                        createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                        deliveredAt DATETIME,
                        readAt DATETIME)''')
    conn.commit()
    conn.close()