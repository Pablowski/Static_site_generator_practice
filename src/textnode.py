from enum import Enum

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text 
            and self.type == other.type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6   