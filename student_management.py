from tkinter import ttk

import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade TEXT
        )
    """)
    conn.commit()
    conn.close()

# ---------- CRUD ----------
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()
    if not name or not age or not grade:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()
    clear_entries()
    view_students()
    messagebox.showinfo("Success", "Student added successfully!")

def view_students():
    student_table.delete(*student_table.get_children())
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        student_table.insert("", "end", values=row)

def delete_student():
    selected = student_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a student to delete")
        return
    student_id = student_table.item(selected[0])["values"][0]
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    clear_entries()
    view_students()
    messagebox.showinfo("Deleted", "Student deleted successfully!")

def update_student():
    selected = student_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Select a student to update")
        return
    student_id = student_table.item(selected[0])["values"][0]
    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()
    if not name or not age or not grade:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, age=?, grade=? WHERE id=?", (name, age, grade, student_id))
    conn.commit()
    conn.close()
    clear_entries()
    view_students()
    messagebox.showinfo("Updated", "Student updated successfully!")

def select_student(event):
    selected = student_table.selection()
    if selected:
        values = student_table.item(selected[0])["values"]
        clear_entries()
        name_entry.insert(0, values[1])
        age_entry.insert(0, values[2])
        grade_entry.insert(0, values[3])

def clear_entries():
    name_entry.delete(0, ctk.END)
    age_entry.delete(0, ctk.END)
    grade_entry.delete(0, ctk.END)

# ---------- UI ----------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Student Management System")
root.geometry("800x500")

# Title
title = ctk.CTkLabel(root, text="Student Management System", font=("Roboto", 24, "bold"))
title.pack(pady=10)

# Input Frame
input_frame = ctk.CTkFrame(root, corner_radius=10)
input_frame.pack(pady=10, padx=20, fill="x")

name_label = ctk.CTkLabel(input_frame, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
age_label = ctk.CTkLabel(input_frame, text="Age:")
age_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
grade_label = ctk.CTkLabel(input_frame, text="Grade:")
grade_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

name_entry = ctk.CTkEntry(input_frame, width=200)
age_entry = ctk.CTkEntry(input_frame, width=200)
grade_entry = ctk.CTkEntry(input_frame, width=200)

name_entry.grid(row=0, column=1, padx=10, pady=5)
age_entry.grid(row=1, column=1, padx=10, pady=5)
grade_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons Frame
button_frame = ctk.CTkFrame(root, corner_radius=10)
button_frame.pack(pady=10, padx=20, fill="x")

add_btn = ctk.CTkButton(button_frame, text="Add Student", command=add_student)
add_btn.grid(row=0, column=0, padx=10, pady=10)
update_btn = ctk.CTkButton(button_frame, text="Update Student", command=update_student)
update_btn.grid(row=0, column=1, padx=10, pady=10)
delete_btn = ctk.CTkButton(button_frame, text="Delete Student", command=delete_student)
delete_btn.grid(row=0, column=2, padx=10, pady=10)
clear_btn = ctk.CTkButton(button_frame, text="Clear Fields", command=clear_entries)
clear_btn.grid(row=0, column=3, padx=10, pady=10)

# Table Frame
table_frame = ctk.CTkFrame(root, corner_radius=10)
table_frame.pack(pady=10, padx=20, fill="both", expand=True)

columns = ("ID", "Name", "Age", "Grade")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=150, anchor="center")
student_table.pack(fill="both", expand=True)

# Optional scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=student_table.yview)
student_table.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")


student_table.bind("<ButtonRelease-1>", select_student)

# Initialize DB and load students
init_db()
view_students()

root.mainloop()
