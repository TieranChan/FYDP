import sys
"""For DEBUGGING"""
sys.path.append(r'C:/Users/Tiera/FYDP')
import database_operations
import tkinter as tk
from tkinter import filedialog, Toplevel, Scrollbar, Listbox
from PIL import Image, ImageTk
from io import BytesIO
import segno
import webbrowser
from database_operations import Database
import mysql.connector
from tkinter import messagebox
import config

"""
File that contains everything to do with logging in to the MYSQL database and launching the program
"""

"""Refactored Functions"""
"""Validate_and_connect handles MYSQL logic and validation"""
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


def mysql_login_window():
    """Create a login window for MySQL credentials."""
    login_window = tk.Tk()
    login_window.title("MySQL Login")
    login_window.configure(bg=config.BG_COLOR)

    tk.Label(
        login_window,
        text="Enter MySQL Credentials",
        font=config.FONT_BOLD,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR
    ).pack(pady=10)

    # Username input
    tk.Label(login_window, text="Username:", font=config.FONT, bg=config.BG_COLOR).pack(pady=5)

    username_entry = tk.Entry(
        login_window,
        font=config.FONT,
        bg=config.ENTRY_COLOR,
        fg=config.TEXT_COLOR,
        width=20  # Predefined length for username box
    )
    username_entry.pack(pady=5)

    # Password input frame
    tk.Label(login_window, text="Password:", font=config.FONT, bg=config.BG_COLOR).pack(pady=5)

    password_frame = tk.Frame(login_window, bg=config.BG_COLOR)
    password_frame.pack(pady=5)

    # Password entry
    password_entry = tk.Entry(
        password_frame,
        font=config.FONT,
        bg=config.ENTRY_COLOR,
        fg=config.TEXT_COLOR,
        show="*",
        width=17  # Slightly shorter to make space for the eye button
    )
    password_entry.pack(side="left")

    # Eye button to toggle password visibility
    def toggle_password():
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
            eye_button.config(text="🔒")
        else:
            password_entry.config(show="*")
            eye_button.config(text="👁")

    eye_button = tk.Button(
        password_frame,
        text="👁",
        font=("Arial", 12),
        bg=config.ENTRY_COLOR,
        fg=config.TEXT_COLOR,
        relief="flat",
        command=toggle_password,
        width=2,  # Predefined button width
        height=1  # Predefined button height
    )
    eye_button.pack(side="right", padx=5)

    # Caps Lock Indicator
    caps_lock_label = tk.Label(login_window, text="", font=config.FONT, bg=config.BG_COLOR, fg="red")
    caps_lock_label.pack(pady=5)

    """Refactored Functions"""
    """Validate_and_connect handles MYSQL logic and validation"""
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
            login_window.destroy()  # Close the login window
            open_main_menu_window()  # Proceed to the main menu window

        elif "Both username and password are required!" in result:
            messagebox.showwarning("Input Error", result)

        else:
            messagebox.showerror("Login Failed", result)


    def update_capslock_indicator(event):
        if event.state & 0x0002:  # Check if Caps Lock is active
            caps_lock_label.config(text="CAPS LOCK ON")
        else:
            caps_lock_label.config(text="")

    # Bind key events to update the Caps Lock indicator
    login_window.bind("<KeyPress>", update_capslock_indicator)



    
    # Bind Enter key to the submit_credentials function
    login_window.bind("<Return>", lambda event: submit_credentials())
    # Submit button
    tk.Button(
        login_window,
        text="Login",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        command=submit_credentials
    ).pack(pady=20)

    login_window.mainloop()


def open_main_menu_window():

    """Open a window with options to add a new entry or access an existing one."""
    # Create the window
    main_menu_window = tk.Tk()
    main_menu_window.title("Main Menu - Database Operations")
    main_menu_window.configure(bg=config.BG_COLOR)
    main_menu_window.geometry("400x300")

    # Title label
    tk.Label(
        main_menu_window,
        text="What would you like to do?",
        font=config.FONT_BOLD,
        bg=config.BG_COLOR,
        fg=config.TEXT_COLOR
    ).pack(pady=20)

    # Button to add a new entry
    def open_new_entry():
        main_menu_window.destroy()
        Database.make_new_entry()  # Call the function for creating a new entry

    tk.Button(
        main_menu_window,
        text="Add New Entry",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=open_new_entry
    ).pack(pady=20)

    # Button to access an existing entry
    def access_existing_entry():
        main_menu_window.destroy()
        open_select_window()  # Call the function to access existing entries

    tk.Button(
        main_menu_window,
        text="Access Existing Entry",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=access_existing_entry
    ).pack(pady=20)

    main_menu_window.mainloop()