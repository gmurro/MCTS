# :deciduous_tree: Monte Carlo Tree Search (MCTS) :mag:

This repository contains a code realized as part of the Multi-Agent System final exam of the Master's degree in Artificial Intelligence, Vrije Universiteit Amsterdam.

It aims to construct a binary tree of depth d = 12 where each  node has a unique address *A* given by the branches traversed along the tree to reach that node (e.g. *A = LLRL*). The solution implemented will be discussed in two steps: first of all how the binary tree was built and then it is described the implementation of the *MCTS algorithm* applied to the binary tree.

## Binary tree representation

To implement a binary tree, the object-oriented paradigm has been used. The data structure consists of the following classes.

The `Node` class is the core part of a tree and it is structured as below:

-   *parent*: pointer to the parent node

-   *left\_child* and *right\_child*: pointers respectively to the left and the right node
    
-   *direction*: the direction that leads to the node (it can be \"L\" or \"R\")
    
-   *address*: the string representing the sequence of branches traversed along the tree to reach the node (\"0\" for the root node)
    
-   *value*: an integer representing the value of the leaf-nodes. It is assigned afterwards

A `Node` is considered \"leaf\" or \"terminal\" when it doesn't have left and right children.

The `BinaryTree` class represents the binary tree structure and the most important attributes are:

-   *depth*: the depth of the tree, initialized at 12

-   *root*: the pointer to the root `Node` from which each left and right child is expanded to build the tree recursively until reaching the depth of 12. Each level in the tree have exactly $2^{level}$ nodes, so the last level has $2^{12}$ leaves.
    
-   *target*: pick a random leaf-node as target node between the leaves of the tree built

As soon as in instance of BinaryTree is created, the value of each leaf-node is initialized according to the following formula dependent by the target node chosen: 
$$
value = Be^{\frac{-d_i}{\tau}}
$$
where $B=20$, $\tau=3$ and $d_i$ is edit-distance of the address of the node $i$ to the target and it is computed counting all the times that a character in the same position between the current address and the target address is different. Therefore the target node chosen will be the one with the highest value (20.0).

Using the method `update_root()`, the root of the BinaryTree is replaced by the child in the direction specified (left or right) and the depth of the tree is decreased by 1 unit. This method is very useful to apply the MCTS algorithm successively on the promising sub-trees.

An example of the representation of BinaryTree is showed in figure below. The numbers in the leave nodes are the correspondent values for that instance, choosing as target the leaf-node \"RLRLRLRLRRLL\".

![Represenation of BinaryTree where the target node is
\"RLRLRLRLRRLL\"](./assets/img/tree.png)



## MCTS implementation

As implementation choice the tree where the MCTS is performed is different from the BinaryTree built, due to the fact that MCTS expand progressively the \"snowcap\" and in the first stages it is not aware of the complete search space. The class `NodeMCTS` is the core part of a MCTS tree and it encapsulate the following class variables:

-   *state*: the correspondent Node instance from the BinaryTree

-   *parent*: pointer to the parent NodeMCTS

-   *children*: list of pointers to the left and the right NodeMCTS children
    
-   *total\_value*: variable that will contain the sum of the leaf-values reached from that node (initialized to 0)
    
-   *visits*: number of times that the node is visited (initialized to 0)

A `NodeMCTS` is condidered a \"leaf in the snowcap\" of the MCTS tree when it doesn't have children.

The real search is encoded in the class `MCTS`, that is instantiated specifying the *max\_iterations*, the maximum number of MCTS iterations (50 by default), and *c*, the value indicating the exploration factor. The essential methods of the algorithm are the ones described also in the Sutton & Barto book [[1]]([1]):

-   *selection*: selection of the child NodeMCTS with the maximal UCB values for the current node
    
-   *expand*: expands the NodeMCTS creating the children (known from the BinaryTree) and select randomly one of them
    
-   *rollout*: choose a random direction (\"L\" or \"R\") until a terminal node of the BinaryTree is reached. In this implementation
    the number of rollouts starting in a particular "snowcap" leaf node is assumed to be 1
    
-   *backpropagate*: updates all the nodes visited adding the value obtained in the terminal node to *total\_value* and increasing *visits* by one unit

A graphical overview of these steps is showed in figure below.

![Outline of a Monte Carlo Tree Search
[@Sutton1998]](./assets/img/mcts.png)

Between the different phases, selection is the most crucial. In fact, depending on how the child is chosen, not only the final average values could differ, but also the convergence time can change. Considering this, it is always chooses the child that maximizes the UCB formula. This is defined as:

$$
UCB(node) = \dfrac{total\_value}{visits} + c * \sqrt{\dfrac{\log N}{visits}}
$$
where $c$ is a constant that regularizes exploitation vs exploration,a nd $N$ is the number of the parent's visits. To find a good balance between exploration and exploitation, one should carefully choose the constant $c$, that in the implementation is equal to 2 as default.

Alternatively a dynamic version could be used, in order to makes the agent more explorative in the first iterations while more exploitative in the final ones. It is defined as:
$$
c_{dynamic} = 2 + (1 - \dfrac{i}{max\_iterations}) * 6
$$
where $i$ is the current iteration step.

The method of `MCTS` that actually starts the search algorithm is `search` that, given the tree instance of BinaryTree from which start the search, return the best direction to take from the root node. The following pseudocode explain how the previous mentioned methods are used in the search:

``` python
def search(tree, dynamic_c):
    root = NodeMCTS(state=tree.root)
    while max_iterations is not reached:
        current_node = root
        c = 2 or given by the dynamic formula according to dynamic_c parameter
        
        while current_node is not a snowcap leaf:
            selection(current_node, c)
        
        if (current_node has no visits and it is not terminal) or current_node is root:
            expand(current_node)
    
        value = rollout(current_node)
        backpropagate(current_node, value)
        
    return direction of the child that maximize total_value/visits
```

In order to find the optimal value of the leaves in the tree:

1.  apply the search from the root node until a computational budget of 50 iterations is reached
    
2.  choose the best child-node as new root (using the method `update_root`) and repeat 1
    
3.  the optimal path is obtained when the new root correspond to a terminal node

## Results

The outputs of the algorithm, applied to a binary three of depth 12 with max\_iterations=50 and both a static (c=8 and c=2) and dynamic exploration factor, are shown respectively in the figures below.
We can observe that in the first two the optimal path obtained from the search is different from the address of the chosen target leaf. Indeed an error in the decision occurred applying the MCTS at depth 7, and this could be caused by the fact that the number of iterations is too low and with a c=2 in the first stages the algorithm is not exploring enough and tend to focus on the most promising nodes found, instead with c=8 it is exploring too much.

However with a dynamic exploration factor, the results are clearly better and the MCTS works as expected. Indeed *c* value during the iterations of the algorithm starts from 8.0 and it is gradually decreasing. This helps to achieve a good exploration-exploitation trade-off.

![Output of the MCTS with max\_iterations=50 and
c=8](./assets/img/mcts_static_dynamic.png)

As further confirmation of what has been said so far, the figure below inspect the behavior of the MCTS increasing the number of max\_iterations. It is clearly observable that with a constant c the search reach the optimal path expected only with a number of iteration greater than 250. Instead using MCTS with dynamic c even with few iteration the algorithm is able to find the target.

![Compare the value of the optimal path found by MCTS with and without
dynamic c](./assets/img/plot_mcts.png)

## References
[1] Richard  S.  Sutton  and  Andrew  G.  Barto. ReinforcementLearning: An Introduction. Second. The MIT Press, 2018. URL: [http://incompleteideas.net/book/the-book-2nd.html](http://incompleteideas.net/book/the-book-2nd.html)
