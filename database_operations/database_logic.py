import mysql.connector
import hashlib
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
import config

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

"""
Helper method to extract the data associated to a name in the entry of the database at an index different from the one
of the list containing the newest set of images
"""
def image_data_retriever(find_data_of, existing_names, cursor, folder, id_numb):
    for i in range(len(existing_names)):
        if find_data_of == existing_names[i]:
            cursor.execute(f"SELECT img_{i+1} FROM {folder} WHERE id_num=\'{id_numb}\' ")
            tmp_data = cursor.fetchone()
            tmp_data = tmp_data[0]
            return tmp_data
    return "NULL"


#Warning, ye who dares venture below shall enter Laplante's battlefield
def image_format(images, id_numb, folder):
    """This function extracts image bytes from a filepath, and assigns it to a position in the list. If there is no image passed, the value of NULL is passed"""
    connection = mysql.connector.connect(
        host="localhost",
        user=config.mysql_username,
        password=config.mysql_password,
        database="museum_db",
        use_pure=True
    )
    cursor = connection.cursor()

    image_data = ["NULL"] * 5
    if id_numb is not None:
        #Names will contain all the img_name fields including NULL
        cursor.execute(f"SELECT img_name1, img_name2, img_name3, img_name4, img_name5 FROM {folder} WHERE id_num=\'{id_numb}\';")
        names = cursor.fetchall()
        names = names[0]
        for i in range(0,5):
            try:
                #The list of images gotten by this function has a title at a diferent index than what currently is in the db,
                #we must move stuff around.
                if images[i]!= names[i] and images[i] != images[i].split('/')[-1]:
                    # In this case, the given name is a filepath, not a title + extension
                    tmp_img = decode_data(images[i])
                    command = (f"UPDATE {folder} SET img_name{i+1}=%s, img_{i+1}=%s WHERE id_num=\'{id_numb}\';")
                    cursor.execute(command,(images[i].split('/')[-1], tmp_img))
                    connection.commit()
                elif images[i] != names[i] and images[i] == images[i].split('/')[-1]:
                    #The name in this index of images is retrieved from the db, so its information is in the db somewhere
                    #The image_data_retriever function is a helper method to get the correct information out of the database.
                    tmp_img = image_data_retriever(images[i], names, cursor, folder, id_numb)
                    command = (f"UPDATE {folder} SET img_name{i + 1}=%s, img_{i + 1}=%s WHERE id_num=\'{id_numb}\';")
                    cursor.execute(command, (images[i], tmp_img))
                    connection.commit()
                #Otherwise, image[i] and names[i] are the same, meaning that the new image at i is in the same position
                #as the old image at i
            except: #Defensive programming
                #If we get here, it is becasue there is no images[i], meaning the code is trying to access an image index
                #slated to be empty.
                command = (f"UPDATE {folder} SET img_name{i+1}=\"NULL\", img_{i + 1}=\"NULL\" WHERE id_num=\'{id_numb}\';")
                cursor.execute(command)
                connection.commit()
    else:
        for i in range(len(images)):
            if images[i].strip().upper() == "NULL":
                image_data[i] = "NULL"
            else:
                image_data[i] = decode_data(images[i])
            images[i] = images[i].split('/')[-1]

        while len(images) < 5:
            images.append("NULL")

    if connection.is_connected():
        cursor.close()
        connection.close()
    return image_data, images

def refs_format(refs):
    """This function extracts the current references into a list of ten elements which include the references and NULLs"""
    all_refs=["NULL"]*10
    for i in range(len(refs)):
        all_refs[i]=refs[i]

    return all_refs

def tag_format(tags):
    """This function extracts the current tags into a list of fifteen elements which include the tags and NULLs"""
    all_tags = ["NULL"] * 15
    for i in range(len(tags)):
        all_tags[i] = tags[i]

    return all_tags

def get_dims(dimensions):
    """Extracting values from potentially non-existent fields in a dictionary"""
    if dimensions['Length'] == "":
        length = 0
    else:
        length = dimensions['Length']
    if dimensions['Width'] == "":
        width = 0
    else:
        width = dimensions['Width']
    if dimensions['Height'] == "":
        height = 0
    else:
        height = dimensions['Height']

    return length, width, height

"""
This function,as the name indicates, sends data to the database. That is both in the case of the creation of an entry and 
the modification of an existing entry.
"""
def send_to_database(folder, title, description, references, location, size, tags, image_titles, id_numb, unit):
    #Laplante here, I need to use the og id_num value of an entry while modifying this allows staff to change the title
    #of an entry should they wish to. id_numb is the og id, id_num is one generated for a new entry. As per Chan's design,
    #we need to let staff know that they must never reuse a title... at least in the same folder.
    images, image_titles= image_format(image_titles, id_numb, folder)
    refs = refs_format(references)
    new_tags = tag_format(tags)
    length, width, height = get_dims(size)

    if unit is None:
        unit="NULL"

    #Using prepared statements to handle escaping and insertion of binary data safely
    # Prepare the SQL query with placeholders for the values
    # Collect all the data into a tuple
    connection = mysql.connector.connect(
        host="localhost",
        user=config.mysql_username,
        password=config.mysql_password,
        database="museum_db",
        use_pure=True
    )
    
    if id_numb is not None:
        query = (f"UPDATE {folder} SET title=%s, description=%s, location=%s, reference_1=%s, reference_2=%s, reference_3=%s, "
                 f"reference_4=%s, reference_5=%s, reference_6=%s, reference_7=%s, reference_8=%s, reference_9=%s,"
                 f" reference_10=%s, tag_1=%s, tag_2=%s, tag_3=%s, tag_4=%s, tag_5=%s, tag_6=%s, tag_7=%s, tag_8=%s,"
                 f" tag_9=%s, tag_10=%s, tag_11=%s, tag_12=%s, tag_13=%s, tag_14=%s, tag_15=%s, length=%s, width=%s,"
                 f" height=%s, unit=%s WHERE id_num=%s;")
        data = (title, description, location, refs[0], refs[1], refs[2], refs[3], refs[4], refs[5], refs[6], refs[7],
                refs[8], refs[9], new_tags[0], new_tags[1], new_tags[2], new_tags[3], new_tags[4], new_tags[5],
                new_tags[6], new_tags[7], new_tags[8], new_tags[9], new_tags[10], new_tags[11], new_tags[12],
                new_tags[13], new_tags[14], length, width, height, unit, id_numb)
    else:
        # Creating the unique key by hashing the title and taking the first 10 characters
        # I am assuming here that there can't be 2 entries with the same title
        full_hash = hashlib.sha256(title.encode()).hexdigest()
        id_num = full_hash[:10]
        query = f"""
            SELECT id_num
            FROM `{folder}`
            WHERE title = %s
            """
        cursor=connection.cursor()
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        """Empty result, no matching titles found in folder"""
        if result is None:

            query = (f"INSERT INTO {folder} (title, description, id_num, img_name1, img_name2, img_name3, img_name4, img_name5, "
                        f"img_1, img_2, img_3, img_4, img_5, location, reference_1, reference_2, reference_3, reference_4, "
                        f"reference_5, reference_6, reference_7, reference_8, reference_9, reference_10, tag_1, tag_2, tag_3, "
                        f"tag_4, tag_5, tag_6, tag_7, tag_8, tag_9, tag_10, tag_11, tag_12, tag_13, tag_14, tag_15, length, "
                        f"width, height, unit) "
                        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                        f"%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
            data = (title, description, id_num, image_titles[0], image_titles[1], image_titles[2], image_titles[3], image_titles[4],
                    images[0], images[1], images[2], images[3], images[4], location, refs[0], refs[1], refs[2], refs[3], refs[4],
                    refs[5], refs[6], refs[7], refs[8], refs[9], new_tags[0], new_tags[1], new_tags[2], new_tags[3], new_tags[4],
                    new_tags[5], new_tags[6], new_tags[7], new_tags[8], new_tags[9], new_tags[10], new_tags[11], new_tags[12],
                    new_tags[13], new_tags[14], length, width, height, unit)
        else:
            print("DUPLICATE TITLE")
            connection.commit()
            if connection.is_connected():
                cursor.close()
                connection.close()
            return False  


    cursor = connection.cursor()
    #Execute with prepared statement
    cursor.execute(query,data)
    connection.commit()

    if connection.is_connected():
        cursor.close()
        connection.close()
    return True

"""
Helper functions to add images
"""
def decode_data(filepath):
    """This function extracts the raw image bytes from a file to store in the database"""
    with open(filepath, "rb") as file:
        binary_data=file.read()
    return binary_data