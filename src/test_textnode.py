import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node222", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode(
            "This is a text node", TextType.BOLD, url="http://www.boot.dev"
        )
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image1(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image"}
        )

    def test_image2(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_image3(self):
        node = TextNode("This is bold", TextType.LINK, "dog.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is bold")
        self.assertEqual(html_node.props, {"href": "dog.jpg"})


"""
TEST PLAN
- bold
- bold double
- italic
- bold and italic
- code (block)
- when the last word is encapsulated
"""


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("testing **Bold** text", TextType.TEXT)
        new_node = markdown_to_htmlnode([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("testing ", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_node,
        )

    def test_bold_double(self):
        node = TextNode("writing **another** sentence **for** double", TextType.TEXT)
        new_node = markdown_to_htmlnode([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("writing ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
                TextNode(" sentence ", TextType.TEXT),
                TextNode("for", TextType.BOLD),
                TextNode(" double", TextType.TEXT),
            ],
            new_node,
        )

    def test_italic(self):
        node = TextNode("another test, *but* this time for italic", TextType.TEXT)
        new_node = markdown_to_htmlnode([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("another test, ", TextType.TEXT),
                TextNode("but", TextType.ITALIC),
                TextNode(" this time for italic", TextType.TEXT),
            ],
            new_node,
        )


    def test_bold_and_italic(self):
        node = TextNode("this time, it's **bold** and *italic* texts", TextType.TEXT)
        new_node = markdown_to_htmlnode([node], "**", TextType.BOLD)
        new_node = markdown_to_htmlnode(new_node, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("this time, it's ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" texts", TextType.TEXT),
            ],
            new_node,
        )

    def test_code(self):
        node = TextNode("lastly, it's `code` block", TextType.TEXT)
        new_node = markdown_to_htmlnode([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("lastly, it's ",TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" block", TextType.TEXT),
            ],
            new_node,
        )

    def test_last_word_encapsulated(self):
        node = TextNode("very final test I **hope!**", TextType.TEXT)
        new_node = markdown_to_htmlnode([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("very final test I ", TextType.TEXT),
                TextNode("hope!", TextType.BOLD),
                TextNode("", TextType.TEXT),
            ],
            new_node,
        )


"""
SELF NOTE
- imports done
- use assertListEqual (https://docs.python.org/3/library/unittest.html)

- almost ran out of sparking water, almond milk, olives
- Costco this weekend
"""


if __name__ == "__main__":
    unittest.main()
