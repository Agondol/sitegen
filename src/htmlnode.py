class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html = ""
        for p in self.props:
            html += f" {p}=\"{self.props[p]}\""
        return html
    
    def __eq__(self, node):
        if self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props:
            return True
        return False
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children == None:
            raise ValueError("All parent nodes must have children.")
        html = f"<{self.tag}{self.props_to_html()}>"
        for c in self.children:
            html += c.to_html()
        html += f"</{self.tag}>"
        return html