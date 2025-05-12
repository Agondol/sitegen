from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.content)
        case TextType.BOLD:
            return LeafNode("b", text_node.content)
        case TextType.ITALIC:
            return LeafNode("i", text_node.content)
        case TextType.CODE:
            return LeafNode("code", text_node.content)
        case TextType.LINK:
            return LeafNode("a", text_node.content, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.content})

main()