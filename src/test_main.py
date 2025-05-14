import unittest

from main import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType

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

if(__name__ == "__main__"):
    unittest.main()