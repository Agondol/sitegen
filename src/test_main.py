import unittest

from main import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    markdown_to_blocks,
)

from textnode import TextNode, TextType
from blocktype import BlockType, block_to_block_type

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a 'code block' word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.NORMAL), TextNode("code block", TextType.CODE),TextNode(" word", TextType.NORMAL),])

    def test_split_beginning(self):
        node = TextNode("**Sample** this", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Sample", TextType.BOLD),
            TextNode(" this", TextType.NORMAL),
        ])

    def test_split_middle(self):
        node = TextNode("Say, **Sample** this", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Say, ", TextType.NORMAL),
            TextNode("Sample", TextType.BOLD),
            TextNode(" this", TextType.NORMAL),
        ])

    def test_split_ending(self):
        node = TextNode("This **sample**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.NORMAL),
            TextNode("sample", TextType.BOLD),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )

def test_split_links(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ],
        new_nodes,
    )

def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

    def test_block_to_block_type_heading_one(self):
        md = """
# I am a heading
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_two(self):
        md = """
## I am a heading
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_three(self):
        md = """
### I am a heading
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_four(self):
        md = """
#### I am a heading
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_five(self):
        md = """
##### I am a heading
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_six(self):
        md = """
###### I am a heading
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = """
```I am a code```
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = """
>I am a quote
>What can I say?
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = """
- bread
- peanut butter
- jelly
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        md = """
1. Boil Water
2. Add noodles
3. Strain
4. Add milk, butter, and cheese sauce
5. Stir
"""
        block_type = block_to_block_type([md])
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

if(__name__ == "__main__"):
    unittest.main()