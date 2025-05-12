from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD   = "bold"
    ITALIC = "italic"
    CODE   = "code"
    LINK   = "link"
    IMAGE  = "image"

class TextNode:
    def __init__(self, content, text_type, url = None):
        self.content = content
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        return (self.content == text_node.content and self.text_type == text_node.text_type and self.url == text_node.url)
        
    def __repr__(self):
        return f"TextNode({self.content}, {self.text_type.value}, {self.url})"

