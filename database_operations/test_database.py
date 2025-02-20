import unittest
from database_logic import *

class TestParseSizeToDict(unittest.TestCase):
    """Unit tests for the parse_size_to_dict function."""

    def test_already_dict(self):
        """Test when input is already a dictionary (should return unchanged)."""
        size_dict = {"length": "10cm", "width": "5cm", "height": "15cm"}
        self.assertEqual(parse_size_to_dict(size_dict), size_dict)

    def test_empty_string(self):
        """Test when input is an empty string (should return empty values)."""
        size_str = ""
        expected = {"length": "", "width": "", "height": ""}
        self.assertEqual(parse_size_to_dict(size_str), expected)

    def test_invalid_string(self):
        """Test when input is a string with no valid size information."""
        size_str = "Some random text without size info"
        expected = {"length": "", "width": "", "height": ""}
        self.assertEqual(parse_size_to_dict(size_str), expected)


    def test_malformed_input(self):
        """Test when input has unexpected characters or partially broken format."""
        size_str = "Len: 10cm Wid: 5cm H: 15cm"
        expected = {"length": "", "width": "", "height": ""}
        self.assertEqual(parse_size_to_dict(size_str), expected)

    def test_mixed_case(self):
        """Test when input has mixed capitalization in keys."""
        size_str = "length: 12cm width: 8cm HEIGHT: 20cm"
        expected = {"length": "", "width": "", "height": ""}
        self.assertEqual(parse_size_to_dict(size_str), expected)  # Function is case-sensitive
  # -------------------- tag_format Tests --------------------

    def test_tags_normal(self):
        """Test when a list of tags has fewer than 15 elements."""
        tags = ["Tag1", "Tag2", "Tag3"]
        expected = ["Tag1", "Tag2", "Tag3"] + ["NULL"] * 12
        self.assertEqual(tag_format(tags), expected)

    def test_tags_exact_fifteen(self):
        """Test when the list contains exactly 15 elements."""
        tags = [f"Tag{i}" for i in range(15)]
        self.assertEqual(tag_format(tags), tags)


    def test_tags_empty(self):
        """Test when the input list is empty (should return 15 NULLs)."""
        self.assertEqual(tag_format([]), ["NULL"] * 15)

    # -------------------- get_dims Tests --------------------

    def test_get_dims_valid(self):
        """Test when the dictionary has valid dimensions."""
        dimensions = {"Length": "10", "Width": "5", "Height": "15"}
        expected = ("10", "5", "15")
        self.assertEqual(get_dims(dimensions), expected)

    def test_get_dims_missing_length(self):
        """Test when the dictionary has an empty Length field."""
        dimensions = {"Length": "", "Width": "5", "Height": "15"}
        expected = (0, "5", "15")
        self.assertEqual(get_dims(dimensions), expected)

    def test_get_dims_missing_width(self):
        """Test when the dictionary has an empty Width field."""
        dimensions = {"Length": "10", "Width": "", "Height": "15"}
        expected = ("10", 0, "15")
        self.assertEqual(get_dims(dimensions), expected)

    def test_get_dims_missing_height(self):
        """Test when the dictionary has an empty Height field."""
        dimensions = {"Length": "10", "Width": "5", "Height": ""}
        expected = ("10", "5", 0)
        self.assertEqual(get_dims(dimensions), expected)

    def test_get_dims_all_missing(self):
        """Test when all fields in the dictionary are empty."""
        dimensions = {"Length": "", "Width": "", "Height": ""}
        expected = (0, 0, 0)
        self.assertEqual(get_dims(dimensions), expected)

    def test_get_dims_nonexistent_keys(self):
        """Test when the dictionary is missing one or more keys (should raise KeyError)."""
        dimensions = {"Length": "10", "Width": "5"}  # Missing Height key
        with self.assertRaises(KeyError):
            get_dims(dimensions)


if __name__ == '__main__':
    unittest.main()
