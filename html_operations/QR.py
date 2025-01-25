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
from generate_html import *
from database_fetch import *

"""
Contains all the functions related to generating the QR codes
"""
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




def create_folder(folder_name):
    print(f"I created a folder with name: {folder_name}")
    #todo
    #create said folder in MySQL


if __name__ == "__main__":
    mysql_login_window()  # Prompt for MySQL credentials
    #open_main_menu_window()

