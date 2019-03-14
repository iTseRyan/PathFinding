import math

"""
As long as the input file is named properly inside the
read_files function the program will work.
"""


class Node(object):
    """
    Class object for nodes in the tree
    """

    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, child):
        self.children.append(child)


leaf_nodes = 0


def minimax(node, isMaximizingPlayer, alpha, beta):
    """
    minimax is a recursive function that uses the current node
    to search children nodes until a leaf is found. The function
    keeps track of the alpha and beta variables as it traverses 
    through the tree. When a leaf node is found the leaf_nodes
    variable is updated to keep track of the number of leafs
    examined.
    """
    if node.name.isdigit():  # leaf nodes contain numbers not letters
        global leaf_nodes
        leaf_nodes += 1
        return int(node.name)

    if isMaximizingPlayer:  # max node
        bestVal = -math.inf
        for child in node.children:
            value = minimax(child, False, alpha, beta)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:  # min node
        bestVal = math.inf
        for child in node.children:
            value = minimax(child, True, alpha, beta)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal


def add_node(parent_name, child_name, node):
    """
    This helper function searches the children of the current node
    until a matching parent node is found and the  new child node
    can be created and added to the parent. The tree is returned.
    """
    if node.name == parent_name:
        return node.add(Node(child_name))
    else:
        for child in node.children:
            add_node(parent_name, child_name, child)


def read_file(file):
    results = []
    with open(file, 'r') as f:
        graph = 1
        for line in f:
            global leaf_nodes
            leaf_nodes = 0
            """
            First we start by evaluating if the root node will be maximizing
            or minimizing. If the string is equal to MAX then the variable
            maximize is set to 0. Otherwise it's set to 1.
            """
            starter = line[:line.find(" ")]
            starter = starter.replace('{', '')
            stater = starter.replace('}', '')
            starter = starter.replace(' ', '')
            starter = str(starter[3]+starter[4]+starter[5])
            maximize = -1
            if starter == "MAX":
                maximize = True
            else:
                maximize = False
            """
            Then the edges are retrieved and looped through the pairs.
            """
            edges = line[line.find(" "):]
            edges = edges.replace('{', '')
            edges = edges.replace('}', '')
            edges = edges.replace(' ', '')
            # the root node is set as the first letter in the edges
            tree = Node(edges[1])
            # looping through the edges
            for i in range(0, len(edges), 6):
                add_node(edges[i+1], edges[i+3], tree)  # user helper function

            # calling the minimax function. Returns the optimal value and the number of leafs
            # examined.
            score = minimax(tree, maximize, -math.inf, math.inf)
            leafs = leaf_nodes
            results.append({'graph': str(graph), 'score': str(
                score), 'leafs_examined': str(leafs)})

            graph += 1
    write_file(results)


def write_file(results):
    with open("alphabeta_out.txt", 'w') as f:
        for line in results:
            f.write("Graph: " + line['graph'] + " Score: " + line['score'] +
                    " Leaf Nodes Examined: " + line['leafs_examined'] + "\n")


read_file("./alphabeta.txt")
