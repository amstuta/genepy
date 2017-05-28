import random
from .node import Node


class Tree:
    """
    Represent a regression tree.
    :param max_depth:           Maximum depth of the tree
    :param max_const:           Maximum value of the constants in the tree
    :param function_ratio:      Ratio of functions over (variables + constants)
    :param variable_ratio:      Ratio of variables over constants
    :param functions:           The different functions available
    :param variables:           The available variables to use in the tree
    :param construction_method: Method used to construct the tree. If set to
                                'full', the tree will be expanded until max_depth
                                is reached. If set to 'grow', a random decision
                                will be made at each split to create nodes or
                                leaves (with depth <= max_depth).
    """

    def __init__(self, max_depth, max_const, function_ratio, variable_ratio,
                functions, variables, construction_method='grow'):
        if not construction_method in ['grow','full']:
            raise AttributeError('Construction method must be either grow or full')
        self.nodes = []
        self.max_depth = max_depth
        self.construction_method = construction_method
        self.root_node = self.construct_tree(max_depth, max_const,
                                            function_ratio, variable_ratio,
                                            functions, variables)


    def predict(self, variables):
        """
        Predicts an output for the given inputs.
        """
        return self.root_node.calc(variables)


    def construct_tree(self, depth, max_const, function_ratio,
                        variable_ratio, functions, variables, prev_node=None):
        """
        Recursively builds the tree.
        """
        if depth == 1:
            val = self.choose_node_values_only(variable_ratio, max_const,
                                                variables)
            node = Node(val, prev_node)
            self.nodes.append(node)
            return node

        if self.construction_method == 'grow':
            val = self.choose_node_content(depth, function_ratio, variable_ratio,
                                            max_const, functions, variables)
        else:
            val = self.choose_node_functions_only(functions)
        current_node = Node(val, prev_node)
        self.nodes.append(current_node)

        if isinstance(val, int) or isinstance(val, str):
            return current_node

        next_left = self.construct_tree(depth - 1, max_const, function_ratio,
                                        variable_ratio, functions, variables,
                                        current_node)
        next_right = self.construct_tree(depth - 1, max_const, function_ratio,
                                        variable_ratio, functions, variables,
                                        current_node)
        current_node.set_children(next_left, next_right)
        return current_node


    def choose_node_content(self, depth, function_ratio, variable_ratio,
                        max_const, functions, variables):
        """
        Chooses a random value for the current node. If the current node is the
        root node, the function will return a randomly chosen function.
        """
        if depth == self.max_depth:
            return random.choice(functions)
        else:
            rand = random.random()
            if rand <= function_ratio:
                return random.choice(functions)
            else:
                return self.choose_node_values_only(variable_ratio, max_const,
                                                    variables)


    def choose_node_values_only(self, variable_ratio, max_const, variables):
        """
        Chooses a random value for the current node between the variables and the
        constants.
        """
        rand = random.random()
        if rand <= variable_ratio:
            return random.choice(variables)
        else:
            return random.choice(range(max_const))


    def choose_node_functions_only(self, functions):
        """
        Returns a randomly chosen function.
        """
        return random.choice(functions)


    def pick_random_node(self, content=None):
        """
        Returns a node randomly chosen from the nodes list.
        :param content: The type of content held in the node. Can be set to
                        None if any node can be chosen, 'function' is the
                        node must contain a function and 'value' for a const
                        or a variable
        """
        node = random.choice(self.nodes)
        if node == self.root_node:
            return self.pick_random_node(content)
        if content is None or \
        (content == 'function' and hasattr(node.value, '__call__')) or \
        (content == 'value' and
            (isinstance(node.value, str) or isinstance(node.value, int))):
            return node
        return self.pick_random_node(content)


    def has_function_node(self):
        """
        Returns True if the tree contains at least one node with a function
        and this node is not the root node.
        """
        for node in self.nodes:
            if node != self.root_node and hasattr(node.value, '__call__'):
                return True
        return False


    def remove_random_node(self):
        """
        Extract a subpart of the tree and returns it.
        """
        random_node = self.pick_random_node()
        self.remove_children_nodes(random_node)
        return random_node


    def remove_children_nodes(self, node):
        """
        Removes all the subnodes of a certain node from the tree.
        """
        if node is None: return
        self.nodes.remove(node)
        self.remove_children_nodes(node.next_left)
        self.remove_children_nodes(node.next_right)


    def add_node(self, node):
        """
        Adds a node and all it's children in the tree.
        """
        if node is None: return
        self.nodes.append(node)
        self.add_node(node.next_left)
        self.add_node(node.next_right)


    def __repr__(self):
        return self.print_tree(self.root_node)


    def print_tree(self, node, ident=''):
        if node is None:
            return ''
        if isinstance(node.value, str):
            return 'f[{}]\n'.format(node.value)
        elif isinstance(node.value, int):
            return '{}\n'.format(node.value)
        else:
            repr = '{}\n'.format(node.value)
            repr += '{} L -> {}'.format(ident, self.print_tree(node.next_left, ident + ' '))
            repr += '{} R -> {}'.format(ident, self.print_tree(node.next_right, ident + ' '))
            return repr
