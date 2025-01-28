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
from QR import *


"""
File that contains everything to do with html from generation logic to the GUI
"""


def safe(value):
    return value if value else None
    
"""Helper function to extract specific fields if they exist"""
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
