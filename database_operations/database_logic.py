def parse_size_to_dict(size_str):
    """Convert a size string or dictionary into a dictionary."""
    if isinstance(size_str, dict):
        return size_str  # Already a dictionary, return as is
    size_dict = {"length": "", "width": "", "height": ""}
    if isinstance(size_str, str):
        size_parts = size_str.split()
        for part in size_parts:
            if part.startswith("Length:"):
                size_dict["length"] = part.split(":")[1].strip()
            elif part.startswith("Width:"):
                size_dict["width"] = part.split(":")[1].strip()
            elif part.startswith("Height:"):
                size_dict["height"] = part.split(":")[1].strip()
    return size_dict



def send_to_database(folder, title="", description="", references=None, location="", size="", tags="", image_titles=None):
    # TODO
    # À implementer par LAPLANTE
    print("Sent to database")