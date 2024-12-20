import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, Frame, BOTH, LEFT, RIGHT, Y, Canvas
from html_operations import QR

#global color scheme
BG_COLOR = "#E0F0FD"  # Light blue background
ENTRY_COLOR = "#BBDEFB"  # Lighter blue for input fields
BUTTON_COLOR = "#96CCF9"  # Button blue
BUTTON_TEXT = "white"
TEXT_COLOR = "#0D47A1"  # Deep blue for text
FONT = ("Arial Rounded MT Bold", 14)  # Rounded font for all text
FONT_BOLD = ("Arial Rounded MT Bold", 16, "bold")  # Rounded font for headings
FONT_TEXT = ("Arial Rounded MT Bold", 10)

def open_window_6(title, description, image_titles, biblio_ref, location, size, tags, window_4):
    """Creates Window 6: Display title, description, image titles, and send button."""
    # Create Window 6
    window_6 = tk.Tk()
    window_6.title("Window 6 - Display Collected Data")
    window_6.configure(bg=BG_COLOR)

    main_frame = Frame(window_6, bg=BG_COLOR)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame, bg=BG_COLOR)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, bg=BG_COLOR)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Center everything by using pack with anchor and expand options
    def create_centered_label(text, font=FONT, bold=False, fg=TEXT_COLOR, bg=BG_COLOR):
        label_font = (font[0], font[1], "bold") if bold else font
        label = tk.Label(second_frame, text=text, font=label_font, fg=fg, bg=BG_COLOR)
        label.pack(pady=10, anchor="center")
        return label

    # Display the title label
    create_centered_label("The title is:", font=FONT_BOLD, fg = TEXT_COLOR)
    create_centered_label(title, font=FONT)

    # Display the description label
    create_centered_label("The description is:", font=FONT_BOLD)

    description_box = scrolledtext.ScrolledText(
        second_frame,
        wrap=tk.WORD,
        width=80,
        height=10,
        font=FONT,
    )
    description_box.insert(tk.END, description)
    description_box.configure(state="disabled")  # Make it read-only
    description_box.pack(pady=10, padx=20)

    # Check if there are image titles, otherwise display a message
    if image_titles:
        create_centered_label("The image titles are:", font=FONT_BOLD)

        images_frame = tk.Frame(second_frame, bg=BG_COLOR)
        images_frame.pack(pady=10)

        for image in image_titles:
            create_centered_label(image, font=FONT)
    else:
        create_centered_label("No images were sent", font=FONT_BOLD, fg="red")

    # Display bibliographic references in a table
    if biblio_ref:
        create_centered_label("Bibliographic References:", font=FONT_BOLD)
        biblio_tree = ttk.Treeview(second_frame, columns=("Reference"), show="headings", height=5)
        biblio_tree.heading("Reference", text="Reference")
        biblio_tree.pack(pady=10)

        for ref in biblio_ref:
            biblio_tree.insert("", "end", values=(ref,))
    else:
        create_centered_label("No bibliographic references were sent", font=FONT_BOLD, fg="red")

    # Display location
    if location:
        create_centered_label("Location:", font=FONT_BOLD)
        create_centered_label(location, font=FONT)
    else:
        create_centered_label("No location was provided", font=FONT_BOLD, fg="red")

    # Display size
    if size:  # Check if size has content indicative of dimensions
        create_centered_label("Size:", font=FONT_BOLD)
        create_centered_label(size, font=FONT)
    else:
        create_centered_label("No sizes were given", font=FONT_BOLD, fg="red")

    # Display tags
    if tags:
        create_centered_label("Tags:", font=FONT_BOLD)
        tags_frame = tk.Frame(second_frame, bg=BG_COLOR)
        tags_frame.pack(pady=1)

        for tag in tags:
            create_centered_label(tag, font=FONT)
    else:
        create_centered_label("No tags were provided", font=FONT_BOLD, fg="red")

    # Back button to return to Window 4 with the updated image count
    back_button = tk.Button(
        second_frame,
        text="Back",
        font=FONT,
        fg=BUTTON_TEXT,
        bg=BUTTON_COLOR,
        command=lambda: (
            window_6.destroy(), open_window_4(title, description, image_titles, biblio_ref, location, size, tags))
    )

    back_button.pack(pady=10)

    # Send to database button
    send_button = tk.Button(
        second_frame,
        text="Send to Database",
        font=FONT,
        fg=BUTTON_TEXT,
        bg=BUTTON_COLOR,
        command=lambda: QR.open_save_HTML(title)  # Opens the new window and closes current
    )
    send_button.pack(pady=20)

    window_6.mainloop()


def open_window_4(title="", description="", image_titles=None, biblio_ref="", location="", size="", tags=""):
    """Creates Window 4: Display title, description, and image upload functionality."""

    # Create Window 4
    window_4 = tk.Tk()
    window_4.title("4 Database - Insert Images")
    window_4.configure(bg=BG_COLOR)

    if image_titles is None:
        image_titles = []

    def go_to_window_6():
        """Transition to Window 6 with the collected title, description, and image titles."""
        # Collect the input data from the current window's fields
        title = title_text.get("1.0", "end-1c").strip()  # Get the title text and strip whitespace
        description = description_text.get("1.0", "end-1c").strip()  # Get the description text and strip whitespace
        biblio_ref = [entry.get().strip() for entry in ref_entries if
                      entry.get().strip()]  # Collect non-empty references
        location = location_entry.get().strip()  # Get location info

        # Collect size info (concatenated dimensions)
        length = length_entry.get().strip()
        width = width_entry.get().strip()
        height = height_entry.get().strip()

        # Collect keywords/tags
        tags = [entry.get().strip() for entry in keyword_entries if entry.get().strip()]

        # Validation checks
        is_valid = True

        # Check for empty title
        if not title:
            title_error.config(text="Please provide a title", fg="red")
            is_valid = False
        else:
            title_error.config(text="")

        # Check for empty description
        if not description:
            description_error.config(text="Please provide a description", fg="red")
            is_valid = False
        else:
            description_error.config(text="")

        # Initialize size as an empty string
        size = ""

        # Check for the presence of any dimension and validate them
        if length or width or height:
            try:
                # Convert dimensions to float, if provided
                if length:
                    length = float(length)
                if width:
                    width = float(width)
                if height:
                    height = float(height)

                # Ensure the dimensions don't exceed the maximum allowed size
                if (length and length > 99999.99) or (width and width > 99999.99) or (height and height > 99999.99):
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_error.config(text="")  # Clear error if sizes are valid

                # Build the size string based on the dimensions provided
                if length:
                    size += f"Length: {length} "
                if width:
                    size += f"Width: {width} "
                if height:
                    size += f"Height: {height} "

                size = size.strip()  # Remove any trailing spaces

            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False
        else:
            size = ""  # If no dimensions are provided, leave size empty

        # If all inputs are valid, proceed to open Window 6 and destroy Window 4
        if is_valid:
            window_4.destroy()
            open_window_6(title, description, image_titles, biblio_ref, location, size, tags, window_4)

    def upload_image():
        """Handle image upload."""
        if len(image_titles) < 5:
            file_path = filedialog.askopenfilename(title="Select an Image",
                                                   filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                image_title = file_path.split('/')[-1]
                image_titles.append(image_title)
                update_image_titles()
                update_upload_count()

        if len(image_titles) >= 5:
            upload_button.config(state="disabled", text="Upload limit\nreached", bg=BUTTON_COLOR, fg=BUTTON_TEXT)

    def update_image_titles():
        """Update the image titles list displayed in the window."""
        for widget in image_titles_frame.winfo_children():
            widget.destroy()

        for image in image_titles:
            image_frame = tk.Frame(image_titles_frame, bg=BG_COLOR)
            image_frame.pack(anchor="w", pady=2)

            title_label = tk.Label(image_frame, text=image, font=FONT, bg=BG_COLOR)
            title_label.pack(side="left")

            remove_button = tk.Button(image_frame, text="X", font=FONT_BOLD, fg="white", bg=BUTTON_COLOR,
                                      command=lambda img=image: remove_image(img))
            remove_button.pack(side="right", padx=5)

    def update_upload_count():
        """Update the upload count text."""
        upload_count_label.config(text=f"{len(image_titles)}/5 images uploaded")

    def remove_image(image_title):
        """Remove the image from the list."""
        image_titles.remove(image_title)
        update_image_titles()
        update_upload_count()
        if len(image_titles) < 5:
            upload_button.config(state="normal", text="Upload")

    def update_character_count(event=None):
        """Update character count and check if the limit is exceeded."""
        send_button_enabled = True  # Flag to track if the send button should be enabled

        # Update character count for the title
        char_count_title = len(title_text.get("1.0", "end-1c"))
        title_char_count_label.config(text=f"{char_count_title}/75")
        if char_count_title > 75:
            title_text.config(fg="red")
            title_char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            title_text.config(fg="black")
            title_char_count_label.config(fg="black")

        # Update character count for the description
        char_count_description = len(description_text.get("1.0", "end-1c"))
        char_count_label.config(text=f"{char_count_description}/3000")
        if char_count_description > 3000:
            description_text.config(fg="red")
            char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            description_text.config(fg="black")
            char_count_label.config(fg="black")

        # Update counter for Location
        char_count_location = len(location_entry.get())
        location_char_count_label.config(text=f"{char_count_location}/75")
        if char_count_location > 75:
            location_entry.config(fg="red")
            location_char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            location_entry.config(fg="black")
            location_char_count_label.config(fg="black")

        # Update character count for each reference field
        for ref_entry, ref_count_label in zip(ref_entries, ref_count_labels):
            char_count_ref = len(ref_entry.get())
            ref_count_label.config(text=f"{char_count_ref}/75")
            if char_count_ref > 75:
                ref_entry.config(fg="red")
                ref_count_label.config(fg="red")
                send_button_enabled = False
            else:
                ref_entry.config(fg="black")
                ref_count_label.config(fg="black")

        # Update character count for each keyword field
        for keyword_entry, keyword_count_label in zip(keyword_entries, keywords_count_labels):
            char_count_ref = len(keyword_entry.get())
            keyword_count_label.config(text=f"{char_count_ref}/20")
            if char_count_ref > 20:
                keyword_entry.config(fg="red")
                keyword_count_label.config(fg="red")
                send_button_enabled = False
            else:
                keyword_entry.config(fg="black")
                keyword_count_label.config(fg="black")

        # Enable or disable the send button based on character count conditions
        if send_button_enabled:
            send_button.config(state="normal")
        else:
            send_button.config(state="disabled")

    main_frame = Frame(window_4, bg=BG_COLOR)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame, bg=BG_COLOR)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, bg=BG_COLOR)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    # Center the title frame
    title_frame = tk.Frame(second_frame, bg=BG_COLOR)
    title_frame.pack(anchor="center")

    title_label = tk.Label(title_frame, text="Title:", font=FONT_BOLD, bg=BG_COLOR)
    title_label.pack(side="left")

    title_text = tk.Text(title_frame, wrap=tk.WORD, width=40, height=1, font=FONT_TEXT, fg="black", bg=ENTRY_COLOR)
    title_text.insert(tk.END, title)
    title_text.pack(side="left")

    title_char_count_label = tk.Label(title_frame, text="0/75", font=FONT_TEXT,
                                      bg=BG_COLOR)
    title_char_count_label.pack(side="left")

    title_error = tk.Label(second_frame, text="", font=FONT_TEXT, bg=BG_COLOR)
    title_error.pack(anchor="center")

    description_frame = tk.Frame(second_frame, bg=BG_COLOR)
    description_frame.pack(anchor="center")

    description_label = tk.Label(description_frame, text="Description:", font=FONT_BOLD, bg=BG_COLOR)
    description_label.pack(side="left")

    description_text = scrolledtext.ScrolledText(second_frame, wrap=tk.WORD, width=60, height=6, font=FONT_TEXT,
                                                 bg=ENTRY_COLOR)

    char_count_label = tk.Label(description_frame, text="0/3000", font=FONT_TEXT, bg=BG_COLOR)
    char_count_label.pack(side="left")

    description_text.insert(tk.END, description)
    description_text.pack(anchor="center", fill="x", padx=20, pady=2)

    description_error = tk.Label(second_frame, text="", font=FONT_TEXT, bg=BG_COLOR)
    description_error.pack(anchor="center")

    upload_prompt_label = tk.Label(second_frame, text="Please upload images:", font=FONT_BOLD,
                                   bg=BG_COLOR)
    upload_prompt_label.pack(anchor="center")

    upload_frame = tk.Frame(second_frame, bg=BG_COLOR)
    upload_frame.pack(anchor="center")

    upload_count_label = tk.Label(upload_frame, text="0/5 images uploaded", font=FONT, bg=BG_COLOR)
    upload_count_label.grid(row=1, column=0, columnspan=2, sticky="nsew")

    upload_button = tk.Button(upload_frame, text="Upload", font=FONT, width=12, height=6, bg=BUTTON_COLOR,
                              command=upload_image, fg=BUTTON_TEXT)
    upload_button.grid(row=0, column=0, sticky="w")

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    image_titles_frame = tk.Frame(upload_frame, bg=BG_COLOR)
    image_titles_frame.grid(row=0, column=1, sticky="w")

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    references = tk.Label(second_frame, text="References:", font=FONT_BOLD, bg=BG_COLOR)
    references.pack(anchor="center")

    # Creating the bibliographic reference entry fields
    ref_entries = []
    ref_count_labels = []  # List to store reference count labels
    for i in range(10):  # Adjust the number based on your needs
        ref_frame = tk.Frame(second_frame, bg=BG_COLOR)
        ref_frame.pack(anchor="center")

        ref_entry = tk.Entry(ref_frame, font=FONT_TEXT, width=60, bg=ENTRY_COLOR)
        ref_entry.pack(side="left")
        ref_entries.append(ref_entry)

        # Add a character count label next to each entry field
        ref_count_label = tk.Label(ref_frame, text="0/75", font=FONT_TEXT, bg=BG_COLOR)
        ref_count_label.pack(side="left")
        ref_count_labels.append(ref_count_label)

        # Bind the update function to each reference entry
        ref_entry.bind("<KeyRelease>", lambda event, lbl=ref_count_label: update_character_count(event, lbl))

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    # Location frame
    location_frame = tk.Frame(second_frame, bg=BG_COLOR)
    location_frame.pack(anchor="center")

    location_label = tk.Label(location_frame, text="Location:", font=FONT_BOLD, bg=BG_COLOR)
    location_label.pack(side="left")

    location_entry = tk.Entry(location_frame, width=40, font=FONT_TEXT, bg=ENTRY_COLOR)
    location_entry.insert(tk.END, location)
    location_entry.pack(side="left")

    location_char_count_label = tk.Label(location_frame, text="0/75", font=FONT_TEXT, bg=BG_COLOR)
    location_char_count_label.pack(side="left")

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    # Size of the museum piece (L x W x H) – Ensure it's centered
    size_label = tk.Label(second_frame, text="Size of Museum Piece (L x W x H):", font=FONT_BOLD,
                          bg=BG_COLOR)
    size_label.pack(anchor="center")

    size_frame = tk.Frame(second_frame, bg=BG_COLOR)
    size_frame.pack(anchor="center", pady=10)

    length_entry = tk.Entry(size_frame, font=FONT_TEXT, bg=ENTRY_COLOR, width=10)
    length_entry.pack(side="left", padx=5)

    width_entry = tk.Entry(size_frame, font=FONT_TEXT, bg=ENTRY_COLOR, width=10)
    width_entry.pack(side="left", padx=5)

    height_entry = tk.Entry(size_frame, font=FONT_TEXT, bg=ENTRY_COLOR, width=10)
    height_entry.pack(side="left", padx=5)

    size_error = tk.Label(second_frame, text="", font=FONT_TEXT, bg=BG_COLOR)
    size_error.pack(anchor="center")

    # 15 keywords/tags with text boxes arranged in 5 rows of 3 columns
    keyword_label = tk.Label(second_frame, text="Keywords/Tags:", font=FONT_BOLD, bg=BG_COLOR)
    keyword_label.pack(anchor="center", pady=10)

    # Initialize lists to hold entries and count labels for keywords
    keyword_entries = []
    keywords_count_labels = []

    # Create the keyword entries and character count labels
    for row in range(5):  # Loop through 5 rows
        keyword_row_frame = tk.Frame(second_frame, bg=BG_COLOR)
        keyword_row_frame.pack(anchor="center", pady=2)

        for col in range(3):  # Loop through 3 columns
            # Create keyword entry widget
            keyword_entry = tk.Entry(keyword_row_frame, font=FONT_TEXT, width=20, bg=ENTRY_COLOR)
            keyword_entry.pack(side="left", padx=5)

            # Create the corresponding character count label
            keyword_count_label = tk.Label(keyword_row_frame, text="0/20", font=FONT_TEXT, bg=BG_COLOR)
            keyword_count_label.pack(side="left")

            # Append the entries and labels to their respective lists
            keyword_entries.append(keyword_entry)
            keywords_count_labels.append(keyword_count_label)

            # Bind the update function to each keyword entry
            keyword_entry.bind("<KeyRelease>", update_character_count)

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    send_button = tk.Button(second_frame, text="Send to Database", font=FONT, bg=BUTTON_COLOR,
                            command=go_to_window_6, fg=BUTTON_TEXT)

    send_button.pack(anchor="center")

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=BG_COLOR)
    space_label.pack(anchor="center")

    update_character_count()
    update_image_titles()
    update_upload_count()

    # Bind events to all relevant input fields
    second_frame.bind("<KeyRelease>", update_character_count)
    title_text.bind("<KeyRelease>", update_character_count)
    description_text.bind("<KeyRelease>", update_character_count)
    for ref_entry in ref_entries:
        ref_entry.bind("<KeyRelease>", update_character_count)
    location_entry.bind("<KeyRelease>", update_character_count)
    for keyword_entry in keyword_entries:
        keyword_entry.bind("<KeyRelease>", update_character_count)

    window_4.mainloop()


if __name__ == "__main__":
    # Start by opening window 4
    open_window_4()
