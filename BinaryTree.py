from Node import Node
import numpy as np

np.random.seed(0)

# constants
LEFT = "L"
RIGHT = "R"


class BinaryTree(object):
    def __init__(self, depth, b, tau):
        """
        Initializes a new tree.
        :param depth: Integer denoting the depth of the tree.
        :param b: Integer denoting the parameter B for the value x_i.
        :param tau: Integer denoting the parameter tau for the value x_i.
        """
        self.depth = depth
        self.root = self.build_tree(Node(), depth)
        self.leaves = self.get_leaves()
        self.target = self.get_random_target()
        self.compute_leaves_values(b, tau)

    def build_tree(self, node, depth):
        """
        Builds the tree.
        :param node: Node object to expand.
        :param depth: Integer denoting the remaining depth of the tree to expand.
        :return: Node object denoting the root of the tree.
        """
        if depth == 0:
            return node
        else:
            node.left_child = self.build_tree(Node(direction=LEFT, parent=node), depth - 1)
            node.right_child = self.build_tree(Node(direction=RIGHT, parent=node), depth - 1)
            return node

    def get_leaves(self):
        """
        Returns a list of all leaves in the tree.
        :return: List of all leaves in the tree.
        """
        leaves = []
        nodes = [self.root]
        for d in range(self.depth+1):
            for node in nodes:
                if node.is_terminal():
                    leaves.append(node)
            if d < self.depth:
                new_nodes = []
                for node in nodes:
                    new_nodes.append(node.left_child)
                    new_nodes.append(node.right_child)
                nodes = new_nodes
        return leaves

    def get_random_target(self):
        """
        Returns a random target from the tree leaves.
        :return: Node object denoting the random target.
        """
        return np.random.choice(self.leaves)

    def compute_distance(self, address):
        """
        Computes the edit-distance to the target.
        :param address: String denoting the address of the node.
        :return: Integer denoting the edit-distance to the target.
        """
        return sum(1 for a, b in zip(address, self.target.address) if a != b)

    def compute_leaves_values(self, b, tau):
        """
        Computes the values of the leaves based on the distance from the target leaf.
        :param b: Integer denoting the parameter B for the x_i.
        :param tau: Integer denoting the parameter tau for the x_i.
        """
        for leaf in self.leaves:
            leaf.value = b * np.exp(-self.compute_distance(leaf.address)/tau)

    def update_root(self, direction):
        """
        Updates the root of the tree.
        :param address: String denoting the direction to choose for the new root.
        """
        # decrease the depth of the tree
        self.depth = self.depth - 1
        # update the root
        if direction == LEFT:
            self.root = self.root.left_child
        elif direction == RIGHT:
            self.root = self.root.right_child
        else:
            raise ValueError("Direction must be either R or L.")

    def __repr__(self):
        """
        Returns a string representation of the tree.
        :return: String representation of the tree.
        """
        tree_string = ""
        nodes = [self.root]
        for d in range(self.depth+1):
            tree_string += f"Depth {d}: {nodes}\n"

            if d < self.depth:
                new_nodes = []
                for node in nodes:
                    new_nodes.append(node.left_child)
                    new_nodes.append(node.right_child)
                nodes = new_nodes
        return tree_string



