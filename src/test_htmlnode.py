import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

class TestHTMLNode(unittest.TestCase):
    def test_constructor(self):
        node = HTMLNode("a", "This is a link", None, {"href": "https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is a link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://boot.dev"})

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), " href=\"https://boot.dev\"")

    def test_html_node_to_string(self):
        node = HTMLNode("p", "This is a paragraph", None, None)
        node_string = "HTMLNode(p, This is a paragraph, None, None)"
        self.assertEqual(str(node), node_string)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_string(self):
        node = LeafNode("p", "This is a paragraph")
        node_string = "HTMLNode(p, This is a paragraph, None, None)"
        self.assertEqual(str(node), node_string)
    
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_result)

if __name__ == "__main__":
    unittest.main()