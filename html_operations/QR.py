import tkinter as tk
from tkinter import filedialog, Toplevel, Scrollbar, Listbox
from PIL import Image, ImageTk
from io import BytesIO
import segno
import webbrowser
from database_operations import Database
import mysql.connector
from tkinter import messagebox


# Global color scheme
BG_COLOR = "#E0F0FD"  # Light blue background
ENTRY_COLOR = "#BBDEFB"  # Lighter blue for input fields
BUTTON_COLOR = "#96CCF9"  # Button blue
TEXT_COLOR = "#0D47A1"  # Deep blue for text
FONT = ("Arial Rounded MT Bold", 14)  # Rounded font for all text
FONT_BOLD = ("Arial Rounded MT Bold", 16, "bold")  # Rounded font for headings

def generate_html_page(data, title):
    """Generate an HTML page dynamically from the fetched data."""
    def safe(value, default="No data provided"):
        return value if value else default

    # Extract specific fields if they exist
    description = safe(data.get("description", ""))
    location = safe(data.get("location", ""))
    size = f"H: {safe(data.get('hight'))}, W: {safe(data.get('width'))}, L: {safe(data.get('length'))}"
    image_titles = [safe(data.get(f"img_{i}")) for i in range(1, 6) if f"img_{i}" in data]
    biblio_ref = [safe(data.get(f"reference_{i}")) for i in range(1, 11) if f"reference_{i}" in data]
    tags = [safe(data.get(f"tag_{i}")) for i in range(1, 16) if f"tag_{i}" in data]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{safe(title)}</title>
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
        <h1>{safe(title)}</h1>
        <div class="section">
            <h2>Description</h2>
            <p>{safe(description)}</p>
        </div>
        <div class="section">
            <h2>Images</h2>
            {''.join(f'<div class="image"><p>{img}</p></div>' for img in image_titles) if image_titles else '<p>No images provided</p>'}
        </div>
        <div class="section">
            <h2>Bibliographic References</h2>
            <div class="biblio">
                <ul>
                    {''.join(f'<li>{ref}</li>' for ref in biblio_ref) if biblio_ref else '<li>No references provided</li>'}
                </ul>
            </div>
        </div>
        <div class="section">
            <h2>Location</h2>
            <p>{safe(location)}</p>
        </div>
        <div class="section">
            <h2>Size</h2>
            <p>{safe(size)}</p>
        </div>
        <div class="section">
            <h2>Tags</h2>
            <div class="tags">
                {', '.join(tags) if tags else 'No tags provided'}
            </div>
        </div>
    </body>
    </html>
    """

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

def open_save_HTML(title):
    """Open a window to prompt the user to save the HTML file."""
    third_window = Toplevel()
    third_window.title("Save HTML File")
    third_window.configure(bg=BG_COLOR)
    third_window.geometry("300x200")

    # Display the title
    tk.Label(
        third_window,
        text=f"Title: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Button to save the HTML file
    tk.Button(
        third_window,
        text="Save HTML File",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: [generate_html_page(title), third_window.destroy()]  # Generate HTML and close this window
    ).pack(pady=20)

def open_options_window(title, html_path):
    """Open a window with options after saving the HTML file."""
    options_window = Toplevel()
    options_window.title("Options - Next Steps")
    options_window.configure(bg=BG_COLOR)
    options_window.geometry("300x300")

    # Display the title
    tk.Label(
        options_window,
        text=f"Title: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Button to view the saved HTML file
    tk.Button(
        options_window,
        text="View HTML",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: webbrowser.open_new_tab(html_path)
    ).pack(pady=10)

    # Button to generate QR code
    tk.Button(
        options_window,
        text="Generate QR Code",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_qr_code_window(title, html_path)
    ).pack(pady=10)

    # Additional placeholder options
    tk.Button(
        options_window,
        text="Modify Entry",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: Database.open_window_4(title)
    ).pack(pady=10)

def open_qr_code_window(title, html_path):
    """Open a window to display the QR code with Save and Print options."""
    qr_window = Toplevel()
    qr_window.title("QR Code Viewer")
    qr_window.configure(bg=BG_COLOR)
    qr_window.geometry("400x550")

    # Display the title
    tk.Label(
        qr_window,
        text=f"Title: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Display the HTML path
    tk.Label(
        qr_window,
        text=f"HTML Path: {html_path}",
        font=FONT,
        fg=TEXT_COLOR,
        bg=BG_COLOR,
        wraplength=380,  # Ensure long paths wrap nicely
    ).pack(pady=10)

    # Generate and display the QR code
    qr_image = generate_qr(html_path)  # Generate QR code for the HTML path
    qr_label = tk.Label(qr_window, image=qr_image, bg=BG_COLOR)
    qr_label.image = qr_image  # Keep a reference to avoid garbage collection
    qr_label.pack(pady=20)

    # Save button
    tk.Button(
        qr_window,
        text="Save",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: save_qr_to_file(html_path)
    ).pack(pady=10)

    # Print button (placeholder for actual print functionality)
    tk.Button(
        qr_window,
        text="Print",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: print(f"Printing QR Code for {html_path}")  # Replace with actual print logic
    ).pack(pady=10)

def confirm_delete(title, parent_window):
    """Display a confirmation popup for deleting an entry."""
    confirm_window = Toplevel()
    confirm_window.title("Confirm Delete")
    confirm_window.configure(bg=BG_COLOR)
    confirm_window.geometry("300x150")

    # Confirmation message
    tk.Label(
        confirm_window,
        text=f"Are you sure you want to delete '{title}'?",
        font=FONT,
        fg=TEXT_COLOR,
        bg=BG_COLOR,
        wraplength=280,  # Ensure text wraps nicely
    ).pack(pady=10)

    # Yes button - Placeholder for actual delete logic
    tk.Button(
        confirm_window,
        text="Yes",
        font=FONT_BOLD,
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
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=confirm_window.destroy
    ).pack(side="right", padx=20, pady=10)

def delete_entry(title):
    """Delete the entry from the database or file system."""
    #TODO
    print(f"Entry '{title}' deleted.")  # Replace with actual delete logic

def open_select_window():
    root = tk.Tk()
    root.title("Select a Title")
    root.geometry("600x300")
    root.configure(bg="#E0F0FD")

    tk.Label(
        root,
        text="Select a title to view information:",
        font=("Arial Rounded MT Bold", 16),
        bg="#E0F0FD",
        fg="#0D47A1"
    ).pack(pady=10)

    # Frame for Listbox and Scrollbar
    frame = tk.Frame(root)
    frame.pack(pady=10)

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    title_listbox = Listbox(
        frame,
        width=50,
        height=10,
        yscrollcommand=scrollbar.set,
        font=("Arial", 12)
    )
    title_listbox.pack(side="left", fill="y")
    scrollbar.config(command=title_listbox.yview)

    # Populate the Listbox with titles
    titles = get_titles()
    for title in titles:
        title_listbox.insert("end", title)

def open_select_window():
    root = tk.Tk()
    root.title("Select a Title")
    root.geometry("600x300")
    root.configure(bg="#E0F0FD")

    tk.Label(
        root,
        text="Select a title to view information:",
        font=("Arial Rounded MT Bold", 16),
        bg="#E0F0FD",
        fg="#0D47A1"
    ).pack(pady=10)

    # Frame for Listbox and Scrollbar
    frame = tk.Frame(root)
    frame.pack(pady=10)

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    title_listbox = Listbox(
        frame,
        width=50,
        height=10,
        yscrollcommand=scrollbar.set,
        font=("Arial", 12)
    )
    title_listbox.pack(side="left", fill="y")
    scrollbar.config(command=title_listbox.yview)

    # Populate the Listbox with titles
    titles = get_titles()
    for title in titles:
        title_listbox.insert("end", title)

    # Define the on_search function inside open_select_window
    def on_search():
        selected_indices = title_listbox.curselection()
        if selected_indices:
            selected_title = title_listbox.get(selected_indices[0])
            data, table = fetch_data_for_title_dynamic(selected_title)
            if data:
                generate_html_page(data, selected_title)
            else:
                messagebox.showinfo("No Data Found", f"No data found for the title: {selected_title}")
        else:
            messagebox.showwarning("No Selection", "Please select a title.")

    # Search button
    tk.Button(
        root,
        text="Search",
        command=on_search,
        font=("Arial Rounded MT Bold", 14),
        bg="#96CCF9",
        fg="white"
    ).pack(pady=10)

    root.mainloop()


def open_what_to_do(title):
    """Open a window to display options for the selected title."""
    what_to_do_window = Toplevel()
    what_to_do_window.title("What to Do Next")
    what_to_do_window.configure(bg=BG_COLOR)
    what_to_do_window.geometry("300x250")

    # Display the title
    tk.Label(
        what_to_do_window,
        text=f"Title: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Modify/Delete Button
    tk.Button(
        what_to_do_window,
        text="Modify/Delete Entry",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_modify_delete_window(title)
    ).pack(pady=10)

    # Generate HTML/QR Button
    tk.Button(
        what_to_do_window,
        text="Generate HTML/QR",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_save_HTML(title)
    ).pack(pady=10)

def open_modify_delete_window(title):
    """Open a window for modifying or deleting the selected entry."""
    modify_delete_window = Toplevel()
    modify_delete_window.title("Modify/Delete Entry")
    modify_delete_window.configure(bg=BG_COLOR)
    modify_delete_window.geometry("300x200")

    # Display the title
    tk.Label(
        modify_delete_window,
        text=f"Modify/Delete: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Modify Button
    tk.Button(
        modify_delete_window,
        text="Modify Entry",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: Database.open_window_4(title)  # Call modify logic
    ).pack(pady=10)

    # Delete Button
    tk.Button(
        modify_delete_window,
        text="Delete Entry",
        font=FONT_BOLD,
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
            user=mysql_username,  # Use global variable from login window
            password=mysql_password,  # Use global variable from login window
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
    """Fetch all details for a given title from any table dynamically."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=mysql_username,  # Use global variable from login window
            password=mysql_password,  # Use global variable from login window
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
            query = f"SELECT * FROM `{table}` WHERE title = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            if result:
                # Retrieve column names for this table to map values
                cursor.execute(f"DESCRIBE `{table}`")
                columns = [col[0] for col in cursor.fetchall()]
                return dict(zip(columns, result)), table  # Return as a dictionary
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
    login_window.geometry("300x200")
    login_window.configure(bg=BG_COLOR)

    tk.Label(
        login_window,
        text="Enter MySQL Credentials",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Username input
    tk.Label(login_window, text="Username:", font=FONT, bg=BG_COLOR).pack(pady=5)
    username_entry = tk.Entry(login_window, font=FONT, bg=ENTRY_COLOR)
    username_entry.pack(pady=5)

    # Password input
    tk.Label(login_window, text="Password:", font=FONT, bg=BG_COLOR).pack(pady=5)
    password_entry = tk.Entry(login_window, font=FONT, bg=ENTRY_COLOR, show="*")
    password_entry.pack(pady=5)

    def submit_credentials():
        """Retrieve credentials and close the login window."""
        global mysql_username, mysql_password
        mysql_username = username_entry.get()
        mysql_password = password_entry.get()
        if not mysql_username or not mysql_password:
            messagebox.showwarning("Input Error", "Both username and password are required!")
        else:
            login_window.destroy()

    # Submit button
    tk.Button(
        login_window,
        text="Login",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        command=submit_credentials
    ).pack(pady=20)

    login_window.mainloop()


if __name__ == "__main__":
    mysql_username = None
    mysql_password = None
    mysql_login_window()  # Prompt for MySQL credentials
    open_select_window()  # Open the main window after login

