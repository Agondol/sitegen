from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if(self.value == None or self.value == ""):
            raise ValueError("All leaf nodes must have a value.")
        if(self.tag == None or self.value == ""):
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"