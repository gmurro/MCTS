from tqdm import tqdm

from MCTS import MCTS
from BinaryTree import BinaryTree
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(15)


def run_experiment(max_iterations, dynamic_c=False):
    """
    Run a single experiment of a sequence of MCTS searches to find the optimal path.
    :param max_iterations: Number of iterations to run the MCTS.
    :param dynamic_c: Boolean indicating whether to use a dynamic c or not.
    :return: value of the optimal path found from the search
    """
    tree = BinaryTree(depth=12, b=20, tau=3)
    best_leaf = max(tree.leaves)
    mcts = MCTS(max_iterations=max_iterations, c=2)

    optimal_path = ""
    while tree.depth > 0:
        # search the best direction
        direction = mcts.search(tree, dynamic_c=dynamic_c, verbose=False)
        optimal_path += direction

        # update the tree
        tree.update_root(direction)

    # return the distance of the optimal path found from the search wrt the best leaf
    return sum(1 for a, b in zip(optimal_path, best_leaf.address) if a != b)


def main():
    # compute statistics for static c and dynamic c
    n_iterations = np.logspace(0.7, 3, num=18, base=10, dtype=int)
    values_static_c = [run_experiment(max_iterations=n, dynamic_c=False) for n in tqdm(n_iterations, desc='Execute MCTS with c=2', unit=' experiment')]
    values_dynamic_c = [run_experiment(max_iterations=n, dynamic_c=True) for n in tqdm(n_iterations, desc='Execute MCTS with dynamic c', unit=' experiment')]

    # plot the results
    plt.figure(figsize=(8, 4))
    plt.plot(n_iterations, values_dynamic_c, '-o', label="MCTS with dynamic c")
    plt.plot(n_iterations, values_static_c, '-o', label="MCTS with c=2")
    plt.xlabel("Number of iterations")
    plt.ylabel("Distance of the optimal path from the best leaf")
    plt.title("Compare the value of the optimal path found by MCTS with and without dynamic c")
    plt.grid(linestyle='--', linewidth=1)
    plt.xscale("log")
    plt.xticks(n_iterations, n_iterations)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()