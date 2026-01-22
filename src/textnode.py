from enum import Enum

from htmlnode import LeafNode
import re

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


# Paul
def markdown_to_htmlnode(old_nodes, delimiter, text_type):
    new_array = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_array.append(old_node)
            continue

        tmp_list = []
        splitted_old_nodes = old_node.text.split(delimiter)

        if len(splitted_old_nodes) % 2 == 0:  # Because then this means
            raise Exception("Invalid Syntax: Check the delimiter")

        for i in range(len(splitted_old_nodes)):
            if splitted_old_nodes[i] == "":
                continue
            if i % 2 == 0:
                tmp_list.append(TextNode(splitted_old_nodes[i], TextType.TEXT))
            else:
                tmp_list.append(TextNode(splitted_old_nodes[i], text_type))

        new_array.extend(tmp_list)

    return new_array

# Paul
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)


def split_nodes_image(old_nodes):
    new_array = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_array.append(old_node)
            continue

        the_text = old_node.text
        images = extract_markdown_images(the_text)

        if len(images) == 0:
            new_array.append(old_node)
            continue

        for image in images:
            text_splitted = the_text.split(f"![{image[0]}]({image[1]})",1)
            if len(text_splitted) != 2:
                raise Exception("Invalid Syntax: Check out for the closing brackets")
            if text_splitted[0] != "":
                new_array.append(TextNode(text_splitted[0], TextType.TEXT))
            new_array.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1]
                )
            )
            the_text = text_splitted[1]
        if the_text != "":
            new_array.append(TextNode(the_text,TextType.TEXT))
    return new_array


def split_nodes_link(old_nodes):
    new_array = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_array.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_array.append(old_node)
            continue

        for link in links:
            text_splitted = text.split(f"[{link[0]}]({link[1]})",1)
            if len(text_splitted) != 2:
                raise Exception("Invalid Syntax: Check out for the closing brackets")
            if text_splitted[0] != "":
                new_array.append(TextNode(text_splitted[0],TextType.TEXT))
            new_array.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1]
                )
            )
            text = text_splitted[1]
        if text != "":
            new_array.append(TextNode(text,TextType.TEXT))

    return new_array

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = markdown_to_htmlnode(nodes, "**", TextType.BOLD)
    nodes = markdown_to_htmlnode(nodes, "_", TextType.ITALIC)
    nodes = markdown_to_htmlnode(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
