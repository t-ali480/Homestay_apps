import sqlite3

# Define the database name
db_name = "personal_expenses.db"

# Connect to the database
conn = sqlite3.connect(db_name)

cur = conn.cursor()

# Create a table if it doesn't exist
cur.execute(""" CREATE TABLE IF NOT EXISTS {table_name}                
                (id INTEGER PRIMARY KEY,
                Date DATE,
                description TEXT,
                category TEXT,
                price REAL)""".format(table_name=db_name[:-3]))

# Commit changes and close the connection
conn.commit()
conn.close()