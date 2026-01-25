from enum import Enum

from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(block):
    blocks = block.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(text_block):
    text_lines = text_block.split("\n")

    if text_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    elif len(text_lines)>1 and text_lines[0].startswith("```") and text_lines[-1].endswith("```"):
        return BlockType.CODE

    elif text_block.startswith("> "):
        for text_line in text_lines:
            if not text_line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    elif text_block.startswith("- "):
        for text_line in text_lines:
            if not text_line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    elif text_block.startswith("1. "):
        i = 1
        for text_line in text_lines:
            if not text_line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i+=1
        return BlockType.OLIST

    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    child_nodes = []
    md_blocks = markdown_to_blocks(markdown) 
    for block in md_blocks: 
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            tmp_list = []
            for line in lines:
                tmp_list.append(line.strip())
            block = " ".join(tmp_list)
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            html_node = ParentNode("p",html_nodes)
            child_nodes.append(html_node)
            
        if block_type == BlockType.HEADING:
            hash_count = 0
            for hash in block:
                if hash == "#":
                    hash_count += 1
                else:
                    break
            block = block[hash_count+1:]
            
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            html_node = ParentNode(f"h{hash_count}",html_nodes)
            child_nodes.append(html_node)
            
            
        if block_type == BlockType.CODE:
            block = block[4:-3]
            lines = block.split("\n")
            tmp_list = []
            for line in lines:
                tmp_list.append(line.strip())
            block = "\n".join(tmp_list)
            text_node = TextNode(block, TextType.TEXT)    
            html_node = text_node_to_html_node(text_node)
            html_node = ParentNode("code", [html_node])
            html_node = ParentNode("pre", [html_node])
            child_nodes.append(html_node)
            
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            tmp_list=[]
            for line in lines:
                tmp_list.append(line[2:].strip())
            block = "\n".join(tmp_list)
            text_nodes = text_to_textnodes(block)
            html_nodes=[]
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            html_node = ParentNode("blockquote",html_nodes)
            child_nodes.append(html_node)
            
            
        if block_type == BlockType.ULIST:
            lines = block.split("\n")
            html_nodes = []
            for line in lines:
                line = line[2:]
                text_nodes = text_to_textnodes(line)
                inner_html_nodes = []
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    inner_html_nodes.append(html_node)
                html_nodes.append(ParentNode("li",inner_html_nodes))
            html_node = ParentNode("ul",html_nodes)
            child_nodes.append(html_node)
            
        if block_type == BlockType.OLIST:
            lines = block.split("\n")
            html_nodes = []
            for line in lines:
                splits = line.split(". ",1)
                line = splits[1]
                text_nodes = text_to_textnodes(line)
                inner_html_nodes = []
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    inner_html_nodes.append(html_node)
                html_nodes.append(ParentNode("li",inner_html_nodes))
            html_node = ParentNode("ol",html_nodes)
            child_nodes.append(html_node)

    return ParentNode("div",child_nodes,None)