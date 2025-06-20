import unittest

from markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_node_images,
    split_node_links,
    text_to_textnodes,
    markdown_to_blocks,
    text_to_children,
    markdown_to_html_node,
    extract_title,
)

from textnode import (
    TextNode,
    TextType,
)

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

class TestMarkdown(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_node_images([node])
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
        node = TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_node_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_text_to_testnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected_result)

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

    def test_text_to_children(self):
        text = "This is a **bolded** paragraph with an _italic_ word."
        html = text_to_children(text)
        expected_result = [
            HTMLNode(None, "This is a ", None, None),
            HTMLNode("b", "bolded", None, None),
            HTMLNode(None, " paragraph with an ", None, None),
            HTMLNode("i", "italic",None, None),
            HTMLNode(None, " word.", None, None)
        ]
        self.assertEqual(html, expected_result)

    def test_ordered_list(self):
        text = "1. Preheat oven to **400**\n2. Bake pizza for _15 minutes_\n3. Enjoy"
        node = markdown_to_html_node(text)
        html = node.to_html()
        expected_result = "<div><ol><li>Preheat oven to <b>400</b></li><li>Bake pizza for <i>15 minutes</i></li><li>Enjoy</li></ol></div>"
        self.assertEqual(html, expected_result)

    def test_unordered_list(self):
        text = "- Preheat oven to **400**\n- Bake pizza for _15 minutes_\n- Enjoy"
        node = markdown_to_html_node(text)
        html = node.to_html()
        expected_result = "<div><ul><li>Preheat oven to <b>400</b></li><li>Bake pizza for <i>15 minutes</i></li><li>Enjoy</li></ul></div>"
        self.assertEqual(html, expected_result)

    def test_quote(self):
        text = "> To be or _not_ to be,\n> that **is** the question."
        node = markdown_to_html_node(text)
        html = node.to_html()
        expected_result = "<div><blockquote>To be or <i>not</i> to be,\nthat <b>is</b> the question.</blockquote></div>"
        self.assertEqual(html, expected_result)

    def test_heading(self):
        text = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(text)
        html = node.to_html()
        expected_result = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected_result)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        text = """
This is a test line.

# This is a test header.

This is another test line.
"""
        title = extract_title(text)
        expected_result = "This is a test header."
        self.assertEqual(title, expected_result)

    def test_extract_title_exception(self):
        text = """
This is a test line.

This is another test line.
"""
        try:
            title = extract_title(text)
        except:
            title = "Exception thrown"
        expected_result = "Exception thrown"
        self.assertEqual(title, expected_result)

if __name__ == "__main__":
    unittest.main()