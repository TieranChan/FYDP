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
    """Generate an HTML page based on the provided data."""
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
        webbrowser.open_new_tab(file_path)  # Open the saved file in a browser


def open_html_page(title):
    """Generate and save an HTML file."""
    description = "Example description for the selected title."
    image_titles = ["image1.jpg", "image2.png"]
    biblio_ref = ["Reference 1", "Reference 2"]
    location = "Section A, Shelf 3"
    size = "Length: 10cm, Width: 5cm, Height: 3cm"
    tags = ["tag1", "tag2", "tag3"]

    generate_html_page(title, description, image_titles, biblio_ref, location, size, tags)


def generate_qr(data):
    """Generate a QR code and return it as a PhotoImage with fixed dimensions of 3cm x 3cm."""
    qr = segno.make(data)  # Create QR code
    buffer = BytesIO()
    qr.save(buffer, kind='png', scale=10)  # Generate high-quality QR code
    buffer.seek(0)
    image = Image.open(buffer)
    image = image.resize((113, 113), Image.Resampling.LANCZOS)  # Resize to 3cm x 3cm (113px at 96dpi)
    return ImageTk.PhotoImage(image)

def save_qr_to_file(data):
    """Prompt the user to save the QR code as a .png file."""
    qr = segno.make(data)  # Generate QR code
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], title="Save QR Code")
    if file_path:
        qr.save(file_path, kind='png', scale=10)
        print(f"QR Code saved to {file_path}")
def open_html_page(title):
    """Generate and save an HTML file."""
    description = "Example description for the selected title."
    image_titles = ["image1.jpg", "image2.png"]
    biblio_ref = ["Reference 1", "Reference 2"]
    location = "Section A, Shelf 3"
    size = "Length: 10cm, Width: 5cm, Height: 3cm"
    tags = ["tag1", "tag2", "tag3"]

    generate_html_page(title, description, image_titles, biblio_ref, location, size, tags)

def open_second_window(title):
    # Open the second window
    second_window = Toplevel()
    second_window.title("QR Code Generator - Step 2")
    second_window.configure(bg=BG_COLOR)
    second_window.geometry("300x400")  # Increased size to accommodate new buttons

    # Title display
    tk.Label(
        second_window,
        text=f"Title: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # HTML information display
    tk.Label(
        second_window,
        text="HTML: html.com",
        font=FONT,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=5)

    # Generate and display QR code
    qr_image = generate_qr(title)  # Generate QR code using the title
    qr_label = tk.Label(second_window, image=qr_image, bg=BG_COLOR)
    qr_label.image = qr_image  # Keep a reference to avoid garbage collection
    qr_label.pack(pady=10)

    # Print button (placeholder action)
    tk.Button(
        second_window,
        text="Print",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5
    ).pack(pady=10)

    # Button to see HTML and open the HTML example window
    tk.Button(
        second_window,
        text="Generate HTML",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_html_page(title)
    ).pack(pady=5)


def open_third_window(title):
    # Open the third window
    third_window = Toplevel()
    third_window.title("QR Code Generator - Step 3")
    third_window.configure(bg=BG_COLOR)
    third_window.geometry("300x300")

    # Title display
    tk.Label(
        third_window,
        text=f"Title: {title}",
        font=FONT_BOLD,
        fg=TEXT_COLOR,
        bg=BG_COLOR
    ).pack(pady=10)

    # Button to see HTML and open the HTML example window
    tk.Button(
        third_window,
        text="Generate HTML",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_html_page(title)  # Pass the title to generate HTML
    ).pack(pady=5)

    # Button to open window 2 when clicked
    tk.Button(
        third_window,
        text="Generate QR Code",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: open_second_window(title)
    ).pack(pady=5)

    # Delete button that triggers the confirmation popup
    tk.Button(
        third_window,
        text="Delete",
        font=FONT_BOLD,
        bg="red",
        fg="white",
        activebackground="#D32F2F",
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: confirm_delete(title)
    ).pack(pady=5)

    # Modify button
    tk.Button(
        third_window,
        text="Modify",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: Database.open_window_4(title)  # Call to open_window_4 from Database module
    ).pack(pady=5)


def confirm_delete(title):
    # Create a confirmation popup window
    confirm_window = Toplevel()
    confirm_window.title("Confirm Delete")
    confirm_window.configure(bg=BG_COLOR)
    confirm_window.geometry("300x150")

    # Confirmation message
    tk.Label(
        confirm_window,
        text=f"Are you sure you want to delete '{title}' from the database?",
        font=FONT,
        fg=TEXT_COLOR,
        bg=BG_COLOR,
        wraplength=280,  # Ensure text wraps nicely
    ).pack(pady=10)

    # Yes button - Placeholder command for delete action
    tk.Button(
        confirm_window,
        text="Yes",
        font=FONT_BOLD,
        bg=BUTTON_COLOR,
        fg="white",
        activebackground=TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: [print(f"{title} deleted"), confirm_window.destroy()]  # Replace with actual delete logic
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

def main():
    # Create the main window
    root = tk.Tk()
    root.title("QR Code Generator - Step 1")
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
            open_third_window(selected_title)
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

if __name__ == "__main__":
    main()
