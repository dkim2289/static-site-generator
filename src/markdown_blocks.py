def markdown_to_blocks(text):
    blocks = []
    separated_texts = text.split("\n\n")
    for separated_text in separated_texts:
        if separated_text == "":
            continue
        blocks.append(separated_text.strip())
    return blocks