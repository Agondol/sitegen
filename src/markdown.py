import re

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)

from blocktype import (
    BlockType,
    block_to_block_type,
)

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for o in old_nodes:
        if o.text_type == TextType.TEXT:
            text = o.text.split(delimiter)
            for i, t in enumerate(text):
                if t == "":
                    continue
                if i % 2 == 2:
                    if t:
                        new_nodes.append(TextNode(t, TextType.TEXT))
                elif i % 2 == 1:
                    if t:
                        new_nodes.append(TextNode(t, text_type))
                else:
                    if t:
                        new_nodes.append(TextNode(t, TextType.TEXT))
        else:
            new_nodes.append(o)
    return new_nodes

def extract_markdown_images(text):
    images = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for m in matches:        
        images.append((m[0], m[1]))
    return images

def extract_markdown_links(text):
    links = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    for m in matches:        
        links.append((m[0], m[1]))
    return links

def split_node_images(old_nodes):
    new_nodes = []
    for o in old_nodes:
        if o.text_type == TextType.TEXT:
            images = extract_markdown_images(o.text)
            text = o.text
            if len(images) == 0:
                new_nodes.append(o)
                continue
            for i in images:            
                split_text = text.split(f"![{i[0]}]({i[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
                text = split_text[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(o)
    return new_nodes


def split_node_links(old_nodes):
    new_nodes = []
    for o in old_nodes:
        if o.text_type == TextType.TEXT:
            links = extract_markdown_links(o.text)
            text = o.text
            if len(links) == 0:
                new_nodes.append(o)
                continue
            for l in links:            
                split_text = text.split(f"[{l[0]}]({l[1]})", 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(l[0], TextType.LINK, l[1]))
                text = split_text[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(o)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    node = split_nodes_delimiter([node], "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_node_images(node)
    node = split_node_links(node)
    return node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for b in blocks:
        new_block = b.strip()
        if new_block == "":
            continue
        new_blocks.append(new_block)
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = []
    for b in blocks:
        block_type = block_to_block_type(b)
        match(block_type):
            case BlockType.PARAGRAPH:
                html.append(ParentNode("p", text_to_children(b)))
            case BlockType.CODE:
                code_block = []
                split_block = b.replace("```", "").split('\n')
                for l in split_block:
                    if l == "":
                        continue
                    code_block.append(l)
                code_block_string = ("\n".join(code_block)) + "\n"
                html.append(ParentNode("pre", [LeafNode("code", code_block_string)]))
            case BlockType.QUOTE:
                html.append(ParentNode("blockquote", text_to_children(b)))
            case BlockType.ORDERED_LIST:
                html.append(ParentNode("ol", text_to_ordered_list(b)))
            case BlockType.UNORDERED_LIST:
                html.append(ParentNode("ul", text_to_unordered_list(b)))
            case BlockType.HEADING:
                text_to_heading(b)
    return ParentNode("div", html)

def text_to_children(text):
    nodes = text_to_textnodes(text.replace("\n", " "))
    new_nodes = []
    for n in nodes:
        new_nodes.append(text_node_to_html_node(n))
    return new_nodes

def text_to_heading(text):
    pass

def text_to_ordered_list(text):
    nodes = text_to_textnodes(text)
    new_nodes = []

def text_to_unordered_list(text):
    pass