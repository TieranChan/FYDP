from QR import *


def open_modify_delete_window(title):
    """Open a window for modifying or deleting the selected entry."""
    data, table = fetch_data_for_title_dynamic(title)
    description = data.get("description") if data else ""  # Default to an empty string if no description
    references = [
        data.get(f"reference_{i}") for i in range(1, 11)
        if data and data.get(f"reference_{i}")  # Only include non-empty references
    ]
    location = data.get("location") if data else ""


    # Extract size components
    length = data.get("length", "")  # Use the database column names
    width = data.get("width", "")
    height = data.get("hight", "")  # Assuming "hight" is the column name

    # Format size as a dictionary
    size = {"length": length, "width": width, "height": height}

    # Extract tags
    tags = [
        data.get(f"tag_{i}") for i in range(1, 16)
        if data and data.get(f"tag_{i}")  # Only include non-empty tags
    ]

    # Create Modify/Delete window
    modify_delete_window = Toplevel()
    modify_delete_window.title("Modify/Delete Entry")
    modify_delete_window.configure(bg=config.BG_COLOR)

    # Display the title
    tk.Label(
        modify_delete_window,
        text=f"Modify/Delete: {title}",
        font=config.FONT_BOLD,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR
    ).pack(pady=10)

    # Modify Button
    tk.Button(
        modify_delete_window,
        text="Modify Entry",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: [
            Database.send_to_db_window(title, description, references, location, size, tags),
            modify_delete_window.destroy(),
        ]  # Pass title, description, and references
    ).pack(pady=10)

    # Delete Button
    tk.Button(
        modify_delete_window,
        text="Delete Entry",
        font=config.FONT_BOLD,
        bg="red",
        fg="white",
        activebackground="#D32F2F",
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: confirm_delete(title, modify_delete_window)
    ).pack(pady=10)


def get_titles():
    """Fetch all titles dynamically from all tables with a 'title' column."""
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

        # Retrieve all titles from those tables
        titles = []
        for table in tables:
            cursor.execute(f"SELECT title FROM `{table}`")
            titles.extend([row[0] for row in cursor.fetchall()])

        return titles
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching titles: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


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

    def update_capslock_indicator(event):
        if event.state & 0x0002:  # Check if Caps Lock is active
            caps_lock_label.config(text="CAPS LOCK ON")
        else:
            caps_lock_label.config(text="")

    # Bind key events to update the Caps Lock indicator
    login_window.bind("<KeyPress>", update_capslock_indicator)

    def submit_credentials():
        """Retrieve credentials, validate them, and handle errors."""
        config.mysql_username = username_entry.get()
        config.mysql_password = password_entry.get()

        if not config.mysql_username or not config.mysql_password:
            messagebox.showwarning("Input Error", "Both username and password are required!")
            return  # Exit without proceeding further

        # Try to connect to MySQL with the provided credentials
        try:
            connection = mysql.connector.connect(
                host="localhost",  # Update this if the MySQL server is on another host
                user=config.mysql_username,
                password=config.mysql_password
            )
            connection.close()  # Close connection if successful
            login_window.destroy()  # Close the login window
            open_main_menu_window()  # Proceed to the main menu window
        except mysql.connector.Error as err:
            messagebox.showerror("Login Failed", f"Invalid credentials: {err}")
            # Do not close the login window or proceed to the main menu

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


def delete_entry(title):
    """Delete the entry from the database or file system."""

    print(f"Entry '{title}' deleted.")  # Log the action for debugging
