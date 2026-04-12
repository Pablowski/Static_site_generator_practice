import unittest
from textnode import *
from inline_markdown import *

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ])
    
    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ])
    
    def test_code(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def multiple_delimiters(self):
        node = TextNode("**one** and **two**", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT)
        ])

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result,[
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT)
        ])

    def test_delimiter_at_end(self):
        node = TextNode("ends with **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result,[
            TextNode("ends with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ])
    
class Test_extract_markdown(unittest.TestCase):
    def test_extract_single_image(self):
        text = "![alt text](https://www.boot.dev/image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "https://www.boot.dev/image.png")])
    
    def test_extract_multiple_images(self):
        text = "![cat](https://cats.com/cat.png) and ![dog](https://dogs.com/dog.png)"
        self.assertEqual(extract_markdown_images(text), [
            ("cat", "https://cats.com/cat.png"),
            ("dog", "https://dogs.com/dog.png"),
        ])

    def test_extract_single_link(self):
        text = "[boot.dev](https://www.boot.dev)"
        self.assertEqual(extract_markdown_links(text), [("boot.dev", "https://www.boot.dev")])

    def test_extract_multiple_links(self):
        text = "[google](https://www.google.com) and [boot.dev](https://www.boot.dev)"
        self.assertEqual(extract_markdown_links(text), [
            ("google", "https://www.google.com"),
            ("boot.dev", "https://www.boot.dev"),
        ])
    
    def test_links_does_not_match_images(self):
        text = "![image](https://img.com/pic.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_images_does_not_match_links(self):
        text = "[just a link](https://www.boot.dev)"
        self.assertEqual(extract_markdown_images(text), [])

class Test_split_Images_links(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("Here is ![cat](https://cats.com/cat.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Here is ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://cats.com/cat.png"),
        ])

    def test_multiple_images(self):
        node = TextNode("![cat](https://cats.com) and ![dog](https://dogs.com)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("cat", TextType.IMAGE, "https://cats.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "https://dogs.com"),
        ])

    def test_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_single_link(self):
        node = TextNode("Visit [boot.dev](https://www.boot.dev) today", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Visit ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" today", TextType.TEXT),
        ])

    def test_multiple_links(self):
        node = TextNode("[google](https://google.com) and [boot.dev](https://boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("boot.dev", TextType.LINK, "https://boot.dev"),
        ])
    
    def test_no_links(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

class Test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes_order_1(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(result, [
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
        ])
        