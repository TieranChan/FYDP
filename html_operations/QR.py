import tkinter as tk
from tkinter import Toplevel, filedialog
from PIL import Image, ImageTk
from io import BytesIO
import segno
import webbrowser
from database_operations import Database

# Global color scheme
BG_COLOR = "#E0F0FD"  # Light blue background
ENTRY_COLOR = "#BBDEFB"  # Lighter blue for input fields
BUTTON_COLOR = "#96CCF9"  # Button blue
TEXT_COLOR = "#0D47A1"  # Deep blue for text
FONT = ("Arial Rounded MT Bold", 14)  # Rounded font for all text
FONT_BOLD = ("Arial Rounded MT Bold", 16, "bold")  # Rounded font for headings

def generate_html_page(title, description="", image_titles=None, biblio_ref=None, location="", size="", tags=None):
    """Generate an HTML page and transition to the options window."""
    if image_titles is None:
        image_titles = []
    if biblio_ref is None:
        biblio_ref = []
    if tags is None:
        tags = []

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
        <div class="section">
            <h2>Description</h2>
            <p>{description}</p>
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
            <p>{location if location else 'No location provided'}</p>
        </div>
        <div class="section">
            <h2>Size</h2>
            <p>{size if size else 'No size provided'}</p>
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

    # Prompt the user to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")],
                                             title="Save HTML Page")
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
    # Create the main window
    root = tk.Tk()
    root.title("Select title")
    root.configure(bg=BG_COLOR)
    root.geometry("600x250")

    # Prompt label
    tk.Label(
        root,
        text="Select a title that you need information on:",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=5)

    # Frame for the listbox and scrollbar
    list_frame = tk.Frame(root)
    list_frame.pack(pady=5)

    # Scrollbar for the listbox
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    # Listbox for selecting titles
    title_listbox = tk.Listbox(
        list_frame,
        font=FONT,
        bg=ENTRY_COLOR,
        fg=TEXT_COLOR,
        selectbackground=BUTTON_COLOR,
        selectforeground="white",
        height=5,  # Display 5 items at a time
        yscrollcommand=scrollbar.set
    )
    titles = [f"Title {i}" for i in range(1, 21)]  # Example with more titles for scrolling
    for title in titles:
        title_listbox.insert("end", title)
    title_listbox.pack(side="left")

    # Configure the scrollbar to scroll the listbox
    scrollbar.config(command=title_listbox.yview)

    # Search button
    def on_search():
        selected_indices = title_listbox.curselection()
        if selected_indices:
            selected_title = title_listbox.get(selected_indices[0])
            open_what_to_do(selected_title)
        else:
            print("No title selected")  # Placeholder for no selection

    tk.Button(
        root,
        text="Search",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=on_search
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


if __name__ == "__main__":
    open_select_window()
