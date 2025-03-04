import unittest
import time
import mysql.connector
from database_logic import send_to_database
from html_operations.logic import get_titles_in_folder
import config

class TestController(unittest.TestCase):
    """Controller tests for performance and functionality requirements."""

    def setUp(self):
        # Record the start time for each test.
        self.start_time = time.time()
        # Set up a dedicated test table.
        self.test_table = "test_entries"
        self.connection = mysql.connector.connect(
            host="localhost",
            user=config.mysql_username,
            password=config.mysql_password,
            database="museum_db",
            use_pure=True
        )
        cursor = self.connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.test_table} (
            title VARCHAR(75) PRIMARY KEY,
            description VARCHAR(3000),
            id_num VARCHAR(10),
            img_1 MEDIUMBLOB,
            img_2 MEDIUMBLOB,
            img_3 MEDIUMBLOB,
            img_4 MEDIUMBLOB,
            img_5 MEDIUMBLOB,
            location VARCHAR(75),
            reference_1 VARCHAR(75),
            reference_2 VARCHAR(75),
            reference_3 VARCHAR(75),
            reference_4 VARCHAR(75),
            reference_5 VARCHAR(75),
            reference_6 VARCHAR(75),
            reference_7 VARCHAR(75),
            reference_8 VARCHAR(75),
            reference_9 VARCHAR(75),
            reference_10 VARCHAR(75),
            tag_1 VARCHAR(20),
            tag_2 VARCHAR(20),
            tag_3 VARCHAR(20),
            tag_4 VARCHAR(20),
            tag_5 VARCHAR(20),
            tag_6 VARCHAR(20),
            tag_7 VARCHAR(20),
            tag_8 VARCHAR(20),
            tag_9 VARCHAR(20),
            tag_10 VARCHAR(20),
            tag_11 VARCHAR(20),
            tag_12 VARCHAR(20),
            tag_13 VARCHAR(20),
            tag_14 VARCHAR(20),
            tag_15 VARCHAR(20),
            height VARCHAR(8),
            width VARCHAR(8),
            length VARCHAR(8),
            unit VARCHAR(10)
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def tearDown(self):
        # Print the name of the test and the time it took.
        elapsed = time.time() - self.start_time
        print(f"Test {self._testMethodName} took {elapsed:.3f} seconds")
        # Clean up by dropping the test table.
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.test_table};")
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def test_single_insertion_time(self):
        """Insert a single entry, measure its time, calculate theoretical time for 200 insertions,
           and verify that insertion time is less than 3 seconds."""
        title = "SingleTestEntry"
        data = {
            "title": title,
            "description": "Single entry test",
            "location": "Test location",
            "height": "10",
            "width": "5",
            "length": "15",
            "unit": "cm"
        }
        start_insertion = time.time()
        send_to_database(
            self.test_table,
            title,
            data["description"],
            ["Ref1"],
            data["location"],
            {"Length": data["length"], "Width": data["width"], "Height": data["height"]},
            ["Tag1"],
            [],  # No images for testing
            None,
            data["unit"]
        )
        elapsed_insertion = time.time() - start_insertion
        print(f"Time for one insertion: {elapsed_insertion:.3f} seconds")
        theoretical_total = elapsed_insertion * 200
        print(f"Theoretical time for 200 insertions: {theoretical_total:.3f} seconds")
        self.assertLess(elapsed_insertion, 3, f"Insertion time {elapsed_insertion:.3f} seconds exceeds 3 sec threshold.")
        if elapsed_insertion < 3:
            print(f"Insertion works because timing {elapsed_insertion:.3f} sec is less than 3 sec.")

    def test_single_entry_size(self):
        """Insert a single entry, calculate its size in MB, and print the theoretical size for 200 entries."""
        title = "SingleTestEntrySize"
        data = {
            "title": title,
            "description": "Single entry test for size measurement",
            "location": "Test location",
            "height": "10",
            "width": "5",
            "length": "15",
            "unit": "cm"
        }
        # Insert one entry.
        send_to_database(
            self.test_table,
            title,
            data["description"],
            ["Ref1"],
            data["location"],
            {"Length": data["length"], "Width": data["width"], "Height": data["height"]},
            ["Tag1"],
            [],  # No images for testing
            None,
            data["unit"]
        )
        # Now, calculate the total size in bytes using a SELECT query.
        cursor = self.connection.cursor()
        query = f"""
        SELECT 
            IFNULL(OCTET_LENGTH(title), 0) +
            IFNULL(OCTET_LENGTH(description), 0) +
            IFNULL(OCTET_LENGTH(id_num), 0) +
            IFNULL(OCTET_LENGTH(img_1), 0) +
            IFNULL(OCTET_LENGTH(img_2), 0) +
            IFNULL(OCTET_LENGTH(img_3), 0) +
            IFNULL(OCTET_LENGTH(img_4), 0) +
            IFNULL(OCTET_LENGTH(img_5), 0) +
            IFNULL(OCTET_LENGTH(location), 0) +
            IFNULL(OCTET_LENGTH(reference_1), 0) +
            IFNULL(OCTET_LENGTH(reference_2), 0) +
            IFNULL(OCTET_LENGTH(reference_3), 0) +
            IFNULL(OCTET_LENGTH(reference_4), 0) +
            IFNULL(OCTET_LENGTH(reference_5), 0) +
            IFNULL(OCTET_LENGTH(reference_6), 0) +
            IFNULL(OCTET_LENGTH(reference_7), 0) +
            IFNULL(OCTET_LENGTH(reference_8), 0) +
            IFNULL(OCTET_LENGTH(reference_9), 0) +
            IFNULL(OCTET_LENGTH(reference_10), 0) +
            IFNULL(OCTET_LENGTH(tag_1), 0) +
            IFNULL(OCTET_LENGTH(tag_2), 0) +
            IFNULL(OCTET_LENGTH(tag_3), 0) +
            IFNULL(OCTET_LENGTH(tag_4), 0) +
            IFNULL(OCTET_LENGTH(tag_5), 0) +
            IFNULL(OCTET_LENGTH(tag_6), 0) +
            IFNULL(OCTET_LENGTH(tag_7), 0) +
            IFNULL(OCTET_LENGTH(tag_8), 0) +
            IFNULL(OCTET_LENGTH(tag_9), 0) +
            IFNULL(OCTET_LENGTH(tag_10), 0) +
            IFNULL(OCTET_LENGTH(tag_11), 0) +
            IFNULL(OCTET_LENGTH(tag_12), 0) +
            IFNULL(OCTET_LENGTH(tag_13), 0) +
            IFNULL(OCTET_LENGTH(tag_14), 0) +
            IFNULL(OCTET_LENGTH(tag_15), 0) +
            IFNULL(OCTET_LENGTH(height), 0) +
            IFNULL(OCTET_LENGTH(width), 0) +
            IFNULL(OCTET_LENGTH(length), 0) +
            IFNULL(OCTET_LENGTH(unit), 0)
        AS total_bytes
        FROM {self.test_table}
        WHERE title = '{title}'
        """
        cursor.execute(query)
        result = cursor.fetchone()
        total_bytes = result[0] if result else 0
        size_mb = total_bytes / (1024 * 1024)
        theoretical_total_mb = size_mb * 200
        print(f"Size for one entry: {size_mb:.6f} MB")
        print(f"Theoretical size for 200 entries: {theoretical_total_mb:.6f} MB")
        cursor.close()
        self.assertGreater(total_bytes, 0, "Entry size should be greater than 0 bytes.")

if __name__ == '__main__':
    print("Starting tests...")
    unittest.main()
