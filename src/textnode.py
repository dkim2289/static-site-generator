from enum import Enum
from this import d

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
– Check on Dan's codes <- (by Thurs 5pm)
"""

""" (wink)(thumbs up)
EDGES
1. given node is not TextType.TEXT as-is -> adding the list as-is
ex. node = TextNode("**blabla**", TextType.BOLD)
2. no closing delimiter ->
ex. node = TextNode("blablal **BLAAAA! ", TextType.BOLD)
3. no text -> skip
ex. node = TextNode("blabla **** blabla", TextType.BOLD)

PSEUDO
params = array(of TextNodes) // delimiter // test_type
ouputs = array(of separated TextNodes)

0. oup_list = []
1. loop the TextNodes -> check the texttype (EDGE1)
2. split each node into parts
3. identify parts -> if part numb is odd -> (EDGE2)
4. identified parts into tmp arrays
5. tmp arrays to oup_list
"""

# def blabla(oldN, delim, tt):
#     oup=[]
#     for node in oldN:
#         if node.text_type != TextType.TEXT:
#             oup.append(node)
#             continue
#         parts =[]
#         parted = oldN.text.split(delim)
#         if len(parted) % 2 == 0:
#             raise Exception("Invalid Syntax")
#         for i in range(len(parted)):
#             if parted[i]=="":
#                 continue
#             if i % 2 == 0:
#                 parts.append(TextNode(parted[i],TextType.TEXT)
#             else:
#                 parts.append(TextNode(parted[i],tt))
#         oup.extend(parts)
#     return oup


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
