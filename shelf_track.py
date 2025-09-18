"""
Imports the sqlite3 module to enable interaction with a local SQLite database.
Used throughout the program to connect to 'ebookstore.db', execute SQL
commands, and manage book inventory data persistently.
"""
import sqlite3

# Connect or create database
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create the book table
cursor.execute('''CREATE TABLE IF NOT EXISTS book(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    authorid INTEGER NOT NULL,
    qty INTEGER NOT NULL
)''')

# Create author table
cursor.execute('''CREATE TABLE IF NOT EXISTS author(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT NOT NULL
)''')

# Insert initial data
books = [
    (3001, "A Tale of Two Cities", 1290, 30),
    (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
    (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
    (3004, "The Lord of the Rings", 6380, 37),
    (3055, "Alice's Adventures in Wonderland", 5620, 12),
    (8207, "Verity", 3978, 18),
    (8208, "It Ends with Us", 3978, 22),
    (8210, "The Other Side of Midnight", 8211, 12),
    (8211, "Master of the Game", 8211, 20),
    (8209, "Reminders of Him", 3978, 15),
    (8212, "If Tomorrow Comes", 8211, 17)
]

cursor.executemany("INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)", books)

authors = [
    (1290, "Charles Dickens", "England"),
    (8937, "J.K. Rowling", "England"),
    (2356, "C.S. Lewis", "Ireland"),
    (6380, "J.R.R. Tolkien", "South Africa"),
    (5620, "Lewis Carroll", "England"),
    (3978, "Colleen Hoover", "America"),
    (8211, "Sidney Sheldon", "United States")

]

cursor.executemany("INSERT OR IGNORE INTO author VALUES (?, ?, ?)", authors)
conn.commit()
conn.close()


def menu():
    """
    Displays the main menu and handles user input.
    Routes the user to the appropriate function based on their choice.
    Continues until the user chooses to exit.
    """
    while True:
        print("\n Welcome to the Ebookstore Clerk System")
        print("1. Add a new book")
        print("2. Update book quantity")
        print("3. Delete a book")
        print("4. Search for a book")
        print("5. Search for an author")
        print("6. View all books")
        print("7. View details of all books")
        print("8. Exit")

        choice = input("Enter your choice(1-7): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_book()
        elif choice == "5":
            search_author()
        elif choice == "6":
            view_books()
        elif choice == "7":
            view_all_book_details()
        elif choice == "8":
            print(
                "Exiting the system. Thank you for using the Ebookstore Clerk "
                "System. Goodbye!"
            )
            break
        else:
            print("Invalid Choice. Please try again.")


def add_book():
    """
    Adds a new book to the database.
    Ensures the book ID is unique.
    Allows user to retry or return to main menu if duplicate ID is entered.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    while True:
        try:
            id = int(input("Enter book ID: "))

            # Check if book ID already exists
            cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
            if cursor.fetchone():
                print(f"Book ID {id} already exists.")
                choice = input("Type 'r' to retry or 'm' to return to main menu: ").strip().lower()
                if choice == 'm':
                    print("Returning to main menu...")
                    break
                elif choice == 'r':
                    continue
                else:
                    print("Invalid choice. Returning to main menu by default.")
                    break

            title = input("Enter book title: ")
            authorid = int(input("Enter author ID: "))
            qty = int(input("Enter quantity: "))

            cursor.execute(
                "INSERT INTO book VALUES (?, ?, ?, ?)",
                (id, title, authorid, qty)
            )
            db.commit()
            print("Book added successfully.")
            break

        except ValueError:
            print("Please enter valid numeric values.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        finally:
            db.commit()

    db.close()


def update_book():
    """
    Updates the quantity of an existing book and optionally the author's name
    and country. Prompts the user for book ID, new quantity, and author details.
    Applies updates to both 'book' and 'author' tables. Repeats prompt if book
    ID is invalid, or allows user to return to main menu.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    try:
        while True:
            user_input = input("Enter book ID to update (or type 'exit' to return): ")
            if user_input.lower() == 'exit':
                print("Returning to main menu...")
                return

            try:
                book_id = int(user_input)
            except ValueError:
                print("Invalid input. Please enter a numeric book ID.")
                continue

            cursor.execute("""
                SELECT book.qty, author.name, author.country, author.id
                FROM book
                JOIN author ON book.authorid = author.id
                WHERE book.id = ?
            """, (book_id,))
            result = cursor.fetchone()

            if not result:
                print("Book not found. Try again or type 'exit' to return.")
                continue

            # Valid book found — proceed with update
            current_qty, current_name, current_country, author_id = result
            print(f"Current quantity: {current_qty}")
            print(f"Author name: {current_name}")
            print(f"Author country: {current_country}")

            # Update quantity
            prompt_qty = "Enter new quantity (or press Enter to keep current): "
            new_qty = int(input(prompt_qty) or current_qty)
            cursor.execute(
                "UPDATE book SET qty = ? WHERE id = ?",
                (new_qty, book_id)
            )

            # Update author name
            prompt_name = "Enter new author name (or press Enter to keep current): "
            new_name = input(prompt_name).strip()
            if new_name:
                cursor.execute(
                    "UPDATE author SET name = ? WHERE id = ?",
                    (new_name, author_id)
                )

            # Update author country
            prompt_country = (
                "Enter new author country (or press Enter to keep current): "
            )
            new_country = input(prompt_country).strip()
            if new_country:
                cursor.execute(
                    "UPDATE author SET country = ? WHERE id = ?",
                    (new_country, author_id)
                )

            db.commit()
            print("***Book and author details updated successfully.***")
            break  # Exit loop after successful update

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


def delete_book():
    """
    Deletes a book from the database after confirming its existence and user approval.
    If the book ID doesn't exist, prompts to retry or return to main menu.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    while True:
        try:
            id = int(input("Enter book ID to delete: "))

            # Check if book exists
            cursor.execute("SELECT title, authorid, qty FROM book WHERE id = ?", (id,))
            book = cursor.fetchone()

            if not book:
                print(f"Book ID {id} not found.")
                choice = input("Would you like to retry (r) or return to main menu (m)? ").strip().lower()
                if choice == 'r':
                    continue
                elif choice == 'm':
                    print("Returning to main menu...")
                    break
                else:
                    print("Invalid choice. Returning to main menu by default.")
                    break

            title, authorid, qty = book

            # Get author name
            cursor.execute("SELECT name FROM author WHERE id = ?", (authorid,))
            author = cursor.fetchone()
            author_name = author[0] if author else "Unknown Author"

            print("\nBook Details:")
            print(f" - Title: {title}")
            print(f" - Author: {author_name}")
            print(f" - Quantity: {qty}")

            confirm = input("\nAre you sure you want to delete this book? (y/n): ").strip().lower()
            if confirm == 'y':
                cursor.execute("DELETE FROM book WHERE id = ?", (id,))
                db.commit()
                print("Book deleted successfully.")
            else:
                print("Deletion cancelled.")
            break

        except ValueError:
            print("Please enter a valid numeric book ID.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        finally:
            db.commit()

    db.close()


def search_book():
    """
    Searches for books by title.
    Prompts the user for a partial or full title.
    Displays all matching books from the 'book' table.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    try:
        title = input("Enter book title to search:")
        cursor.execute(
            "SELECT * FROM book WHERE title LIKE ?",
            ('%' + title + '%',)
        )
        results = cursor.fetchall()
        if results:
            for book in results:
                print(book)
        else:
            print("No matching books found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


def search_author():
    """
    Continuously prompts for an author ID until a valid one is entered.
    Displays the author's name and all books written by them.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()

    while True:
        try:
            authorid = int(input("Enter author ID to search: "))

            # Check if author exists
            cursor.execute("SELECT name FROM author WHERE id = ?", (authorid,))
            author = cursor.fetchone()

            if not author:
                print("Invalid author ID. Please try again.")
                continue

            # Fetch books by author
            cursor.execute("SELECT title, qty FROM book WHERE authorid = ?", (authorid,))
            books = cursor.fetchall()

            print(f"\n***Books by {author[0]}***:")
            if books:
                for title, qty in books:
                    print(f" - {title} (Qty: {qty})")
            else:
                print("No books found for this author.")
            break  # Exit loop after successful search

        except ValueError:
            print("Please enter a valid numeric author ID.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        finally:
            db.commit()

    db.close()


def view_books():
    """
    Displays all books currently in the database.
    Retrieves and prints all entries from the 'book' table.
    """
    db = sqlite3.connect('ebookstore.db')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM book")
        books = cursor.fetchall()
        for book in books:
            print(book)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


def view_all_book_details():
    """
    Display detailed information for all books in the database.

    Performs an inner join between the 'book' and 'author' tables to show each
    book's title, the author's name, and their country of origin. Results are
    printed in a formatted layout for easy readability.
    """
    conn = sqlite3.connect('ebookstore.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT book.title, author.name, author.country
        FROM book
        INNER JOIN author ON book.authorid = author.id
    ''')

    results = cursor.fetchall()
    conn.close()

    print("Details --------------------------------------------------")
    for title, name, country in results:
        print(f"Title: {title}")
        print(f"Author's Name: {name}")
        print(f"Author's Country: {country}")
        print("----------------------------------------------------")


# Run the menu
menu()
