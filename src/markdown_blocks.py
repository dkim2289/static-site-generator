from enum import Enum

from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode
import os

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

    elif text_block.startswith(">"):
        for text_line in text_lines:
            if not text_line.startswith(">"):
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

# this function pulls the h1 header from a darkdown file
def extract_title(markdown):
    # the whole markdown file into blocks
    blocks = markdown_to_blocks(markdown)
    # for each block
    for block in blocks:
        # firstly, strip it.
        block = block.strip()
        # if its type is Heading,
        if block_to_block_type(block) == BlockType.HEADING:
            # and it has a single #
            if block[0:2] == "# ":
                # return the content
                return (block[2:]).strip()
    # after loop, nothing's returned, raise an error
    raise Exception("Error: The line should start with '#")

# This function generates a page. It takes a markdown file, a template file, and a destination path as input.
def generate_page(from_path, template_path, dest_path, basepath):
    # print a msg of what it does
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read the markdown file
    with open(from_path, "r") as f:
        # store the content in a variable
        content = f.read()
    # read the template file
    with open(template_path, "r") as f:
        # store the template in a variable
        template = f.read()
    # use markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string
    html_content = markdown_to_html_node(content).to_html()
    # use extract_title function to grab the title
    title = extract_title(content)
    # replace the placeholder in the template with the title and html
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    ## replace any instances of 1) href="/ with href="{basepath}
    output = output.replace('href="/', f'href="{basepath}')
    ## 2) src="/ with src="{basepath}
    output = output.replace('src="/', f'src="{basepath}')

    # Be sure to create any necessary directories if they don't exist
    dirpath = os.path.dirname(dest_path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    # then write the new full HTML page to a file at dest_path.
    with open(dest_path, "w") as f:
        f.write(output)

# this function generate pages recursively. Inp : dir_path_content, template_path, dest_dir_path
# tips:
# os.listdir()
# os.path.join() -> only works for full paths
# os.path.isfile() -> only works for full paths
# pathlib.Path
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # get every entries
    entries = os.listdir(dir_path_content)
    # for each entry
    for entry in entries:
        # get full paths for os functions
        full_path = os.path.join(dir_path_content, entry)
        # for each md file found
        if os.path.isfile(full_path) and entry.endswith(".md"):
            # generate a new .html file
            generate_page(
                full_path,
                template_path,
                os.path.join(dest_dir_path, entry.replace(".md", ".html")),
                basepath
            )
        # if entry is a dir
        elif os.path.isdir(full_path):
            # generate pages recursively
            generate_pages_recursive(
                full_path,
                template_path,
                os.path.join(dest_dir_path, entry),
                basepath
            )
