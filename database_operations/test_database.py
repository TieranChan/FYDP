import unittest
from database_logic import parse_size_to_dict

"""Many test cases have been removed assuming UI in Tkinter catches many before submitting input"""
class TestParseSizeToDict(unittest.TestCase):

    def test_already_dict(self):
        size_dict = {"length": "10cm", "width": "5cm", "height": "15cm"}
        self.assertEqual(parse_size_to_dict(size_dict), size_dict)

    def test_empty_string(self):
        size_str = ""
        expected = {"length": "", "width": "", "height": ""}
        self.assertEqual(parse_size_to_dict(size_str), expected)

    def test_invalid_string(self):
        size_str = "Some random text without size info"
        expected = {"length": "", "width": "", "height": ""}
        self.assertEqual(parse_size_to_dict(size_str), expected)



if __name__ == '__main__':
    unittest.main()