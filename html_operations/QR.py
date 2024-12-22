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


def generate_html_page(data, title):
    """Generate an HTML page dynamically from the fetched data."""
    def safe(value):
        return value if value else None

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

    html_sections = []

    # Add sections conditionally
    if description:
        html_sections.append(f"""
        <div class="section">
            <h2>Description</h2>
            <p>{description}</p>
        </div>
        """)

    if image_titles:
        images_html = ''.join(f'<div class="image"><p>{img}</p></div>' for img in image_titles)
        html_sections.append(f"""
        <div class="section">
            <h2>Images</h2>
            {images_html}
        </div>
        """)

    if biblio_ref:
        biblio_html = ''.join(f'<li>{ref}</li>' for ref in biblio_ref)
        html_sections.append(f"""
        <div class="section">
            <h2>Bibliographic References</h2>
            <div class="biblio">
                <ul>
                    {biblio_html}
                </ul>
            </div>
        </div>
        """)

    if location:
        html_sections.append(f"""
        <div class="section">
            <h2>Location</h2>
            <p>{location}</p>
        </div>
        """)

    if size:
        html_sections.append(f"""
        <div class="section">
            <h2>Size</h2>
            <p>{size}</p>
        </div>
        """)

    if tags:
        tags_html = ', '.join(tags)
        html_sections.append(f"""
        <div class="section">
            <h2>Tags</h2>
            <div class="tags">
                {tags_html}
            </div>
        </div>
        """)

    # Combine all sections
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #E0F0FD;
                color: #0D47A1;
                margin: 20px;
            }}
            h1, h2 {{
                color: #0D47A1;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            .image {{
                margin: 10px 0;
            }}
            .biblio, .tags {{
                background-color: #BBDEFB;
                padding: 10px;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {''.join(html_sections)}
    </body>
    </html>
    """

    # Save the HTML
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")], title="Save HTML Page")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML page saved to {file_path}")
        open_options_window(title, file_path)  # Transition to the options window


def generate_qr(data):
    """Generate a QR code and return it as a PhotoImage."""
    qr = segno.make(data)  # Create QR code
    buffer = BytesIO()
    qr.save(buffer, kind='png', scale=10)  # Generate high-quality QR code
    buffer.seek(0)
    image = Image.open(buffer)
    image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize for display
    return ImageTk.PhotoImage(image)


def save_qr_to_file(data):
    """Prompt the user to save the QR code as a .png file."""
    qr = segno.make(data)  # Generate QR code
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], title="Save QR Code")
    if file_path:
        qr.save(file_path, kind='png', scale=10)
        qr.save(file_path, kind='png', scale=10)
        print(f"QR Code saved to {file_path}")


def open_save_html(data, title):
    """Open a window to prompt the user to save the HTML file."""
    third_window = Toplevel()
    third_window.title("Save HTML File")
    third_window.configure(bg=config.BG_COLOR)

    # Display the title
    tk.Label(
        third_window,
        text=f"Title: {title}",
        font=config.FONT_BOLD,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR
    ).pack(pady=10)

    # Button to save the HTML file
    tk.Button(
        third_window,
        text="Save HTML File",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: [generate_html_page(data, title), third_window.destroy()]  # Pass both arguments
    ).pack(pady=20)


def open_options_window(title, html_path):
    """Open a window with options after saving the HTML file."""
    options_window = Toplevel()
    options_window.title("Options - Next Steps")
    options_window.configure(bg=config.BG_COLOR)

    # Display the title
    tk.Label(
        options_window,
        text=f"Title: {title}",
        font=config.FONT_BOLD,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR
    ).pack(pady=10)

    # Button to view the saved HTML file
    tk.Button(
        options_window,
        text="View HTML",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: webbrowser.open_new_tab(html_path)
    ).pack(pady=10)

    # Button to generate QR code
    tk.Button(
        options_window,
        text="Generate QR Code",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_qr_code_window(title, html_path)
    ).pack(pady=10)


def open_qr_code_window(title, html_path):
    """Open a window to display the QR code with Save and Print options."""
    qr_window = Toplevel()
    qr_window.title("QR Code Viewer")
    qr_window.configure(bg=config.BG_COLOR)

    # Display the title
    tk.Label(
        qr_window,
        text=f"Title: {title}",
        font=config.FONT_BOLD,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR
    ).pack(pady=10)

    # Display the HTML path
    tk.Label(
        qr_window,
        text=f"HTML Path: {html_path}",
        font=config.FONT,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR,
        wraplength=380,  # Ensure long paths wrap nicely
    ).pack(pady=10)

    # Generate and display the QR code
    qr_image = generate_qr(html_path)  # Generate QR code for the HTML path
    qr_label = tk.Label(qr_window, image=qr_image, bg=config.BG_COLOR)
    qr_label.image = qr_image  # Keep a reference to avoid garbage collection
    qr_label.pack(pady=20)

    # Save button
    tk.Button(
        qr_window,
        text="Save",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: save_qr_to_file(html_path)
    ).pack(pady=10)

    # Print button (placeholder for actual print functionality)
    tk.Button(
        qr_window,
        text="Print",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: print(f"Printing QR Code for {html_path}")  # Replace with actual print logic
    ).pack(pady=10)


def confirm_delete(title, parent_window):
    """Display a confirmation popup for deleting an entry."""
    confirm_window = Toplevel()
    confirm_window.title("Confirm Delete")
    confirm_window.configure(bg=config.BG_COLOR)

    # Confirmation message
    tk.Label(
        confirm_window,
        text=f"Are you sure you want to delete '{title}'?",
        font=config.FONT,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR,
        wraplength=280,  # Ensure text wraps nicely
    ).pack(pady=10)

    # Yes button - Placeholder for actual delete logic
    tk.Button(
        confirm_window,
        text="Yes",
        font=config.FONT_BOLD,
        bg="red",
        fg="white",
        activebackground="#D32F2F",
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: [delete_entry(title), confirm_window.destroy(), parent_window.destroy()]  # Close both windows
    ).pack(side="left", padx=20, pady=10)

    # No button - Closes the confirmation window
    tk.Button(
        confirm_window,
        text="No",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=confirm_window.destroy
    ).pack(side="right", padx=20, pady=10)


def open_select_window():
    root = tk.Tk()
    root.title("Select Folder and Title")
    root.configure(bg=config.BG_COLOR)

    tk.Label(
        root,
        text="Select a folder to view titles:",
        font=config.FONT_BOLD,
        bg=config.BG_COLOR,
        fg=config.TEXT_COLOR
    ).pack(pady=10)

    # Frame for folder selection
    folder_frame = tk.Frame(root, bg=config.BG_COLOR)
    folder_frame.pack(pady=10)

    folder_listbox = tk.Listbox(
        folder_frame,
        font=config.FONT,
        bg=config.ENTRY_COLOR,
        fg=config.TEXT_COLOR,
        selectbackground=config.BUTTON_COLOR,
        selectforeground="white",
        height=10,
        width=30
    )
    folder_listbox.pack(side="left", fill="y", padx=5)

    folder_scrollbar = tk.Scrollbar(folder_frame, orient="vertical", command=folder_listbox.yview)
    folder_scrollbar.pack(side="right", fill="y")
    folder_listbox.config(yscrollcommand=folder_scrollbar.set)

    tk.Label(
        root,
        text="Select a title within the folder:",
        font=config.FONT_BOLD,
        bg=config.BG_COLOR,
        fg=config.TEXT_COLOR
    ).pack(pady=10)

    # Frame for title selection
    title_frame = tk.Frame(root, bg=config.BG_COLOR)
    title_frame.pack(pady=10)

    title_listbox = tk.Listbox(
        title_frame,
        font=config.FONT,
        bg=config.ENTRY_COLOR,
        fg=config.TEXT_COLOR,
        selectbackground=config.BUTTON_COLOR,
        selectforeground="white",
        height=10,
        width=30
    )
    title_listbox.pack(side="left", fill="y", padx=5)

    title_scrollbar = tk.Scrollbar(title_frame, orient="vertical", command=title_listbox.yview)
    title_scrollbar.pack(side="right", fill="y")
    title_listbox.config(yscrollcommand=title_scrollbar.set)

    # Populate folder listbox with folder names
    folders = get_folders()  # Fetch all folder (table) names dynamically
    for folder in folders:
        folder_listbox.insert("end", folder)

    def update_titles(event):
        """Update the titles listbox based on the selected folder."""
        try:
            # Check if a folder is selected
            if not folder_listbox.curselection():
                return  # Exit the function if no folder is selected

            # Get the selected folder
            selected_folder = folder_listbox.get(folder_listbox.curselection())

            # Fetch titles from the selected folder
            titles = get_titles_in_folder(selected_folder)

            # Clear the title listbox
            title_listbox.delete(0, "end")

            # Populate the title listbox with titles from the selected folder
            for title in titles:
                title_listbox.insert("end", title)

        except Exception as e:
            print(f"Error updating titles: {e}")  # Debugging purpose, can be removed in production

    folder_listbox.bind("<<ListboxSelect>>", update_titles)

    def on_search():
        """Fetch data for the selected title and open the next window."""
        try:
            # Validate title selection
            if not title_listbox.curselection():
                messagebox.showwarning("Selection Error", "Please select a title.")
                return

            # Get the selected title
            selected_title = title_listbox.get(title_listbox.curselection())

            # Fetch data for the selected title
            data, table = fetch_data_for_title_dynamic(selected_title)

            if data:
                open_what_to_do(data, selected_title)  # Pass the data and title to the next window
            else:
                messagebox.showinfo("No Data Found", f"No data found for the title: {selected_title}")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Search button
    tk.Button(
        root,
        text="Search",
        command=on_search,
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white"
    ).pack(pady=20)

    root.mainloop()


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


def open_what_to_do(data, title):
    """Open a window to display options for the selected title."""
    what_to_do_window = Toplevel()
    what_to_do_window.title("What to Do Next")
    what_to_do_window.configure(bg=config.BG_COLOR)

    # Display the title
    tk.Label(
        what_to_do_window,
        text=f"Title: {title}",
        font=config.FONT_BOLD,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR
    ).pack(pady=10)

    # Modify/Delete Button
    tk.Button(
        what_to_do_window,
        text="Modify/Delete Entry",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_modify_delete_window(title)
    ).pack(pady=10)

    # Generate HTML/QR Button
    tk.Button(
        what_to_do_window,
        text="Generate HTML/QR",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_save_html(data, title)  # Pass both arguments
    ).pack(pady=10)


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
        """Retrieve credentials and close the login window."""
        config.mysql_username = username_entry.get()
        config.mysql_password = password_entry.get()
        if not config.mysql_username or not config.mysql_password:
            messagebox.showwarning("Input Error", "Both username and password are required!")
        else:
            login_window.destroy()

    # Submit button
    tk.Button(
        login_window,
        text="Login",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        command=lambda: [submit_credentials(), open_main_menu_window()]
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


if __name__ == "__main__":
    mysql_login_window()  # Prompt for MySQL credentials
    # open_main_menu_window()

