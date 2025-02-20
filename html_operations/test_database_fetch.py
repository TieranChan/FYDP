import unittest
from logic import *

def safe(value):
    """Mock safe function to mimic its behavior in `extract_fields`."""
    return value if value is not None else ""
"""
Non-optional partial fields not tested as they are covered by the GUI
Therefore, any failures are already checked by the GUI
"""
class TestExtractFields(unittest.TestCase):
    """Unit tests for extract_fields function in html_operations.logic."""

    def test_full_data(self):
        """Test when all fields are present with valid values."""
        data = {
            "description": "A wooden chair",
            "location": "Warehouse A",
            "hight": "120cm",
            "width": "50cm",
            "length": "60cm",
            "img_1": "image1.jpg",
            "img_2": "image2.jpg",
            "reference_1": "Ref001",
            "reference_2": "Ref002",
            "tag_1": "Furniture",
            "tag_2": "Wood"
        }
        expected_size = "H: 120cm, W: 50cm, L: 60cm"
        expected_image_titles = ["image1.jpg", "image2.jpg"]
        expected_biblio_ref = ["Ref001", "Ref002"]
        expected_tags = ["Furniture", "Wood"]
        expected_size_components = ["H: 120cm", "W: 50cm", "L: 60cm"]

        self.assertEqual(extract_fields(data), ("A wooden chair", "Warehouse A", expected_size, expected_image_titles, expected_biblio_ref, expected_tags, expected_size_components))

    def test_missing_optional_fields(self):
        """Test when some optional fields are missing."""
        data = {
            "description": "A steel table",
            "location": "Warehouse B",
            "hight": "100cm",
            "width": "40cm",
            "length": "",
            "img_1": "table.jpg"
        }
        expected_size = "H: 100cm, W: 40cm, L: None"
        expected_image_titles = ["table.jpg"]
        expected_biblio_ref = []
        expected_tags = []
        expected_size_components = ["H: 100cm", "W: 40cm", "L: None"]

        self.assertEqual(extract_fields(data), ("A steel table", "Warehouse B", expected_size, expected_image_titles, expected_biblio_ref, expected_tags, expected_size_components))

 




    def test_multiple_images_references_tags(self):
        """Test when all image, reference, and tag fields are provided."""
        data = {
            "description": "A wooden bookshelf",
            "location": "Library",
            "hight": "200cm",
            "width": "80cm",
            "length": "40cm",
            "img_1": "bookshelf1.jpg",
            "img_2": "bookshelf2.jpg",
            "img_3": "bookshelf3.jpg",
            "img_4": "bookshelf4.jpg",
            "img_5": "bookshelf5.jpg",
            "reference_1": "RefA",
            "reference_2": "RefB",
            "reference_3": "RefC",
            "reference_4": "RefD",
            "reference_5": "RefE",
            "tag_1": "Wood",
            "tag_2": "Shelf",
            "tag_3": "Storage",
            "tag_4": "Furniture",
            "tag_5": "Library"
        }
        expected_size = "H: 200cm, W: 80cm, L: 40cm"
        expected_image_titles = ["bookshelf1.jpg", "bookshelf2.jpg", "bookshelf3.jpg", "bookshelf4.jpg", "bookshelf5.jpg"]
        expected_biblio_ref = ["RefA", "RefB", "RefC", "RefD", "RefE"]
        expected_tags = ["Wood", "Shelf", "Storage", "Furniture", "Library"]
        expected_size_components = ["H: 200cm", "W: 80cm", "L: 40cm"]

        self.assertEqual(extract_fields(data), ("A wooden bookshelf", "Library", expected_size, expected_image_titles, expected_biblio_ref, expected_tags, expected_size_components))

if __name__ == '__main__':
    unittest.main()
