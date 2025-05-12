import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        testnode = HTMLNode("a", "This is a test link.", None, {"href": "https://www.google.com", "target": "_blank"})
        expected_result = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(testnode.props_to_html(), expected_result)

    def test_properties(self):
        testnode = HTMLNode("a", "This is a test link.", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(testnode.tag, "a")
        self.assertEqual(testnode.value, "This is a test link.")
        self.assertEqual(testnode.children, None)
        self.assertEqual(testnode.props, {"href": "https://www.google.com", "target":"_blank"})

    def test_repr(self):
        testnode = HTMLNode("a", "This is a test link.", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(testnode.__repr__(), "HTMLNode(a, This is a test link., None,  href=\"https://www.google.com\" target=\"_blank\")")

if __name__ == "__main__":
    unittest.main()