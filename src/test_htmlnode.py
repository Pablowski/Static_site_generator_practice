import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "click me",[], {"href": "https://www.boot.dev", "class": "link"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" class="link"')

    def test_default_children_and_props(self):
        node = HTMLNode("div","Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    
    def test_repr(self):
        node = HTMLNode("div", "Hello", [], {})
        self.assertEqual(repr(node), "HTMLNode(tag = div, value = Hello, children = [], props = {})")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grand_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
        

    
if __name__ == "__main__":
    unittest.main()