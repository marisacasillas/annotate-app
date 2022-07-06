#!/usr/bin/env python3
from annotate.database import create_database
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.wm_title("Annotate App Launcher")
root.geometry("400x200")
warning_text_input = tk.StringVar()
success_text_input = tk.StringVar()

def new_db():
    if os.path.exists('var/database.db'): 
        warning_text_input.set("Warning! A database file already exists.\nRemove this file before trying to create a new database.")
        success_text_input.set("")
        return
    root.withdraw()
    csv = filedialog.askopenfilename(initialdir = os.getcwd(),
                    filetypes = [('CSV files', '*.csv'),])
    create_database(csv)
    os.system('python app.py')

def existing_db():
    if not os.path.exists('var/database.db'): 
        warning_text_input.set("Warning! There is no existing database file.")
        success_text_input.set("")
        return
    root.withdraw()
    os.system('python app.py')

def rm_db():
    if not os.path.exists('var/database.db'): 
        warning_text_input.set("Warning! There is no existing database file.")
        success_text_input.set("")
        return
    os.system('rm var/database.db')
    warning_text_input.set("")
    success_text_input.set("Success!")

def export_csv():
    if not os.path.exists('var/database.db'): 
        warning_text_input.set("Warning! There is no existing database file.")
        success_text_input.set("")
        return   
    os.system('./db2csv.py')
    warning_text_input.set("")
    success_text_input.set("Success!")


welcome_text = tk.Label(root, text="Welcome to the Annotate App!\nSelect from the below options to begin\nannotating or manage your existing annotations.", fg="blue")
welcome_text.pack()

tk.Button(root, text='Create new database', command=new_db).pack()
tk.Button(root, text='Continue existing database', command=existing_db).pack()
tk.Button(root, text='Remove existing database', command=rm_db).pack()
tk.Button(root, text='Export codes to CSV', command=export_csv).pack()

warning_text = tk.Label(root, textvariable=warning_text_input, fg="red")
warning_text.pack()

success_text = tk.Label(root, textvariable=success_text_input, fg="green")
success_text.pack()

root.mainloop()