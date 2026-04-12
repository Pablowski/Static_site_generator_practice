from block_markdown import *
import unittest

class Test_block_markdown(unittest.TestCase):

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

class Test_block_to_block_type(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Heading 2"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")

    def test_code(self):
        self.assertEqual(block_to_block_type("```print('hello')```"), "code")

    def test_quote(self):
        self.assertEqual(block_to_block_type(">this is a quote\n>another line"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one\n- item two\n- item three"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item one\n2. item two\n3. item three"), "ordered_list")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just a plain paragraph"), "paragraph")


class Test_markdown_to_html_node(unittest.TestCase):
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