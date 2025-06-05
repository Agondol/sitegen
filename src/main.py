import os
import re
import shutil

from blocktype import (
    BlockType,
)

from htmlnode import (
    HTMLNode,
)

from leafnode import (
    LeafNode,
)

from textnode import(
    TextNode,
    TextType,
)

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

def block_to_block_type(block):
    quote_count = 0
    unordered_list_count = 0
    ordered_list_count = 0
    for l in block:
        if re.match(r"#{1,6}", l) != None:
            return BlockType.HEADING
        if re.match(r"`.*`", l) != None:
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

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

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
        new_blocks.append('\n'.join(new_lines))
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for b in blocks:
        match(block_to_block_type(b)):
            case BlockType.PARAGRAPH:
                new_node = HTMLNode("p", b, text_to_children(b))
            case BlockType.HEADING:
                new_node = HTMLNode("h1", b, text_to_children(b))
            case BlockType.CODE:
                text_node = TextNode(b, TextType.CODE)
                new_node = HTMLNode("code", b, text_node_to_html_node(text_node))
            case BlockType.QUOTE:
                new_node = HTMLNode("q", b, text_to_children(b))
            case BlockType.UNORDERED_LIST:
                new_node = HTMLNode("ul", b, text_to_children(b))
            case BlockType.ORDERED_LIST:
                new_node = HTMLNode("ol", b, text_to_children(b))
        nodes.append(new_node)
    return HTMLNode("div", None, nodes)

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

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for n in nodes:
        html_nodes.append(text_node_to_html_node(n))
    return html_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

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

if __name__ == "__main__":
    main()