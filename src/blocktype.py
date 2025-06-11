import enum
import re

class BlockType(enum.Enum):
    PARAGRAPH = "paragrah"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r"#{1,6} .*", block):
        return BlockType.HEADING
    if re.match(r"`{3}(.|\n)*`{3}", block):
        return BlockType.CODE
    quote = True
    unordered_list = True
    ordered_list = True
    lines = block.split("\n")
    for i, l in enumerate(lines):
        if not re.match(r">.*", l):
            quote = False
        if not re.match(r"- .*", l):
            unordered_list = False
        matches = re.match(r"(\d+)\. ", l)
        if not matches:
            ordered_list = False
            continue
        if matches[1] != str(i + 1):
            ordered_list = False
    if quote == True:
        return BlockType.QUOTE
    if unordered_list == True:
        return BlockType.UNORDERED_LIST
    if ordered_list == True:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    