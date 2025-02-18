from pathlib import Path
import mysql.connector
def ugly_image(images):
    """This function extracts image bytes from a filepath, and assigns it to a position in the list. If there is no image passed, the value of NULL is passed"""
    image_data=["NULL"]*5
    for i in range(len(images)):
        image_data[i]=decode_data(images[i])

    return image_data

def decode_data(filepath):
    with open(filepath, "rb") as file:
        binary_data=file.read()
    return binary_data


def main():
    # image_titles=[]
    # test_file_path=r"C:/Users/Tiera/Downloads/IMG_20240914_111249_1.jpg"
    # #This is for 
    # image_titles.append(test_file_path)
    # img_1,img_2,img_3,img_4,img_5=ugly_image(image_titles)

    # print(f"{img_2}, {img_5}")
    """Testing retrieving the image from database"""

    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YellowMYSQL45*",
    database="museum_v2"
    )

    cursor = connection.cursor()

    # Execute a query to retrieve the image stored as a BLOB
    cursor.execute("SELECT img_1 FROM museum_test WHERE title = 'asd';")

    # Fetch the image data (first result)
    image_data = cursor.fetchone()[0]

    # Write the image data to a file
    with open("retrieved_image.jpg", "wb") as file:
        file.write(image_data)

    # Close the connection
    cursor.close()
    connection.close()

    print("Image retrieved and saved as retrieved_image.jpg")


if __name__ == "__main__":
    main()