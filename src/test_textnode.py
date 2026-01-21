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
"""
SELF NOTE
- imports done
- use assertListEqual (https://docs.python.org/3/library/unittest.html)

- almost ran out of sparking water, almond milk, olives
- Costco this weekend
"""


# Paul
class TestMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        match = extract_markdown_images("This is text with an ![image](https://example.com/image.jpg)")
        self.assertListEqual(
            [
                ("image", "https://example.com/image.jpg"),
            ],
            match,
        )

# Paul
class TestMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        match = extract_markdown_links(
            "This is text with a link [to example](https://www.boot.dev) and [to YouTube](https://www.youtube.com)"
        )
        self.assertListEqual(
            [
                ("to example", "https://www.boot.dev"),
                ("to YouTube", "https://www.youtube.com")
            ],
            match,
        )




if __name__ == "__main__":
    unittest.main()
