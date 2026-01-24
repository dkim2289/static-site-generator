import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType



class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = "This is **bolded** paragraph"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_heading(self):
        text = "# Heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_code(self):
        text = "```\npython\nprint('Hello, World!')```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_quote(self):
        text = "> This is a quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_unordered_list(self):
        text = "- This is an unordered list"
        self.assertEqual(block_to_block_type(text), BlockType.ULIST)

    def test_ordered_list(self):
        text = "1. This is an ordered list\n2. This is another item\n3. This is a third item"
        self.assertEqual(block_to_block_type(text), BlockType.OLIST)



if __name__ == "__main__":
    unittest.main()
