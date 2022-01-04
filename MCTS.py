import numpy as np
from BinaryTree import BinaryTree
from BinaryTree import LEFT, RIGHT


class NodeMCTS:
    """
    Node class for MCTS
    """
    def __init__(self, state, parent=None):
        """
        Initialize the MCTS node.
        :param state: Node instance from the BinaryTree
        :param parent: Pointer to the parent NodeMCTS
        """
        self.state = state
        self.parent = parent
        self.children = []
        self.total_value = 0
        self.visits = 0

    def get_avg_value(self):
        """"
        This function return the ratio between total score and visits
        :return: a float value
        """
        if self.visits == 0:
            return 0
        else:
            return self.total_value / self.visits

    def is_leaf(self):
        """
        This function checks if the node is a leaf node in the snowcap of MCTS tree
        :return: boolean indicating if the node is a leaf node
        """
        return len(self.children) == 0

    def __repr__(self):
        """
        This function returns a string representation of the MCTS node
        :return: a string
        """
        return f"{self.state.address} ({self.total_value}/{self.visits})"


class MCTS(object):
    """
    MCTS class
    """
    def __init__(self, c=2, max_iterations=50):
        """
        Initialize the MCTS.
        :param c: value indicating the exploration factor
        :param max_iterations: maximum number of MCTS iterations
        """
        self.c = c
        self.max_iterations = max_iterations

    def select(self, node, c):
        """
        This function selects the node to expand
        :param node: a NodeMCTS object from which start the selection
        :param c: value indicating the exploration factor
        :return: a NodeMCTS object selected
        """
        # if the node is a leaf node, return the node
        if node.is_leaf():
            return node
        # otherwise, select the child with the highest UCB
        else:
            best = None
            best_ucb = -np.inf
            for child in node.children:
                if child.visits == 0:
                    ucb = np.inf
                else:
                    ucb = child.total_value / child.visits + c * np.sqrt(np.log(node.visits) / child.visits)
                if ucb > best_ucb:
                    best_ucb = ucb
                    best = child
            return self.select(best, c)

    def expand(self, node):
        """
        This function expands the node creating the children and returning a random child
        :param node: a NodeMCTS object to expand
        :return: NodeMCTS object corresponding to a random child of the father node
        """
        # create the children
        left_child = NodeMCTS(state=node.state.left_child, parent=node)
        right_child = NodeMCTS(state=node.state.right_child, parent=node)
        node.children.append(left_child)
        node.children.append(right_child)

        # select a random child
        return np.random.choice(node.children)

    def rollout(self, node):
        """
        This function simulates a random rollout from the node
        :param node: a NodeMCTS object from which start the rollout
        :return: the value of the terminal node
        """
        state = node.state
        while not state.is_terminal():
            # choose randomly a child
            state = np.random.choice([state.left_child, state.right_child])
        return state.value

    def backpropagate(self, node, value):
        """
        This function backpropagates the result of the game
        :param node: a NodeMCTS object
        :param value: value of the terminal node
        :return: None
        """
        while node is not None:
            node.visits += 1
            node.total_value += value
            node = node.parent

    def best_direction(self, node):
        """
        This function returns the best direction for the node and the values for each direction
        :param node: a NodeMCTS object
        :return: a pair where the first element is the best direction and the second element is the list of values for each direction
        """
        values = [child.get_avg_value() for child in node.children]
        i_best_value = np.argmax(values)
        best_direction = node.children[i_best_value].state.direction
        return best_direction, values

    def search(self, tree, dynamic_c = False, verbose=False):
        """
        This function implements the Monte Carlo Tree Search algorithm
        :param tree: tree instance of BinaryTree from which start the search
        :param dynamic_c: boolean indicating if the c parameter should be dynamically updated or fixed to 2
        :param verbose: boolean indicating if the search is verbose
        :return: the best direction to take from the root node
        """

        if verbose:
            print(f"🔍 MCTS execution from node {tree.root}")

        # initialize the root node
        root = NodeMCTS(state=tree.root)

        # run the iterations
        for i in range(self.max_iterations):
            # select the node to expand
            c = (2 + (1 - i / self.max_iterations) * 6) if dynamic_c else 2
            node = self.select(root, c)

            # expand only when if the node is the root or when it is a leaf node already visited
            if node == root or (node.is_leaf() and node.visits > 0 and not node.state.is_terminal()):
                node = self.expand(node)

            # perform a rollout
            value = self.rollout(node)

            # backpropagate the result
            self.backpropagate(node, value)

        # choose the best direction
        best_direction, values = self.best_direction(root)

        if verbose:
            direction_icon = "⏪" if best_direction == LEFT else "➡️"
            print("\tAverage values of the children:", [round(v,2) for v in values])
            print(f"\tBest direction: {best_direction} {direction_icon}")

        # return the best direction from the root node
        return best_direction


