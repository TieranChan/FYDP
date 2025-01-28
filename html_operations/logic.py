import tkinter as tk
from tkinter import filedialog, Toplevel, Scrollbar, Listbox
from PIL import Image, ImageTk
from io import BytesIO
import segno
import webbrowser
import sys
sys.path.append(r"C:\Users\Tiera\FYDP\database_operations")
import Database
import mysql.connector
from tkinter import messagebox
sys.path.append(r"C:\Users\Tiera\FYDP")
import config

"""
This file is used to decouple logic functions from TKINTER calls
"""


"""Helper function to extract specific fields if they exist"""
def safe(value):
    return value if value else None

"""
Function used to extract fields from a table given data
"""
def extract_fields(data):
    # Extract specific fields if they exist
    description = safe(data.get("description"))
    location = safe(data.get("location"))
    size_components = [
        f"H: {safe(data.get('hight'))}",
        f"W: {safe(data.get('width'))}",
        f"L: {safe(data.get('length'))}"
    ]
    size = ", ".join(filter(None, size_components))
    image_titles = [safe(data.get(f"img_{i}")) for i in range(1, 6) if f"img_{i}" in data and data.get(f"img_{i}")]
    biblio_ref = [safe(data.get(f"reference_{i}")) for i in range(1, 11) if f"reference_{i}" in data and data.get(f"reference_{i}")]
    tags = [safe(data.get(f"tag_{i}")) for i in range(1, 16) if f"tag_{i}" in data and data.get(f"tag_{i}")]

    return description, location, size, image_titles, biblio_ref, tags, size_components


"""Refactored Functions"""
"""
Validate_and_connect handles MYSQL logic and validation given a username and password
"""
def validate_and_connect(username, password):
    """Validate credentials and attempt to connect to MYSQL"""
    if not username or not password:
        return "Both username and password are required!"
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Update this if the MySQL server is on another host
            user=username,
            password=password
        )
        connection.close()  # Close connection if successful
        return "Success"
    except mysql.connector.Error as err:
        messagebox.showerror("Login Failed", f"Invalid credentials: {err}")
        # Do not close the login window or proceed to the main menu
        return f"Login Failed: {err}"

"""submit_credentials() deals only with GUI-specific behaviour"""
def submit_credentials():
    """Retrieve credentials, validate them, and handle errors."""
    config.mysql_username = username_entry.get()
    config.mysql_password = password_entry.get()

    result=validate_and_connect(config.mysql_username, config.mysql_password)

    if result == "Success":
        messagebox.showinfo("Login Successful", "You are logged in!")
        login_window.destroy()  # Close the login window
        open_main_menu_window()  # Proceed to the main menu window

    elif "Both username and password are required!" in result:
        messagebox.showwarning("Input Error", result)

    else:
        messagebox.showerror("Login Failed", result)