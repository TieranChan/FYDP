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


"""MYSQL/Database Ops, I should put this in another file"""
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
    
"""
Method used to fetch all folder (table) names dynamically
"""
def get_folders():
    """Fetch all folder (table) names dynamically."""
    if not config.mysql_username or not config.mysql_password:
        messagebox.showerror("Login Error", "MySQL credentials are not set. Please log in first.")
        return []  # Return an empty list if credentials are not set

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=config.mysql_username,
            password=config.mysql_password,
            database="museum"
        )
        cursor = connection.cursor()
        cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'museum'
        """)
        return [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching folders: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

"""
Method to fetch all titles from a specific folder
"""
def get_titles_in_folder(folder):
    """Fetch all titles from a specific folder (table)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=config.mysql_username,
            password=config.mysql_password,
            database="museum"
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT title FROM `{folder}`")
        return [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching titles from {folder}: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

"""
Dynamically fetches data for the title when you click login
"""
def fetch_data_for_title_dynamic(title):
    """Fetch detailed information (title, description, images, references, location, size, tags) for a given title from any table dynamically."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=config.mysql_username,
            password=config.mysql_password,
            database="museum"
        )
        cursor = connection.cursor()

        # Find all tables with a 'title' column
        cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'museum' AND COLUMN_NAME = 'title'
        """)
        tables = [row[0] for row in cursor.fetchall()]

        # Search for the title in each table
        for table in tables:
            query = f"""
            SELECT title, description, 
                   img_1, img_2, img_3, img_4, img_5, 
                   reference_1, reference_2, reference_3, reference_4, reference_6, reference_7, reference_8, reference_9, reference_10,
                   location, 
                   hight, width, length, 
                   tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7, tag_8, tag_9, tag_10, tag_11, tag_12, tag_13, tag_14, tag_15
            FROM `{table}`
            WHERE title = %s
            """
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            if result:
                # Build a detailed dictionary of the result
                columns = [
                    "title", "description",
                    "img_1", "img_2", "img_3", "img_4", "img_5",
                    "reference_1", "reference_2", "reference_3", "reference_4", "reference_6", "reference_7", "reference_8", "reference_9", "reference_10",
                    "location",
                    "hight", "width", "length",
                    "tag_1", "tag_2", "tag_3", "tag_4", "tag_5", "tag_6", "tag_7", "tag_8", "tag_9", "tag_10",
                    "tag_11", "tag_12", "tag_13", "tag_14", "tag_15"
                ]
                detailed_info = dict(zip(columns, result))
                return detailed_info, table  # Return detailed info and table name
        return None, None  # No matching title found
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching data: {err}")
        return None, None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

"""
Fetches all titles dynamically from all tables with a 'title' column NOT CURRENTLY BEING USED!1
"""
# def get_titles():
#     """Fetch all titles dynamically from all tables with a 'title' column."""
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user=config.mysql_username,
#             password=config.mysql_password,
#             database="museum"
#         )
#         cursor = connection.cursor()

#         # Find all tables with a 'title' column
#         cursor.execute("""
#         SELECT TABLE_NAME 
#         FROM INFORMATION_SCHEMA.COLUMNS 
#         WHERE TABLE_SCHEMA = 'museum' AND COLUMN_NAME = 'title'
#         """)
#         tables = [row[0] for row in cursor.fetchall()]

#         # Retrieve all titles from those tables
#         titles = []
#         for table in tables:
#             cursor.execute(f"SELECT title FROM `{table}`")
#             titles.extend([row[0] for row in cursor.fetchall()])

#         print(titles)

#         return titles
#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error fetching titles: {err}")
#         return []
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
