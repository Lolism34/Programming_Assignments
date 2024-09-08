import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Database setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    genre TEXT,
    description TEXT,
    type TEXT,
    availability INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    contact_info TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS card_holders (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    contact_info TEXT,
    borrowed_items TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS checkout (
    id INTEGER PRIMARY KEY,
    media_id INTEGER NOT NULL,
    card_holder_id INTEGER NOT NULL,
    checkout_date TEXT,
    due_date TEXT,
    return_status TEXT,
    FOREIGN KEY (media_id) REFERENCES media(id),
    FOREIGN KEY (card_holder_id) REFERENCES card_holders(id)
)
''')

conn.commit()


# Class Definitions
class Media:
    def __init__(self, title, author, genre, description, media_type):
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description
        self.media_type = media_type
        self.availability = 1  # 1 means available, 0 means checked out

    def save_to_db(self):
        cursor.execute('''
        INSERT INTO media (title, author, genre, description, type, availability)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.title, self.author, self.genre, self.description, self.media_type, self.availability))
        conn.commit()

    @staticmethod
    def search_media(search_term):
        cursor.execute('''
        SELECT * FROM media WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? OR description LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        return cursor.fetchall()

    @staticmethod
    def update_availability(media_id, availability):
        cursor.execute('UPDATE media SET availability = ? WHERE id = ?', (availability, media_id))
        conn.commit()


class Staff:
    def __init__(self, name, position, contact_info):
        self.name = name
        self.position = position
        self.contact_info = contact_info

    def save_to_db(self):
        cursor.execute('''
        INSERT INTO staff (name, position, contact_info)
        VALUES (?, ?, ?)
        ''', (self.name, self.position, self.contact_info))
        conn.commit()

    @staticmethod
    def search_staff(search_term):
        cursor.execute('''
        SELECT * FROM staff WHERE name LIKE ? OR position LIKE ? OR id LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        return cursor.fetchall()


class Checkout:
    def __init__(self, media_id, card_holder_id, due_date):
        self.media_id = media_id
        self.card_holder_id = card_holder_id
        self.checkout_date = datetime.now().strftime("%Y-%m-%d")
        self.due_date = due_date
        self.return_status = 'Not Returned'

    def save_to_db(self):
        cursor.execute('''
        INSERT INTO checkout (media_id, card_holder_id, checkout_date, due_date, return_status)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.media_id, self.card_holder_id, self.checkout_date, self.due_date, self.return_status))
        conn.commit()

    @staticmethod
    def return_media(checkout_id):
        cursor.execute('UPDATE checkout SET return_status = "Returned" WHERE id = ?', (checkout_id,))
        conn.commit()
        # Update media availability
        cursor.execute('SELECT media_id FROM checkout WHERE id = ?', (checkout_id,))
        media_id = cursor.fetchone()[0]
        Media.update_availability(media_id, 1)


# GUI Setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("500x600")

# Functions to interact with the database
def add_media():
    title = simpledialog.askstring("Input", "Enter title:")
    author = simpledialog.askstring("Input", "Enter author:")
    genre = simpledialog.askstring("Input", "Enter genre:")
    description = simpledialog.askstring("Input", "Enter description:")
    media_type = simpledialog.askstring("Input", "Enter type (book/DVD/etc.):")
    
    if title and author:
        media = Media(title, author, genre, description, media_type)
        media.save_to_db()
        messagebox.showinfo("Success", "Media added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


def search_media():
    search_term = simpledialog.askstring("Search", "Enter search term:")
    if search_term:
        results = Media.search_media(search_term)
        result_text = ""
        for result in results:
            result_text += f"ID: {result[0]}, Title: {result[1]}, Author: {result[2]}, Available: {'Yes' if result[6] == 1 else 'No'}\n"
        
        if result_text:
            messagebox.showinfo("Search Results", result_text)
        else:
            messagebox.showinfo("No Results", "No media found.")


def checkout_media():
    media_id = simpledialog.askinteger("Input", "Enter Media ID:")
    card_holder_id = simpledialog.askinteger("Input", "Enter Card Holder ID:")
    due_date = simpledialog.askstring("Input", "Enter Due Date (YYYY-MM-DD):")
    
    if media_id and card_holder_id and due_date:
        checkout = Checkout(media_id, card_holder_id, due_date)
        checkout.save_to_db()
        Media.update_availability(media_id, 0)
        messagebox.showinfo("Success", "Media checked out successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


def return_media():
    checkout_id = simpledialog.askinteger("Input", "Enter Checkout ID:")
    
    if checkout_id:
        Checkout.return_media(checkout_id)
        messagebox.showinfo("Success", "Media returned successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


def add_staff():
    name = simpledialog.askstring("Input", "Enter staff name:")
    position = simpledialog.askstring("Input", "Enter job title:")
    contact_info = simpledialog.askstring("Input", "Enter contact information:")
    
    if name and position:
        staff = Staff(name, position, contact_info)
        staff.save_to_db()
        messagebox.showinfo("Success", "Staff added successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


def search_staff():
    search_term = simpledialog.askstring("Search Staff", "Enter name, ID, or position:")
    if search_term:
        results = Staff.search_staff(search_term)
        result_text = ""
        for result in results:
            result_text += f"ID: {result[0]}, Name: {result[1]}, Position: {result[2]}\n"
        
        if result_text:
            messagebox.showinfo("Staff Search Results", result_text)
        else:
            messagebox.showinfo("No Results", "No staff found.")


# GUI Elements
label = tk.Label(root, text="Library Management System", font=("Helvetica", 16))
label.pack(pady=20)

add_media_button = tk.Button(root, text="Add Media", command=add_media, width=30)
add_media_button.pack(pady=10)

search_media_button = tk.Button(root, text="Search Media", command=search_media, width=30)
search_media_button.pack(pady=10)

checkout_media_button = tk.Button(root, text="Checkout Media", command=checkout_media, width=30)
checkout_media_button.pack(pady=10)

return_media_button = tk.Button(root, text="Return Media", command=return_media, width=30)
return_media_button.pack(pady=10)

add_staff_button = tk.Button(root, text="Add Staff", command=add_staff, width=30)
add_staff_button.pack(pady=10)

search_staff_button = tk.Button(root, text="Search Staff", command=search_staff, width=30)
search_staff_button.pack(pady=10)

# Run the GUI
root.mainloop()
