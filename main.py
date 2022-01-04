from BinaryTree import BinaryTree
from MCTS import MCTS


def main():
    # create the tree
    print("🌲 Building the tree...")
    tree = BinaryTree(depth=12, b=20, tau=3)
    best_leaf = max(tree.leaves)
    print(f"The address of the highest value leaf is {best_leaf.__repr__()}")

    # create the MCTS
    c = 2
    dynamic_c = True
    print(f"\nStarting the MCTS with dynamic c...") if dynamic_c else print(f"\nStarting the MCTS with c={c}...")
    mcts = MCTS(max_iterations=50, c=c)

    optimal_path = ""
    while not tree.root.is_terminal():
        # search the best direction
        direction = mcts.search(tree, dynamic_c=dynamic_c, verbose=True)
        optimal_path += direction

        # update the tree
        tree.update_root(direction)

    print(f"Optimal path obtained from the search: {optimal_path}")
    if optimal_path == best_leaf.address:
        print(f"✅ It is the address expected!")
    else:
        print(f"❌ It is NOT the address expected!")


if __name__ == "__main__":
    main()