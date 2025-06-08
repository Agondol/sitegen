import unittest

from blocktype import (
    BlockType,
    block_to_block_type,
)

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type_heading_one(self):
        block = "# This is a heading one"
        expected_result = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_heading_two(self):
        block = "## This is a heading two"
        expected_result = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_heading_three(self):
        block = "### This is a heading three"
        expected_result = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_heading_four(self):
        block = "#### This is a heading four"
        expected_result = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_heading_five(self):
        block = "##### This is a heading five"
        expected_result = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_heading_six(self):
        block = "###### This is a heading six"
        expected_result = BlockType.HEADING
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_heading_seven(self):
        block = "####### This is a heading seven"
        expected_result = BlockType.HEADING
        self.assertNotEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_code(self):
        block = "```This is a block of code```"
        expected_result = BlockType.CODE
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_quote(self):
        block = "> To be or not to be,\n> that is the question."
        expected_result = BlockType.QUOTE
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_unordered_list(self):
        block = "- bread\n- peanut butter\n- jelly"
        expected_result = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(block), expected_result)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Preheat oven to 400\n2. Bake pizza for 15 minutes\n3. Enjoy"
        expected_result = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(block), expected_result)

if __name__ == "__main__":
    unittest.main()