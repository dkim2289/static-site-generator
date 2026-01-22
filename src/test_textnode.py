import unittest

from textnode import (
    TextType,
    TextNode,

    text_node_to_html_node,
    markdown_to_htmlnode,

    extract_markdown_images,
    extract_markdown_links,

    split_nodes_image,
    split_nodes_link,
)


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
- import done
- use assertListEqual (https://docs.python.org/3/library/unittest.html)

- almost ran out of sparking water, almond milk, olives
- Costco this weekend
"""

# Paul
class MarkdownToHTMLNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("testing ** bold ** texts",TextType.TEXT)
        new_nodes = markdown_to_htmlnode([node],"**",TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("testing ", TextType.TEXT),
                TextNode(" bold ", TextType.BOLD),
                TextNode(" texts", TextType.TEXT),
            ],
            new_nodes
        )

    def test_bold_double(self):
        def test_double_bolds(self):
            node = TextNode("testing ** double ** bold ** texts ** now.",TextType.TEXT)
            new_nodes = markdown_to_htmlnode([node],"**",TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("testing ", TextType.TEXT),
                    TextNode(" double ", TextType.BOLD),
                    TextNode("  bold ", TextType.TEXT),
                    TextNode(" texts ", TextType.BOLD),
                    TextNode(" now.", TextType.TEXT),
                ],
                new_nodes
            )

    def test_italic(self):
        def test_italic(self):
            node = TextNode("testing ** italic ** texts",TextType.TEXT)
            new_nodes = markdown_to_htmlnode([node],"*",TextType.ITALIC)
            self.assertListEqual(
                [
                    TextNode("testing ", TextType.TEXT),
                    TextNode(" italic ", TextType.ITALIC),
                    TextNode(" texts", TextType.TEXT),
                ],
                new_nodes
            )

    def test_bold_and_italic(self):
        def test_bold_and_italic(self):
            node = TextNode("testing ** both ** bold * and * italic fonts",TextType.TEXT)
            new_nodes = markdown_to_htmlnode([node],"**",TextType.BOLD)
            new_nodes = markdown_to_htmlnode([new_nodes],"*",TextType.ITALIC)
            self.assertListEqual(
                [
                    TextNode("testing ", TextType.TEXT),
                    TextNode(" both ", TextType.BOLD),
                    TextNode(" bold ", TextType.TEXT),
                    TextNode(" and ", TextType.ITALIC),
                    TextNode(" italic fonts ", TextType.TEXT),
                ],
                new_nodes
            )

    def test_code(self):
        def test_code(self):
            node = TextNode("testing ` code ` texts",TextType.TEXT)
            new_nodes = markdown_to_htmlnode([node],"`",TextType.CODE)
            self.assertListEqual(
                [
                    TextNode("testing ", TextType.TEXT),
                    TextNode(" code ", TextType.CODE),
                    TextNode(" texts", TextType.TEXT),
                ],
                new_nodes
            )


    def test_last_word(self):
        def test_last_word(self):
            node = TextNode("testing last ** words **",TextType.TEXT)
            new_nodes = markdown_to_htmlnode([node],"**",TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("testing last ", TextType.TEXT),
                    TextNode(" words ", TextType.BOLD),
                    TextNode("", TextType.TEXT),
                ],
                new_nodes
            )

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

    def test_double_image_extraction(self):
        match = extract_markdown_images("testing for double image extraction ![example1](firstimage.jpg) and here's the second ![example2](secondiamge.jpg)")
        self.assertListEqual(
            [
                ("example1","firstimage.jpg"),
                ("example2","secondiamge.jpg"),
            ],
            match
        )

    def test_extract_markdown_links(self):
        match = extract_markdown_links("texting link extraction [here we go](https://www.hereisthelink.com)")
        self.assertListEqual(
            [
                ("here we go", "https://www.hereisthelink.com"),
            ],
            match
        )

    def test_double_link_extraction(self):
        match = extract_markdown_links("testing double link extraction [example1](https://www.example1.com) and here's the second [example2](https://www.example2.com)")
        self.assertListEqual(
            [
                ("example1","https://www.example1.com"),
                ("example2","https://www.example2.com"),
            ],
            match
        )
        
class TestImgExtractionThenSeparation(unittest.TestCase):
    def test_basic_two_parts(self):
        node = TextNode("A photo of a dog! ![dog](src/img/lovely_dog.jpg)",TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A photo of a dog! ",TextType.TEXT),
                TextNode("dog",TextType.IMAGE,"src/img/lovely_dog.jpg"),
            ],
            new_node
        )
        
    def test_basic_three_parts(self):
        node = TextNode("A photo of a dog! ![dog](src/img/lovely_dog.jpg) and there's more texts",TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A photo of a dog! ",TextType.TEXT),
                TextNode("dog",TextType.IMAGE,"src/img/lovely_dog.jpg"),
                TextNode(" and there's more texts",TextType.TEXT),
            ],
            new_node
        )
        
    def test_two_images(self):
        node = TextNode("A photo of a dog! ![dog](src/img/lovely_dog.jpg) and there's more texts ![look](src/img/one_more_img.jpg)and there's more texts here",TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A photo of a dog! ",TextType.TEXT),
                TextNode("dog",TextType.IMAGE,"src/img/lovely_dog.jpg"),
                TextNode(" and there's more texts ",TextType.TEXT),
                TextNode("look",TextType.IMAGE,"src/img/one_more_img.jpg"),
                TextNode("and there's more texts here",TextType.TEXT)
            ],
            new_node
        )
    
    
        

if __name__ == "__main__":
    unittest.main()
