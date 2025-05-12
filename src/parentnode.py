from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if(self.tag is None):
            raise ValueError("Tag value must be set.")
        if(self.children is None):
            raise ValueError("ParentNode must have children.")
        node_beginning = f"<{self.tag}{self.props_to_html()}>"
        node_ending = f"</{self.tag}>"
        node_children = ""
        for c in self.children:
            node_children += c.to_html()
        return node_beginning + node_children + node_ending
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"