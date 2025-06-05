import re
import os
import shutil
from textnode import TextNode, TextType
from leafnode import LeafNode
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode

def main():
#     text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#     print(f"text {text}")
#     nodes = text_to_textnodes(text)
#     print(f"nodes: {nodes}")
#     md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
# """
#     print(f"md: {md}")
#     blocks = markdown_to_blocks(md)
#     print(f"blocks: {blocks}")
#     block_types = []
#     for b in blocks:
#         block_types.append(block_to_block_type(b))
#     print(f"block_types: {block_types}")
    source = "/home/agondol/Documents/Courses/BootDev/sitegen/static"
    destination = "/home/agondol/Documents/Courses/BootDev/sitegen/public"
    copy_files(source, destination)

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):    
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            split_node = node.content.split(delimiter)
            for i, part in enumerate(split_node):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, TextType.NORMAL))
                else:
                    if part:
                        new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            images = extract_markdown_images(node.content)
            text = node.content
            if len(images) == 0:
                new_nodes.append(node)
                continue
            for i in images:
                split_nodes = text.split(f"![{i[0]}]({i[1]})", 1)
                if split_nodes[0] != "":
                    new_nodes.append(TextNode(split_nodes[0], TextType.NORMAL))
                new_nodes.append(TextNode(i[0], TextType.IMAGE, i[1]))
                text = split_nodes[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            links = extract_markdown_links(node.content)
            text = node.content
            if len(links) == 0:
                new_nodes.append(node)
                continue
            for l in links:
                split_nodes = text.split(f"[{l[0]}]({l[1]})", 1)
                if split_nodes != "":
                    new_nodes.append(TextNode(split_nodes[0], TextType.NORMAL))
                new_nodes.append(TextNode(l[0], TextType.LINK, l[1]))
                text = split_nodes[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []
    for b in blocks:
        lines = b.split('\n')
        new_lines = []
        for l in lines:
            strip_l = l.strip()
            if strip_l == "":
                continue
            new_lines.append(strip_l)
        new_blocks.append(new_lines)
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for b in blocks:
        match(block_to_block_type(b)):
            case BlockType.PARAGRAPH:
                nodes.append(HTMLNode())

def copy_files(source, destination):
    #delete files in the destination
    if os.path.exists(destination):
        files = os.listdir(destination)
        for file in files:
            path = f"{destination}/{file}"
            if os.path.isfile(path):
                os.remove(path)
                print(f"Removed {path}")
            else:
                shutil.rmtree(f"{destination}/{file}")
                print(f"Removed {path}/*")
    else:
        raise FileNotFoundError(f"{destination} doesn't exist")
    
    #copy source files to destination recursively
    if os.path.exists(source):
        files = os.listdir(source)
        for file in files:
            source_path = f"{source}/{file}"
            destination_path = f"{destination}/{file}"
            if os.path.isfile(source_path):
                result_path = shutil.copy(source_path, destination_path)
                print(f"{result_path} copied.")                
            else:
                os.mkdir(destination_path)
                copy_files(source_path, destination_path)
    else:
        raise FileNotFoundError(f"{source} doesn't exist")
    
if __name__ == "__main__":
    main()