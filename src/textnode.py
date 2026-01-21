from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Not a valid text type")


""" for PAUL
– By Fri 14:00 pls. Thx Mate! 
– Convert Function (from a Markdown Strings to TextNodes), and
– Test Cases, and
– Check on Dan's codes <- (by Thurs 5pm), and
– Scrum at Fri 16:00
"""

""" (wink)(thumbs up)
EDGES
1. given node is not Textext_typeype.TEXT as-is -> adding the list as-is
ex. node = TextNode("**blabla**", Textext_typeype.BOLD)
2. no closing delimiteriter ->
ex. node = TextNode("blablal **BLAAAA! ", Textext_typeype.BOLD)
3. no text -> skip
ex. node = TextNode("blabla **** blabla", Textext_typeype.BOLD)

PSEUDO
params = array(of TextNodes) // delimiteriter // test_type
new_nodesuts = array(of separated TextNodes)

0. new_nodes_list = []
1. loop the TextNodes -> check the textext_typeype (EDGE1)
2. split each node into parts
3. identify parts -> if part numb is odd -> (EDGE2)
4. identified parts into tmp arrays
5. tmp arrays to new_nodes_list
"""

def markdown_to_htmlnode(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: # EDGE 1
            new_nodes.append(node)
            continue

        splitted_sections = []
        splitting = node.text.split(delimiter)

        if len(splitting) % 2 == 0: # EDGE 2
            raise Exception("Invalid Syntax -> Check delimiteriters")

        for i in range(len(splitting)):
            if i % 2 == 0:
                splitted_sections.append(TextNode(splitting[i],TextType.TEXT))
            else:
                splitted_sections.append(TextNode(splitting[i],text_type))
        new_nodes.extend(splitted_sections)

    return new_nodes
