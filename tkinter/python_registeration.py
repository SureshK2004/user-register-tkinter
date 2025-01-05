import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",#your root name
        password="suresh",#your password
        database="recipe" #your data basename
    )

# Save registration details to the database
def register_user():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()
    course = entry_course.get()
    gender = gender_var.get()
    location = location_var.get()

    if not name or not email or not password or not course or not gender or location == "Select Location":
        messagebox.showwarning("Validation Error", "All fields are required.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password, course, gender, location) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, password, course, gender, location)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Registration successful!")
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    gender_var.set("")
    location_var.set("Select Location")

# Create users table if not exists
def create_users_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            course VARCHAR(100),
            gender VARCHAR(10),
            location VARCHAR(100)
        )
    """)
    conn.close()

# Tkinter GUI setup
app = tk.Tk()
app.title("User Registration")
app.geometry("400x450")
app.config(bg='pink')

tk.Label(app, text="User Registration", font=("Arial", 16)).pack(pady=10)

tk.Label(app, text="Name:").pack(anchor="w", padx=20)
entry_name = tk.Entry(app, width=30,bg='lightgrey')
entry_name.pack(pady=5, padx=20)

tk.Label(app, text="Email:").pack(anchor="w", padx=20)
entry_email = tk.Entry(app, width=30)
entry_email.pack(pady=5, padx=20)

tk.Label(app, text="Password:").pack(anchor="w", padx=20)
entry_password = tk.Entry(app, width=30, show="*")
entry_password.pack(pady=5, padx=20)

tk.Label(app, text="Course Taken:").pack(anchor="w", padx=20)
entry_course = tk.Entry(app, width=30)
entry_course.pack(pady=5, padx=20)

tk.Label(app, text="Gender:").pack(anchor="w", padx=20)
gender_var = tk.StringVar()
tk.Radiobutton(app, text="Male", variable=gender_var, value="Male").pack(anchor="w", padx=30)
tk.Radiobutton(app, text="Female", variable=gender_var, value="Female").pack(anchor="w", padx=30)
tk.Radiobutton(app, text="Other", variable=gender_var, value="Other").pack(anchor="w", padx=30)

tk.Label(app, text="Location:").pack(anchor="w", padx=20)
location_var = tk.StringVar()
location_var.set("Select Location")
locations = ["Tamil Nadu", "Kerela", "Bangalore", "Delhi", "Hyderbad"]
tk.OptionMenu(app, location_var, *locations).pack(pady=5, padx=20)

tk.Button(app, text="Register", command=register_user).pack(pady=20)

# Initialize database table
create_users_table()

# Run the application
app.mainloop()
