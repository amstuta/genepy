class Node:
    """
    Represents a node / leaf in a tree.
    :param value:       The value that this node holds
    :param prev_node:   The previous node in the tree
    """

    def __init__(self, value, prev_node):
        self.value = value
        self.prev = prev_node
        self.next_left = None
        self.next_right = None


    def set_children(self, left, right):
        """
        Sets the children of this node.
        :param left:    The left child
        :param right:   The right child
        """
        self.next_left = left
        self.next_right = right


    def calc(self, feature):
        """
        Calculates the output of this node. If the node is a leaf,
        returns self.value; otherwise returns the result of the function contained
        in self.value called with the results from the children.
        :param variables:   The variables that can be used in the tree
        """
        if isinstance(self.value, int):
            return self.value
        elif isinstance(self.value, str):
            return feature[int(self.value)]
        else:
            left = self.next_left.calc(feature)
            right = self.next_right.calc(feature)
            return self.value(left, right)


    def __repr__(self):
        if isinstance(self.value, str):
            return 'Variable: {}'.format(self.value)
        elif isinstance(self.value, int):
            return 'Constant: {}'.format(self.value)
        else:
            return 'Function: {}'.format(self.value)
