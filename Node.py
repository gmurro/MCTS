class Node(object):
    def __init__(self, direction="", parent=None, left_child=None, right_child=None):
        """
        Initializes a node.
        :param direction: Direction that leads to the node. Can be "L" or "R".
        :param parent: Pointer to the parent node.
        :param left_child: Pointer to the left child node.
        :param right_child: Pointer to the right child node.
        """
        self.direction = direction
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.address = self.get_address()
        self.value = 0


    def get_address(self):
        """
        Returns the address of the node.
        :return: String denoting the address of the node.
        """
        if self.is_root():
            return "0"
        else:
            return self.parent.address[1:] + self.direction if self.parent.is_root() else self.parent.address + self.direction

    def is_terminal(self):
        """
        Returns whether the node is a leaf node.
        :return: Boolean denoting whether the node is a leaf node.
        """
        return self.left_child is None and self.right_child is None

    def is_root(self):
        """
        Returns whether the node is a root node.
        :return: Boolean denoting whether the node is a root node.
        """
        return self.parent is None

    def __gt__(self, other):
        """
        Returns whether the node is greater than the other node.
        :param other: Other node.
        :return: Boolean denoting whether the node is greater than the other node.
        """
        return self.value > other.value

    def __lt__(self, other):
        """
        Returns whether the node is less than the other node.
        :param other: Other node.
        :return: Boolean denoting whether the node is less than the other node.
        """
        return self.value < other.value

    def __str__(self):
        return f"{self.address}"

    def __repr__(self):
        return f"{self.address} ({self.value:.1f})"


