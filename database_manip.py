"""
sqlite3 module:
Enables Python programs to connect to SQLite databases,
execute SQL queries, and manage data storage locally.
Ideal for lightweight, serverless database applications.
"""
import sqlite3

# Connect to the database (creates it if it doesn't exist)
db = sqlite3.connect('student.db')

# Create a cursor object
cursor = db.cursor()

# Ensure data does not duplicate
cursor.execute("DROP TABLE IF EXISTS python_programming")
db.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS python_programming(
               id INTEGER PRIMARY KEY,
               name TEXT,
               grade INTEGER
               )
               ''')

# Save changes
db.commit()

# Insert student records
cursor.execute(
    "INSERT OR IGNORE INTO python_programming (id, name, grade) "
    "VALUES (?, ?, ?)",
    (55, 'Carl Davis', 61)
)
cursor.execute(
    "INSERT OR IGNORE INTO python_programming (id, name, grade) "
    "VALUES (?, ?, ?)",
    (66, 'Dennis Fredrickson', 88)
)
cursor.execute(
    "INSERT OR IGNORE INTO python_programming (id, name, grade) "
    "VALUES (?, ?, ?)",
    (77, 'Jane Richards', 78)
)
cursor.execute(
    "INSERT OR IGNORE INTO python_programming (id, name, grade) "
    "VALUES (?, ?, ?)",
    (12, 'Peyton Sawyer', 45)
)
cursor.execute(
    "INSERT OR IGNORE INTO python_programming (id, name, grade) "
    "VALUES (?, ?, ?)",
    (2, 'Lucas Brooke', 99)
)
# Save changes
db.commit()

# Retrieve and print all records
cursor.execute("SELECT * FROM python_programming")
rows = cursor.fetchall()

# Display each record
for row in rows:
    print(row)

# Change Carl Davis grade to 65
cursor.execute("UPDATE python_programming SET grade = ? WHERE name = ?", (
    65, 'Carl Davis'))
db.commit()

# Delete row for Dennis Fredrickson
cursor.execute("DELETE FROM python_programming WHERE id = ?", (66,))
db.commit()

# Retrieve and display all remaining records
print("\nUpdated records (Dennis removed):")
cursor.execute("SELECT * FROM python_programming ORDER BY id")
for row in cursor.fetchall():
    print(row)

# Select and display records with grade between 50 and 80
cursor.execute(
    "SELECT * FROM python_programming WHERE grade BETWEEN 50 AND 80"
)
filtered_rows = cursor.fetchall()

print("\nStudents with grades between 50 and 80:")
for row in filtered_rows:
    print(row)

# Change and update the grades for all students with an ID > 50 to 80
cursor.execute("UPDATE python_programming SET grade = 80 WHERE id > 50")
db.commit()

# Retrieve and display updated records
print("\nUpdated grades student records:")
cursor.execute("SELECT * FROM python_programming WHERE id > 50")
updated_rows = cursor.fetchall()

for row in updated_rows:
    print(row)

# Print final table
print("\nFinal student records: ")
cursor.execute("SELECT * FROM python_programming ORDER BY id")
for row in cursor.fetchall():
    print(row)
