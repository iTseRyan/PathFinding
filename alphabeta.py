import re


class Node(object):
    def __init__(self, Name):
        self.Name = Name
        self.parent = None
        self.children = []

    def add(self, child):
        self.children.append(child)
        child.parent = self


def read_file(file):
    with open(file, 'r') as f:
        for line in f:
            result = line[line.find(" "):]
            result = result.replace('{', '')
            result = result.replace('}', '')
            result = result.replace(' ', '')
            current_node = Node(result[1])
            for i in range(len(result)-1, 0, -6):
                print("1_node: "+str(result[i-3])+" 2_node: "+str(result[i-1]))
                # next_node = Node(result[i+3])
                # if result[i+1] == current_node.Name:
                #     current_node.add(next_node)
                # else:
                #     current_node = find_parent(next_node.Name, current_node)


# def find_node(name, node):
    # if node.Name == name:
    #     return node
    # else:
    #     if node.parent not None:
    #         return find_parent(name, node.parent)


read_file("./alphabeta.txt")


# class AlphaBeta:
#     # print utility value of root node (assuming it is max)
#     # print names of all nodes visited during search
#     def __init__(self, file):
#         with open(file, 'r') as f:
#             self.game_tree = [line.strip() for line in f]
#         self.game_tree = game_tree  # GameTree
#         self.root = game_tree.root  # GameNode
#         return

#     def alpha_beta_search(self, node):
#         infinity = float('inf')
#         best_val = -infinity
#         beta = infinity

#         successors = self.getSuccessors(node)
#         best_state = None
#         for state in successors:
#             value = self.min_value(state, best_val, beta)
#             if value > best_val:
#                 best_val = value
#                 best_state = state
#         print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
#         print "AlphaBeta:  Best State is: " + best_state.Name
#         return best_state

#     def max_value(self, node, alpha, beta):
#         print "AlphaBeta-->MAX: Visited Node :: " + node.Name
#         if self.isTerminal(node):
#             return self.getUtility(node)
#         infinity = float('inf')
#         value = -infinity

#         successors = self.getSuccessors(node)
#         for state in successors:
#             value = max(value, self.min_value(state, alpha, beta))
#             if value >= beta:
#                 return value
#             alpha = max(alpha, value)
#         return value

#     def min_value(self, node, alpha, beta):
#         print "AlphaBeta-->MIN: Visited Node :: " + node.Name
#         if self.isTerminal(node):
#             return self.getUtility(node)
#         infinity = float('inf')
#         value = infinity

#         successors = self.getSuccessors(node)
#         for state in successors:
#             value = min(value, self.max_value(state, alpha, beta))
#             if value <= alpha:
#                 return value
#             beta = min(beta, value)

#         return value

#     #                     #
#     #   UTILITY METHODS   #
#     #                     #

#     # successor states in a game tree are the child nodes...
#     def getSuccessors(self, node):
#         assert node is not None
#         return node.children

#     # return true if the node has NO children (successor states)
#     # return false if the node has children (successor states)
#     def isTerminal(self, node):
#         assert node is not None
#         return len(node.children) == 0

#     def getUtility(self, node):
#         assert node is not None
#         return node.value
