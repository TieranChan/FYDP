import tkinter as tk
from tkinter import filedialog, Toplevel, Scrollbar, Listbox
from PIL import Image, ImageTk
from io import BytesIO
import segno
import webbrowser
import sys
sys.path.append(r"C:\Users\Tiera\FYDP\database_operations")

#from database_operations import Database
#from database_operations.Database_existing import Database_existing
import importlib.util
import sys
sys.path.append(r"C:\Users\Tiera\FYDP")

spec = importlib.util.spec_from_file_location("database_existing", r"C:\Users\Tiera\FYDP\database_operations\Database_existing.py")
database_existing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database_existing)
import mysql.connector
from tkinter import messagebox
sys.path.append(r"C:\Users\Tiera\FYDP")
import config


from logic import *


def on_closing():
    """Function to exit the application when the window is closed."""
    sys.exit()  # Forcefully exits the program


def generate_html_page(data, title):
    """Generate an HTML page dynamically from the fetched data."""
   
    description,location, size, image_titles, biblio_ref, tags, size_components=extract_fields(data)
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

    third_window.protocol("WM_DELETE_WINDOW", on_closing)

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

    # Back button
    back_button = tk.Button(
        third_window,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            third_window.destroy(),
            open_what_to_do(data, title)
        )
    )
    back_button.pack(pady=10)



def open_options_window(title, html_path):
    """Open a window with options after saving the HTML file."""
    options_window = Toplevel()
    options_window.title("Options - Next Steps")
    options_window.configure(bg=config.BG_COLOR)

    options_window.protocol("WM_DELETE_WINDOW", on_closing)

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
        command=lambda: (open_qr_code_window(title, html_path), options_window.destroy())
    ).pack(pady=10)


def open_qr_code_window(title, html_path):
    """Open a window to display the QR code with Save and Print options."""
    qr_window = Toplevel()
    qr_window.title("QR Code Viewer")
    qr_window.configure(bg=config.BG_COLOR)

    qr_window.protocol("WM_DELETE_WINDOW", on_closing)

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

    # Back button
    back_button = tk.Button(
        qr_window,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            qr_window.destroy(),
            open_options_window(title, html_path)
        )
    )
    back_button.pack(pady=10)


def confirm_delete(title, parent_window):
    """Display a confirmation popup for deleting an entry."""
    confirm_window = Toplevel()
    confirm_window.title("Confirm Delete")
    confirm_window.configure(bg=config.BG_COLOR)

    confirm_window.protocol("WM_DELETE_WINDOW", on_closing)

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
        command=lambda: (delete_entry(title), confirm_window.destroy(), parent_window.destroy(), open_select_window())  # Close both windows
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
        command=lambda : (confirm_window.destroy(), parent_window.destroy(), open_modify_delete_window(title))
    ).pack(side="right", padx=20, pady=10)


def open_select_window():
    root = tk.Tk()
    root.title("Select Folder and Title")
    root.configure(bg=config.BG_COLOR)

    root.protocol("WM_DELETE_WINDOW", on_closing)

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
                root.withdraw()
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

    # Back button
    back_button = tk.Button(
        root,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            root.destroy(),
            open_main_menu_window()
        )
    )
    back_button.pack(pady=10)

    root.mainloop()



def open_what_to_do(data, title):
    """Open a window to display options for the selected title."""
    what_to_do_window = Toplevel()
    what_to_do_window.title("What to Do Next")
    what_to_do_window.configure(bg=config.BG_COLOR)

    what_to_do_window.protocol("WM_DELETE_WINDOW", on_closing)

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
        command=lambda: (open_modify_delete_window(title), what_to_do_window.destroy())
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
        command=lambda: (open_save_html(data, title), what_to_do_window.destroy())   # Pass both arguments
    ).pack(pady=10)

    # Back button
    back_button = tk.Button(
        what_to_do_window,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            what_to_do_window.destroy(),
            open_select_window()
        )
    )
    back_button.pack(pady=10)


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

    modify_delete_window.protocol("WM_DELETE_WINDOW", on_closing)

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
            Database_existing.send_to_db_window(title, description, references, location, size, tags),
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
        command=lambda: (confirm_delete(title, modify_delete_window), modify_delete_window.destroy())
    ).pack(pady=10)

    # Back button
    back_button = tk.Button(
        modify_delete_window,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            modify_delete_window.destroy(),
            open_what_to_do(data, title)
        )
    )
    back_button.pack(pady=10)


def mysql_login_window():
    """Create a login window for MySQL credentials."""
    login_window = tk.Tk()
    login_window.title("MySQL Login")
    login_window.configure(bg=config.BG_COLOR)

    login_window.protocol("WM_DELETE_WINDOW", on_closing)

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

    main_menu_window.protocol("WM_DELETE_WINDOW", on_closing)

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


def create_folder(folder_name):
    print(f"I created a folder with name: {folder_name}")
    #todo
    #create said folder in MySQL


if __name__ == "__main__":
    #mysql_login_window()  # Prompt for MySQL credentials
    open_main_menu_window()

