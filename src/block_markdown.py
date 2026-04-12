from enum import Enum
from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = ["\n".join(line.strip() for line in block.split("\n")) for block in blocks]
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNOREDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("#","##","###","#####","#####","######")):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in block.split("\n")):
        return "quote"
    elif all(line.startswith("- ")for line in block.split("\n")):
        return "unordered_list"
    elif all(line.startswith(f"{i + 1}. ")for i, line in enumerate(block.split("\n"))):
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            level = len(block.split(" ")[0])
            text = block[level + 1:]
            children.append(ParentNode(f"h{level}", text_to_children(text)))
        elif block_type == "code":
            text = block[3:-3].strip()
            children.append(ParentNode("pre", [ParentNode("code", text_to_children(text))]))
        elif block_type == "quote":
            text = "\n".join(line[1:].strip() for line in block.split("\n"))
            children.append(ParentNode("blockquote", text_to_children(text)))
        elif block_type == "unordered_list":
            items = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
            children.append(ParentNode("ul", items))
        elif block_type == "ordered_list":
            items = [ParentNode("li", text_to_children(line.split(". ", 1)[1]))for line in block.split("\n")]
            children.append(ParentNode("ol", items))
        else:
            text = block.replace("\n", " ")
            children.append(ParentNode("p", text_to_children(text)))
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
