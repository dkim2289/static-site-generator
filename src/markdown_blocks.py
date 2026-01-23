from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(text):
    blocks = []
    separated_texts = text.split("\n\n")
    for separated_text in separated_texts:
        if separated_text == "":
            continue
        blocks.append(separated_text.strip())
    return blocks


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
