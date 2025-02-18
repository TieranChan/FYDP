import unittest
from unittest.mock import patch
from io import StringIO
import tkinter.filedialog as filedialog
from logic import *  # Assuming the function is in this file

"""
This file is used to test the extract_fields function in the generate_html function
"""
class TestGenerateHtmlPage(unittest.TestCase):

    def test_extract_fields_with_complete_data(self):
        data = {
            "description": "Museum of Art",
            "location": "Paris",
            "hight": 10,
            "width": 20,
            "length": 30,
            "img_1": "image1.jpg",
            "img_2": "image2.jpg",
            "reference_1": "Reference 1",
            "tag_1": "Art",
            "tag_2": "Museum"
        }

        description, location, size, image_titles, biblio_ref, tags, size_components = extract_fields(data)

        # Assertions
        self.assertEqual(description, "Museum of Art")
        self.assertEqual(location, "Paris")
        self.assertEqual(size, "H: 10, W: 20, L: 30")
        self.assertEqual(image_titles, ["image1.jpg", "image2.jpg"])
        self.assertEqual(biblio_ref, ["Reference 1"])
        self.assertEqual(tags, ["Art", "Museum"])
        self.assertEqual(size_components, ["H: 10", "W: 20", "L: 30"])

    def test_extract_fields_with_missing_data(self):
        data = {
            "description": "Modern Art Museum",
            "location": "New York",
            # Missing hight, width, length
            "img_1": "image1.jpg"
        }

        description, location, size, image_titles, biblio_ref, tags, size_components = extract_fields(data)

        # Assertions
        self.assertEqual(description, "Modern Art Museum")
        self.assertEqual(location, "New York")
        self.assertEqual(size, "H: None, W: None, L: None")
        self.assertEqual(image_titles, ["image1.jpg"])
        self.assertEqual(biblio_ref, [])
        self.assertEqual(tags, [])
        self.assertEqual(size_components, ["H: None", "W: None", "L: None"])

if __name__ == '__main__':
    unittest.main()