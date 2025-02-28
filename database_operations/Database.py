import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, Frame, BOTH, LEFT, RIGHT, Y, Canvas, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from database_operations.database_logic import *
#from database_logic import *
import config
from html_operations import QR, logic


def final_check_window(title, description, image_titles, biblio_ref, location, size, tags, window_4, id_num=None, unit=None):
    """Creates Window 6: Display title, description, image titles, and send button."""
    window_6 = tk.Tk()
    window_6.title("Window 6 - Display Collected Data")
    window_6.configure(bg=config.BG_COLOR)
    window_6.geometry("950x600")

    main_frame = Frame(window_6, bg=config.BG_COLOR)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame, bg=config.BG_COLOR)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, bg=config.BG_COLOR)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Helper function: returns True only if value is not empty and not "NULL"
    def is_valid(value):
        return value is not None and str(value).strip() != "" and str(value).strip().upper() != "NULL"

    # Helper to create centered labels
    def create_centered_label(text, font=config.FONT, bold=False, fg=config.TEXT_COLOR, bg=config.BG_COLOR):
        label_font = (font[0], font[1], "bold") if bold else font
        label = tk.Label(second_frame, text=text, font=label_font, fg=fg, bg=bg)
        label.pack(pady=10, anchor="center")
        return label

    # Display title (assumed to be always valid)
    create_centered_label("The title is:", font=config.FONT_BOLD, fg=config.TEXT_COLOR)
    create_centered_label(title, font=config.FONT)

    # Display description if valid; otherwise, show a message indicating no description
    if is_valid(description):
        create_centered_label("The description is:", font=config.FONT_BOLD)
        description_box = scrolledtext.ScrolledText(
            second_frame,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=config.FONT,
        )
        description_box.insert(tk.END, description)
        description_box.configure(state="disabled")
        description_box.pack(pady=10, padx=20)
    else:
        create_centered_label("No description provided", font=config.FONT_BOLD, fg="red")

    # Display image titles if any valid images are passed
    valid_images = [img for img in image_titles if is_valid(img)]
    if valid_images:
        create_centered_label("The image titles are:", font=config.FONT_BOLD)
        images_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
        images_frame.pack(pady=10)
        for image in valid_images:
            # Show only the filename portion
            create_centered_label(image.split('/')[-1], font=config.FONT)
    else:
        create_centered_label("No images were sent", font=config.FONT_BOLD, fg="red")

    # Display bibliographic references if any valid ones exist
    valid_refs = [ref for ref in biblio_ref if is_valid(ref)]
    if valid_refs:
        create_centered_label("Bibliographic References:", font=config.FONT_BOLD)
        biblio_tree = ttk.Treeview(second_frame, columns=("Reference"), show="headings", height=5)
        biblio_tree.heading("Reference", text="Reference")
        biblio_tree.pack(pady=10)
        for ref in valid_refs:
            biblio_tree.insert("", "end", values=(ref,))
    else:
        create_centered_label("No bibliographic references were sent", font=config.FONT_BOLD, fg="red")

    # Display location if valid
    if is_valid(location):
        create_centered_label("Location:", font=config.FONT_BOLD)
        create_centered_label(location, font=config.FONT)
    else:
        create_centered_label("No location was provided", font=config.FONT_BOLD, fg="red")

    # Display size if at least one of its components is valid
    if size and (is_valid(size.get("Length", "")) or is_valid(size.get("Width", "")) or is_valid(size.get("Height", ""))):
        create_centered_label("Size:", font=config.FONT_BOLD)
        size_str = f"Length: {size['Length']} Width: {size['Width']} Height: {size['Height']}"
        create_centered_label(size_str, font=config.FONT)
    else:
        create_centered_label("No sizes were given", font=config.FONT_BOLD, fg="red")

    # Display tags if any valid tags exist
    valid_tags = [tag for tag in tags if is_valid(tag)]
    if valid_tags:
        create_centered_label("Tags:", font=config.FONT_BOLD)
        tags_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
        tags_frame.pack(pady=1)
        for tag in valid_tags:
            create_centered_label(tag, font=config.FONT)
    else:
        create_centered_label("No tags were provided", font=config.FONT_BOLD, fg="red")

    # Back button: simply return to the previous window
    back_button = tk.Button(
        second_frame,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            window_6.destroy(),
            send_to_db_window(
                title=title,
                description=description,
                references=biblio_ref,
                location=location,
                size=size,  # Pass size as a dict
                tags=tags,
                image_titles=image_titles,
                id_num=id_num,
                unit=unit
            )
        )
    )
    back_button.pack(pady=10)

    # Send to database button
    send_button = tk.Button(
        second_frame,
        text="Send to Database",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            window_6.destroy(),
            open_select_where_to_store_window(title, description, references=biblio_ref, location=location, size=size, tags=tags, image_titles=image_titles, id_num=id_num, unit=unit)
        )
    )
    send_button.pack(pady=20)

    window_6.mainloop()


def send_to_db_window(title="", description="", references=None, location="", size={}, tags="", image_titles=None, id_num=None, unit=None):
    """Creates Window 4: Display title, description, and reference input functionality."""
    window_4 = tk.Tk()
    window_4.title("4 Database - Insert Images")
    window_4.configure(bg=config.BG_COLOR)
    window_4.geometry("680x600")

    if image_titles is None:
        image_titles = []
    if tags is None:
        tags = []

    # Initialize the preloaded size values with defaults.
    length_value = size['Length']
    width_value = size['Width']
    height_value = size['Height']

    def clean_field(value):
        """Return an empty string if value is None or 'NULL' (ignoring case), otherwise return the trimmed value."""
        if value is None or str(value).strip().upper() == "NULL":
            return ""
        return str(value).strip()

    def clean_size(value):
        """Return an empty string if the size value is 0, None, or 'NULL'; otherwise return the trimmed value."""
        if value in (0, "0", None) or str(value).strip().upper() == "NULL":
            return ""
        return str(value).strip()

    def go_to_window_6():
        """Transition to Window 6 with the collected data."""
        title_val = title_text.get("1.0", "end-1c").strip()
        description_val = description_text.get("1.0", "end-1c").strip()
        biblio_ref = [entry.get().strip() for entry in ref_entries if entry.get().strip()]
        location_val = location_entry.get().strip()

        is_valid = True  # Overall validity flag

        # Build the size dict from the three entry fields.
        length = length_entry.get().strip()
        width = width_entry.get().strip()
        height = height_entry.get().strip()
        size_dict = {"Height": "", "Width": "", "Length": ""}

        if length:
            try:
                length_val = float(length)
                if length_val > 99999.99:
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_dict["Length"] = length
            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False

        if width:
            try:
                width_val = float(width)
                if width_val > 99999.99:
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_dict["Width"] = width
            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False

        if height:
            try:
                height_val = float(height)
                if height_val > 99999.99:
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_dict["Height"] = height
            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False

        tags_val = [entry.get().strip() for entry in keyword_entries if entry.get().strip()]

        # Validate title and description.
        if not title_val:
            title_error.config(text="Please provide a title", fg="red")
            is_valid = False
        else:
            title_error.config(text="")

        if not description_val:
            description_error.config(text="Please provide a description", fg="red")
            is_valid = False
        else:
            description_error.config(text="")

        if is_valid:
            window_4.destroy()
            final_check_window(title_val, description_val, image_titles, biblio_ref, location_val, size_dict, tags_val,
                               window_4, id_num, unit)

    def upload_image():
        """Handle image upload."""
        if len(image_titles) < 5:
            file_path = filedialog.askopenfilename(title="Select an Image",
                                                   filetypes=[("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"),
                                                              ("PNG Files", "*.png")], initialdir="/media/user")
            if file_path:
                # image_title = file_path.split('/')[-1] #The point of this is to display the filename to the users.
                # That's great, but useless in the backend. I found where the image title is shown and just modified the text there.
                image_titles.append(file_path)
                update_image_titles()
                update_upload_count()
        if len(image_titles) >= 5:
            upload_button.config(state="disabled", text="Upload limit\nreached", bg=config.BUTTON_COLOR, fg=config.BUTTON_TEXT)

    def update_image_titles():
        """Update the image titles list displayed in the window."""
        for widget in image_titles_frame.winfo_children():
            widget.destroy()
        for image in image_titles:
            image_frame = tk.Frame(image_titles_frame, bg=config.BG_COLOR)
            image_frame.pack(anchor="w", pady=2)
            title_label = tk.Label(image_frame, text=image.split('/')[-1], font=config.FONT, bg=config.BG_COLOR)
            title_label.pack(side="left")
            remove_button = tk.Button(image_frame, text="X", font=config.FONT_BOLD, fg="white", bg=config.BUTTON_COLOR,
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
        send_button_enabled = True

        # Title
        char_count_title = len(title_text.get("1.0", "end-1c"))
        title_char_count_label.config(text=f"{char_count_title}/75")
        if char_count_title > 75:
            title_text.config(fg="red")
            title_char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            title_text.config(fg="black")
            title_char_count_label.config(fg="black")

        # Description
        char_count_description = len(description_text.get("1.0", "end-1c"))
        char_count_label.config(text=f"{char_count_description}/3000")
        if char_count_description > 3000:
            description_text.config(fg="red")
            char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            description_text.config(fg="black")
            char_count_label.config(fg="black")

        # Location
        char_count_location = len(location_entry.get())
        location_char_count_label.config(text=f"{char_count_location}/75")
        if char_count_location > 75:
            location_entry.config(fg="red")
            location_char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            location_entry.config(fg="black")
            location_char_count_label.config(fg="black")

        # References
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

        # Keywords/tags
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

        if send_button_enabled:
            send_button.config(state="normal")
        else:
            send_button.config(state="disabled")

    main_frame = Frame(window_4, bg=config.BG_COLOR)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame, bg=config.BG_COLOR)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, bg=config.BG_COLOR)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")

    # Title frame
    title_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    title_frame.pack(anchor="center")
    title_label = tk.Label(title_frame, text="Title:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    title_label.pack(side="left")
    title_text = tk.Text(title_frame, wrap=tk.WORD, width=40, height=1, font=config.FONT_TEXT, fg="black", bg=config.ENTRY_COLOR)
    title_text.insert(tk.END, clean_field(title))
    title_text.pack(side="left")
    title_char_count_label = tk.Label(title_frame, text="0/75", font=config.FONT_TEXT, bg=config.BG_COLOR)
    title_char_count_label.pack(side="left")
    title_error = tk.Label(second_frame, text="", font=config.FONT_TEXT, bg=config.BG_COLOR)
    title_error.pack(anchor="center")

    # Description frame
    description_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    description_frame.pack(anchor="center")
    description_label = tk.Label(description_frame, text="Description:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    description_label.pack(side="left")
    description_text = scrolledtext.ScrolledText(second_frame, wrap=tk.WORD, width=60, height=6, font=config.FONT_TEXT, bg=config.ENTRY_COLOR)
    char_count_label = tk.Label(description_frame, text="0/3000", font=config.FONT_TEXT, bg=config.BG_COLOR)
    char_count_label.pack(side="left")
    description_text.insert(tk.END, clean_field(description))
    description_text.pack(anchor="center", fill="x", padx=20, pady=2)
    description_error = tk.Label(second_frame, text="", font=config.FONT_TEXT, bg=config.BG_COLOR)
    description_error.pack(anchor="center")

    upload_prompt_label = tk.Label(second_frame, text="Please upload images:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    upload_prompt_label.pack(anchor="center")
    upload_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    upload_frame.pack(anchor="center")
    upload_count_label = tk.Label(upload_frame, text="0/5 images uploaded", font=config.FONT, bg=config.BG_COLOR)
    upload_count_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
    upload_button = tk.Button(upload_frame, text="Upload", font=config.FONT, width=12, height=6, bg=config.BUTTON_COLOR,
                              command=upload_image, fg=config.BUTTON_TEXT)
    upload_button.grid(row=0, column=0, sticky="w")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    image_titles_frame = tk.Frame(upload_frame, bg=config.BG_COLOR)
    image_titles_frame.grid(row=0, column=1, sticky="w")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")

    refs = tk.Label(second_frame, text="References:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    refs.pack(anchor="center")
    ref_count_labels = []
    ref_entries = []
    for i in range(10):
        ref_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
        ref_frame.pack(anchor="center")
        ref_entry = tk.Entry(ref_frame, font=config.FONT_TEXT, width=60, bg=config.ENTRY_COLOR)
        ref_entry.insert(tk.END, clean_field(references[i]) if i < len(references) else "")
        ref_entry.pack(side="left")
        ref_entries.append(ref_entry)
        ref_count_label = tk.Label(ref_frame, text="0/75", font=config.FONT_TEXT, bg=config.BG_COLOR)
        ref_count_label.pack(side="left")
        ref_count_labels.append(ref_count_label)
        ref_entry.bind("<KeyRelease>", lambda event, lbl=ref_count_label: update_character_count(event, lbl))
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")

    location_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    location_frame.pack(anchor="center")
    location_label = tk.Label(location_frame, text="Location:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    location_label.pack(side="left")
    location_entry = tk.Entry(location_frame, width=40, font=config.FONT_TEXT, bg=config.ENTRY_COLOR)
    location_entry.insert(tk.END, clean_field(location))
    location_entry.pack(side="left")
    location_char_count_label = tk.Label(location_frame, text="0/75", font=config.FONT_TEXT, bg=config.BG_COLOR)
    location_char_count_label.pack(side="left")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")

    # Size frame
    size_label = tk.Label(second_frame, text="Size of Museum Piece (L x W x H):", font=config.FONT_BOLD, bg=config.BG_COLOR)
    size_label.pack(anchor="center")
    size_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    size_frame.pack(anchor="center", pady=10)
    length_entry = tk.Entry(size_frame, font=config.FONT_TEXT, bg=config.ENTRY_COLOR, width=10)
    length_entry.pack(side="left", padx=5)
    width_entry = tk.Entry(size_frame, font=config.FONT_TEXT, bg=config.ENTRY_COLOR, width=10)
    width_entry.pack(side="left", padx=5)
    height_entry = tk.Entry(size_frame, font=config.FONT_TEXT, bg=config.ENTRY_COLOR, width=10)
    height_entry.pack(side="left", padx=5)
    length_entry.insert(0, clean_size(size.get('Length', 0)))
    width_entry.insert(0, clean_size(size.get('Width', 0)))
    height_entry.insert(0, clean_size(size.get('Height', 0)))
    size_error = tk.Label(second_frame, text="", font=config.FONT_TEXT, bg=config.BG_COLOR)
    size_error.pack(anchor="center")

    keyword_label = tk.Label(second_frame, text="Keywords/Tags:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    keyword_label.pack(anchor="center", pady=10)
    keyword_entries = []
    keywords_count_labels = []
    for index, tag in enumerate(tags + [""] * (15 - len(tags))):
        row = index // 3
        col = index % 3
        if col == 0:
            keyword_row_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
            keyword_row_frame.pack(anchor="center", pady=2)
        keyword_entry = tk.Entry(keyword_row_frame, font=config.FONT_TEXT, width=20, bg=config.ENTRY_COLOR)
        keyword_entry.insert(tk.END, clean_field(tag))
        keyword_entry.grid(row=row, column=col * 2, padx=5, pady=5)
        keyword_count_label = tk.Label(keyword_row_frame, text="0/20", font=config.FONT_TEXT, bg=config.BG_COLOR)
        keyword_count_label.grid(row=row, column=(col * 2) + 1, padx=5)
        keyword_entries.append(keyword_entry)
        keywords_count_labels.append(keyword_count_label)
        keyword_entry.bind("<KeyRelease>", update_character_count)
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    send_button = tk.Button(second_frame, text="Send to Database", font=config.FONT, bg=config.BUTTON_COLOR,
                            command=go_to_window_6, fg=config.BUTTON_TEXT)
    send_button.pack(anchor="center")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")

    # Back button
    back_button = tk.Button(
        second_frame,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            modification_abort(window_4, title)
        )
    )
    back_button.pack(pady=10)

    update_character_count()
    update_image_titles()
    update_upload_count()
    second_frame.bind("<KeyRelease>", update_character_count)
    title_text.bind("<KeyRelease>", update_character_count)
    description_text.bind("<KeyRelease>", update_character_count)
    for ref_entry in ref_entries:
        ref_entry.bind("<KeyRelease>", update_character_count)
    location_entry.bind("<KeyRelease>", update_character_count)
    for keyword_entry in keyword_entries:
        keyword_entry.bind("<KeyRelease>", update_character_count)
    window_4.mainloop()


def open_select_where_to_store_window(title="", description="", references=None, location="", size="", tags="", image_titles=None, id_num=None, unit=None):
    """Open a window to select where to store the data."""
    select_window = tk.Tk()
    select_window.title("Select Folder to Store Data")
    select_window.configure(bg=config.BG_COLOR)
    select_window.geometry("400x600")
    tk.Label(
        select_window,
        text="Select a folder to store the data:",
        font=config.FONT_BOLD,
        bg=config.BG_COLOR,
        fg=config.TEXT_COLOR
    ).pack(pady=20)
    folder_frame = tk.Frame(select_window, bg=config.BG_COLOR)
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
    def refresh_folder_list():
        folder_listbox.delete(0, "end")
        folders = logic.get_folders()
        for folder in folders:
            folder_listbox.insert("end", folder)
    refresh_folder_list()
    def create_new_folder():
        folder_name = folder_name_entry.get().strip()
        if folder_name:
            try:
                logic.create_folder(folder_name)
                tk.messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully!")
                folder_name_entry.delete(0, "end")
                refresh_folder_list()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to create folder: {e}")
        else:
            tk.messagebox.showwarning("Input Error", "Folder name cannot be empty!")
    tk.Label(
        select_window,
        text="Create a new folder:",
        font=config.FONT_BOLD,
        bg=config.BG_COLOR,
        fg=config.TEXT_COLOR
    ).pack(pady=10)
    new_folder_frame = tk.Frame(select_window, bg=config.BG_COLOR)
    new_folder_frame.pack(pady=10)
    folder_name_entry = tk.Entry(new_folder_frame, font=config.FONT, bg=config.ENTRY_COLOR, fg=config.TEXT_COLOR, width=20)
    folder_name_entry.pack(side="left", padx=5)
    tk.Button(
        new_folder_frame,
        text="Create Folder",
        font=config.FONT,
        bg=config.BUTTON_COLOR,
        fg="white",
        command=create_new_folder
    ).pack(side="left", padx=5)
    def send_to_selected_folder():
        try:
            selected_folder = folder_listbox.get(folder_listbox.curselection())
            send_to_database(selected_folder, title, description, references, location, size, tags, image_titles, id_num, unit)
            select_window.destroy()
        except tk.TclError:
            tk.messagebox.showwarning("Selection Error", "Please select a folder before proceeding.")

    send_to_db_button = tk.Button(
        select_window,
        text="Send to Database",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: (
            send_to_selected_folder(),
            QR.open_main_menu_window()
        )
    )

    send_to_db_button.pack(pady=20)
    select_window.mainloop()


def make_new_entry(title="", description="", image_titles=None, biblio_ref=[], location="", size={}, tags=[], unit=None):
    """Creates Window 4: Display title, description, and image upload functionality."""
    window_4 = tk.Tk()
    window_4.title("4 Database - Insert Images")
    window_4.geometry("650x650")
    window_4.configure(bg=config.BG_COLOR)
    if image_titles is None:
        image_titles = []

    def go_to_window_6():
        """Transition to Window 6 with the collected data."""
        title_val = title_text.get("1.0", "end-1c").strip()
        description_val = description_text.get("1.0", "end-1c").strip()
        biblio_ref = [entry.get().strip() for entry in ref_entries if entry.get().strip()]
        location_val = location_entry.get().strip()

        is_valid = True  # Overall validity flag

        # Build the size dict from the three entry fields.
        length = length_entry.get().strip()
        width = width_entry.get().strip()
        height = height_entry.get().strip()
        size_dict = {"Height": "", "Width": "", "Length": ""}

        if length:
            try:
                length_val = float(length)
                if length_val > 99999.99:
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_dict["Length"] = length
            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False

        if width:
            try:
                width_val = float(width)
                if width_val > 99999.99:
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_dict["Width"] = width
            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False

        if height:
            try:
                height_val = float(height)
                if height_val > 99999.99:
                    size_error.config(text="Please keep the sizes under 99'999.99", fg="red")
                    is_valid = False
                else:
                    size_dict["Height"] = height
            except ValueError:
                size_error.config(text="Please enter valid numeric values for size", fg="red")
                is_valid = False

        tags_val = [entry.get().strip() for entry in keyword_entries if entry.get().strip()]

        # Validate title and description.
        if not title_val:
            title_error.config(text="Please provide a title", fg="red")
            is_valid = False
        else:
            title_error.config(text="")

        if not description_val:
            description_error.config(text="Please provide a description", fg="red")
            is_valid = False
        else:
            description_error.config(text="")

        if is_valid:
            window_4.destroy()
            final_check_window(title_val, description_val, image_titles, biblio_ref, location_val, size_dict, tags_val,
                               window_4, None, unit)

    def upload_image():
        """Handle image upload."""
        if len(image_titles) < 5:
            file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"),
                                                ("PNG Files", "*.png")],initialdir="/media/user")
            if file_path:
                #image_title = file_path.split('/')[-1] #The point of this is to display the filename to the users.
                #That's great, but useless in the backend. I found where the image title is shown and just modified the text there.
                image_titles.append(file_path)
                update_image_titles()
                update_upload_count()
        if len(image_titles) >= 5:
            upload_button.config(state="disabled", text="Upload limit\nreached", bg=config.BUTTON_COLOR, fg=config.BUTTON_TEXT)
    def update_image_titles():
        """Update the image titles list displayed in the window."""
        for widget in image_titles_frame.winfo_children():
            widget.destroy()
        for image in image_titles:
            image_frame = tk.Frame(image_titles_frame, bg=config.BG_COLOR)
            image_frame.pack(anchor="w", pady=2)
            title_label = tk.Label(image_frame, text=image.split('/')[-1], font=config.FONT, bg=config.BG_COLOR)#Added the split part to the text of this label
            title_label.pack(side="left")
            remove_button = tk.Button(image_frame, text="X", font=config.FONT_BOLD, fg="white", bg=config.BUTTON_COLOR,
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
        send_button_enabled = True
        char_count_title = len(title_text.get("1.0", "end-1c"))
        title_char_count_label.config(text=f"{char_count_title}/75")
        if char_count_title > 75:
            title_text.config(fg="red")
            title_char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            title_text.config(fg="black")
            title_char_count_label.config(fg="black")
        char_count_description = len(description_text.get("1.0", "end-1c"))
        char_count_label.config(text=f"{char_count_description}/3000")
        if char_count_description > 3000:
            description_text.config(fg="red")
            char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            description_text.config(fg="black")
            char_count_label.config(fg="black")
        char_count_location = len(location_entry.get())
        location_char_count_label.config(text=f"{char_count_location}/75")
        if char_count_location > 75:
            location_entry.config(fg="red")
            location_char_count_label.config(fg="red")
            send_button_enabled = False
        else:
            location_entry.config(fg="black")
            location_char_count_label.config(fg="black")
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
        if send_button_enabled:
            send_button.config(state="normal")
        else:
            send_button.config(state="disabled")
    main_frame = Frame(window_4, bg=config.BG_COLOR)
    main_frame.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(main_frame, bg=config.BG_COLOR)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    second_frame = Frame(my_canvas, bg=config.BG_COLOR)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    title_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    title_frame.pack(anchor="center")
    title_label = tk.Label(title_frame, text="Title:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    title_label.pack(side="left")
    title_text = tk.Text(title_frame, wrap=tk.WORD, width=40, height=1, font=config.FONT_TEXT, fg="black", bg=config.ENTRY_COLOR)
    title_text.insert(tk.END, title)
    title_text.pack(side="left")
    title_char_count_label = tk.Label(title_frame, text="0/75", font=config.FONT_TEXT, bg=config.BG_COLOR)
    title_char_count_label.pack(side="left")
    title_error = tk.Label(second_frame, text="", font=config.FONT_TEXT, bg=config.BG_COLOR)
    title_error.pack(anchor="center")
    description_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    description_frame.pack(anchor="center")
    description_label = tk.Label(description_frame, text="Description:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    description_label.pack(side="left")
    description_text = scrolledtext.ScrolledText(second_frame, wrap=tk.WORD, width=60, height=6, font=config.FONT_TEXT, bg=config.ENTRY_COLOR)
    char_count_label = tk.Label(description_frame, text="0/3000", font=config.FONT_TEXT, bg=config.BG_COLOR)
    char_count_label.pack(side="left")
    description_text.insert(tk.END, description)
    description_text.pack(anchor="center", fill="x", padx=20, pady=2)
    description_error = tk.Label(second_frame, text="", font=config.FONT_TEXT, bg=config.BG_COLOR)
    description_error.pack(anchor="center")
    upload_prompt_label = tk.Label(second_frame, text="Please upload images:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    upload_prompt_label.pack(anchor="center")
    upload_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    upload_frame.pack(anchor="center")
    upload_count_label = tk.Label(upload_frame, text="0/5 images uploaded", font=config.FONT, bg=config.BG_COLOR)
    upload_count_label.grid(row=1, column=0, columnspan=2, sticky="nsew")
    upload_button = tk.Button(upload_frame, text="Upload", font=config.FONT, width=12, height=6, bg=config.BUTTON_COLOR,
                              command=upload_image, fg=config.BUTTON_TEXT)
    upload_button.grid(row=0, column=0, sticky="w")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    image_titles_frame = tk.Frame(upload_frame, bg=config.BG_COLOR)
    image_titles_frame.grid(row=0, column=1, sticky="w")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    references = tk.Label(second_frame, text="References:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    references.pack(anchor="center")
    ref_entries = []
    ref_count_labels = []
    for i in range(10):
        ref_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
        ref_frame.pack(anchor="center")
        ref_entry = tk.Entry(ref_frame, font=config.FONT_TEXT, width=60, bg=config.ENTRY_COLOR)
        ref_entry.insert(tk.END, biblio_ref[i] if i < len(biblio_ref) else "")
        ref_entry.pack(side="left")
        ref_entries.append(ref_entry)
        ref_count_label = tk.Label(ref_frame, text="0/75", font=config.FONT_TEXT, bg=config.BG_COLOR)
        ref_count_label.pack(side="left")
        ref_count_labels.append(ref_count_label)
        ref_entry.bind("<KeyRelease>", lambda event, lbl=ref_count_label: update_character_count(event, lbl))
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    location_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    location_frame.pack(anchor="center")
    location_label = tk.Label(location_frame, text="Location:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    location_label.pack(side="left")
    location_entry = tk.Entry(location_frame, width=40, font=config.FONT_TEXT, bg=config.ENTRY_COLOR)
    location_entry.insert(tk.END, location)
    location_entry.pack(side="left")
    location_char_count_label = tk.Label(location_frame, text="0/75", font=config.FONT_TEXT, bg=config.BG_COLOR)
    location_char_count_label.pack(side="left")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    size_label = tk.Label(second_frame, text="Size of Museum Piece (L x W x H):", font=config.FONT_BOLD, bg=config.BG_COLOR)
    size_label.pack(anchor="center")
    size_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
    size_frame.pack(anchor="center", pady=10)
    length_entry = tk.Entry(size_frame, font=config.FONT_TEXT, bg=config.ENTRY_COLOR, width=10)
    length_entry.pack(side="left", padx=5)
    width_entry = tk.Entry(size_frame, font=config.FONT_TEXT, bg=config.ENTRY_COLOR, width=10)
    width_entry.pack(side="left", padx=5)
    height_entry = tk.Entry(size_frame, font=config.FONT_TEXT, bg=config.ENTRY_COLOR, width=10)
    height_entry.pack(side="left", padx=5)
    size_error = tk.Label(second_frame, text="", font=config.FONT_TEXT, bg=config.BG_COLOR)
    size_error.pack(anchor="center")
    keyword_label = tk.Label(second_frame, text="Keywords/Tags:", font=config.FONT_BOLD, bg=config.BG_COLOR)
    keyword_label.pack(anchor="center", pady=10)
    keyword_entries = []
    keywords_count_labels = []
    for index, tag in enumerate(tags + [""] * (15 - len(tags))):
        row = index // 3
        col = index % 3
        if col == 0:
            keyword_row_frame = tk.Frame(second_frame, bg=config.BG_COLOR)
            keyword_row_frame.pack(anchor="center", pady=2)
        keyword_entry = tk.Entry(keyword_row_frame, font=config.FONT_TEXT, width=20, bg=config.ENTRY_COLOR)
        keyword_entry.insert(tk.END, tag)
        keyword_entry.grid(row=row, column=col * 2, padx=5, pady=5)
        keyword_count_label = tk.Label(keyword_row_frame, text="0/20", font=config.FONT_TEXT, bg=config.BG_COLOR)
        keyword_count_label.grid(row=row, column=(col * 2) + 1, padx=5)
        keyword_entries.append(keyword_entry)
        keywords_count_labels.append(keyword_count_label)
        keyword_entry.bind("<KeyRelease>", update_character_count)
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")
    send_button = tk.Button(second_frame, text="Send to Database", font=config.FONT, bg=config.BUTTON_COLOR,
                            command=go_to_window_6, fg=config.BUTTON_TEXT)
    send_button.pack(anchor="center")
    space_label = tk.Label(second_frame, text="\n", font=("Helvetica", 2, "bold"), bg=config.BG_COLOR)
    space_label.pack(anchor="center")

    # Back button
    back_button = tk.Button(
        second_frame,
        text="Back",
        font=config.FONT,
        fg=config.BUTTON_TEXT,
        bg=config.BUTTON_COLOR,
        command=lambda: (
            modification_abort_new(window_4)
        )
    )
    back_button.pack(pady=10)

    update_character_count()
    update_image_titles()
    update_upload_count()
    second_frame.bind("<KeyRelease>", update_character_count)
    title_text.bind("<KeyRelease>", update_character_count)
    description_text.bind("<KeyRelease>", update_character_count)
    for ref_entry in ref_entries:
        ref_entry.bind("<KeyRelease>", update_character_count)
    location_entry.bind("<KeyRelease>", update_character_count)
    for keyword_entry in keyword_entries:
        keyword_entry.bind("<KeyRelease>", update_character_count)
    window_4.mainloop()

def modification_abort(window_4, title):
    """Display a modal abort window that prevents interaction with window_4.
    When the user clicks (attempting to interact with the background), the window border flashes red.
    """
    # Create the abort window as a child of window_4
    abort_window = tk.Toplevel(window_4)
    abort_window.transient(window_4)
    abort_window.grab_set()  # Make the window modal
    abort_window.title("Confirm Modification Abort")

    # Create a frame with a highlight border inside the abort window.
    border_frame = tk.Frame(abort_window, bg=config.BG_COLOR,
                            highlightthickness=2, highlightbackground=config.BG_COLOR)
    border_frame.pack(fill="both", expand=True)

    # Function to flash the border red when a click is detected.
    def on_click(event):
        border_frame.config(highlightbackground="red")
        # After 500 ms, reset the border to its original color.
        abort_window.after(500, lambda: border_frame.config(highlightbackground=config.BG_COLOR))

    # Bind any left-click in the abort window to on_click.
    abort_window.bind("<Button-1>", on_click)

    # Place your message and buttons inside the border_frame.
    tk.Label(
        border_frame,
        text="You have unsaved changes. Do you want to continue modifying or go back without saving?",
        font=config.FONT,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR,
        wraplength=280,  # Ensure text wraps nicely
    ).pack(pady=10)

    # Yes button - continue modifying.
    tk.Button(
        border_frame,
        text="Keep modifying",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: abort_window.destroy()
    ).pack(side="left", padx=20, pady=10)

    # Cancel button - abort modifications and go back.
    cancel_button = (tk.Button(
        border_frame,
        text="Go back without saving",
        font=config.FONT_BOLD,
        bg="red",
        fg="white",
        activebackground="#D32F2F",
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: [
            abort_window.destroy(),
            window_4.destroy(),
            QR.open_modify_delete_window(title)
        ]
    ))
    cancel_button.pack(side="right", padx=20, pady=10)

    abort_window.mainloop()


def modification_abort_new(window_4):
    """Display a modal abort window that prevents interaction with window_4.
    When the user clicks (attempting to interact with the background), the window border flashes red.
    """
    # Create the abort window as a child of window_4
    abort_window = tk.Toplevel(window_4)
    abort_window.transient(window_4)
    abort_window.grab_set()  # Make the window modal
    abort_window.title("Confirm Modification Abort")

    # Create a frame with a highlight border inside the abort window.
    border_frame = tk.Frame(abort_window, bg=config.BG_COLOR,
                            highlightthickness=2, highlightbackground=config.BG_COLOR)
    border_frame.pack(fill="both", expand=True)

    # Function to flash the border red when a click is detected.
    def on_click(event):
        border_frame.config(highlightbackground="red")
        # After 500 ms, reset the border to its original color.
        abort_window.after(500, lambda: border_frame.config(highlightbackground=config.BG_COLOR))

    # Bind any left-click in the abort window to on_click.
    abort_window.bind("<Button-1>", on_click)

    # Place your message and buttons inside the border_frame.
    tk.Label(
        border_frame,
        text="You have unsaved changes. Do you want to continue modifying or go back without saving?",
        font=config.FONT,
        fg=config.TEXT_COLOR,
        bg=config.BG_COLOR,
        wraplength=280,  # Ensure text wraps nicely
    ).pack(pady=10)

    # Yes button - continue modifying.
    tk.Button(
        border_frame,
        text="Keep modifying",
        font=config.FONT_BOLD,
        bg=config.BUTTON_COLOR,
        fg="white",
        activebackground=config.TEXT_COLOR,
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: abort_window.destroy()
    ).pack(side="left", padx=20, pady=10)

    # Cancel button - abort modifications and go back.
    tk.Button(
        border_frame,
        text="Go back without saving",
        font=config.FONT_BOLD,
        bg="red",
        fg="white",
        activebackground="#D32F2F",
        activeforeground="white",
        padx=10,
        pady=5,
        command=lambda: (
            abort_window.destroy(),
            window_4.destroy(),
            QR.open_main_menu_window()
        )
    ).pack(side="right", padx=20, pady=10)

    abort_window.mainloop()


if __name__ == "__main__":
    make_new_entry()
