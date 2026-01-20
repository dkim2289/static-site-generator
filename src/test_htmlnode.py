import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    # HTMLNode Tests
    def test_props_to_html(self):
        node = HTMLNode(
            "p",
            None,
            [HTMLNode(tag="p", value="Hello")],
            {"src": "photo.jpg", "alt": "A beautiful sunset"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' src="photo.jpg" alt="A beautiful sunset"')

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "I wish I could read"
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(
            node.to_html(),
            "Hello, World!"
        )


class TestParentNode(unittest.TestCase):
    def no_val(self):
        node = ParentNode(None, None)
        self.assertEqual(node.to_html(),"No Tag")

    def no_child(self):
        node = ParentNode("p",None)
        self.assertEqual(node.to_html(),"No Children")

    def one_child(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode("div",[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>",
        )

    def multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b","Bold text"),
                LeafNode(None,"Normal text"),
                LeafNode("i","italic text"),
                LeafNode(None,"Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def grandchildren(self):
        grandchildren_node = LeafNode("b","grandchlid")
        child_node = ParentNode("span",[grandchildren_node])
        parent_node = ParentNode("div",[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )


    def headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__=="__main__":
    unittest.main()
