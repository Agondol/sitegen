from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    quote_count = 0
    unordered_list_count = 0
    ordered_list_count = 0
    for l in block:
        if re.match(r"#{1,6}", l) != None:
            return BlockType.HEADING
        if re.match(r"```.*```", l) != None:
            return BlockType.CODE
        if re.match(r">", l) != None:
            quote_count += 1
            continue
        if re.match(r"- ", l) != None:
            unordered_list_count += 1
            continue
        matches = re.match(r"(\d)\. ", l)
        if  matches != None and matches.groups()[0] == str(ordered_list_count + 1):
            ordered_list_count += 1
    if quote_count == len(block):
        return BlockType.QUOTE
    if unordered_list_count == len(block):
        return BlockType.UNORDERED_LIST
    if ordered_list_count == len(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
