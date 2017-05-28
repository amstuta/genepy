import random
from copy import deepcopy
from .tree import Tree
from .node import Node


class EvolutionaryAlgorithm:
    """
    Evolutionary algorithm using the concepts of genetic programming.

    :param min_depth:           Minimum depth of a tree
    :param max_depth:           Maximum depth of a tree
    :param nb_trees:            Number of trees to use during training
    :param max_const:           The maximum value of consts used in the trees
    :param func_ratio:          Ratio function / values used to build the trees
    :param var_ratio:           Ratio variables / constants used to build the trees
    :param crossover_prob:      Crossover probability when evolving the population
    :param mutation_prob:       Mutation probability when evolving the population
    :param functions:           The functions that can be used in the trees
    :param fitness_function:    The fitness function used to evaluate the population
    """

    def __init__(self, functions, fitness_function, min_depth=2, max_depth=5,
                nb_trees=100, max_const=20, func_ratio=0.7, var_ratio=0.6,
                crossover_prob=0.6, mutation_prob=0.3, **args):
        self.min_depth  = min_depth
        self.max_depth  = max_depth
        self.nb_trees   = nb_trees
        self.max_const  = max_const
        self.func_ratio = func_ratio
        self.var_ratio  = var_ratio
        self.cross_prob = crossover_prob
        self.mutat_prob = mutation_prob
        self.functions  = functions
        self.fitness    = fitness_function
        self.tree       = None


    def fit(self, features, targets, iterations=100):
        """
        Genetic Programming algorithm.
        :param features:    Training examples (array-like / matrix object of
                            shape [n_samples, n_features])
        :param targets:     Target values (array-like object of shape [n_samples])
        :param iterations:  Maximum number of iterations
        """
        if len(features) == 0 or len(features) != len(targets):
            raise AttributeError('Invalid features or targets: %s' % key)

        variables = [str(i) for i in range(len(features[0]))]
        trees = self.create_trees(variables)
        for i in range(iterations):
            fitness = [self.fitness(tree, features, targets) for tree in trees]
            trees = self.selection(trees, fitness)
            trees = self.generate_next_population(trees, variables)
        self.tree = trees[fitness.index(max(fitness))]


    def predict(self, feature):
        """
        Predicts a value for a given input.
        :param feature: Input for prediction (array-like object of shape [n_features])
        """
        if self.tree is None:
            raise ValueError('Algorithm not trained')
        return self.tree.predict(feature)


    def create_trees(self, variables):
        """
        Generates the random population used during the training.
        :param variables:   The availabe variables
        """
        trees = []
        depths = range(self.min_depth, self.max_depth + 1)
        for i in range(self.nb_trees):
            depth = random.choice(depths)
            tree = Tree(depth, self.max_const, self.func_ratio, self.var_ratio,
                        self.functions, variables,
                        'grow' if i % 2 == 0 else 'full')
            trees.append(tree)
        return trees


    def selection(self, trees, fitness):
        """
        Emulates a selection process. Select individuals with probability
        proportional to their fitness value.
        :param trees:   The current population
        :param fitness: The fitness of the current population
        """
        fitness = [fit / sum(fitness) for fit in fitness]
        fitness = [sum(fitness[:i+1]) for i in range(len(fitness))]
        new_trees = []
        for i in range(len(trees)):
            if i % 2 == 0:
                new_trees.append(deepcopy(random.choice(trees)))
            else:
                rand = random.random()
                selected = 0
                for idx, fit in enumerate(fitness):
                    if rand <= fit:
                        selected = idx
                        break
                new_trees.append(deepcopy(trees[selected]))
        return new_trees


    def generate_next_population(self, trees, variables):
        """
        Generate next population by applying variation operators to individuals.
        :param trees:       The current population
        :param variables:   The available variables
        """
        new_generation = []
        it = iter(trees)
        for tree in it:
            try: next_tree = next(it)
            except:
                new_generation.append(tree)
                continue
            rand = random.random()
            probabilities = [self.cross_prob, self.cross_prob + self.mutat_prob]
            if rand <= probabilities[0]:
                self.crossover(tree, next_tree)
            elif rand <= probabilities[1]:
                mutation_funcs = [self.single_point_mutation,
                                self.expansion_mutation, self.collapse_mutation]
                random.choice(mutation_funcs)(tree, variables)
                random.choice(mutation_funcs)(next_tree, variables)
            new_generation.append(tree)
            new_generation.append(next_tree)
        return new_generation


    def crossover(self, left_tree, right_tree):
        """
        Performs a cross-over between two trees. Randomly selects a node in each
        tree and exchanges them.
        :param left_tree:   The left tree used to perform crossover
        :param right_tree:  The right tree used to perform crossover
        """
        left_node = left_tree.remove_random_node()
        right_node = right_tree.remove_random_node()
        left_prev = left_node.prev
        right_prev = right_node.prev
        if left_node == left_prev.next_left:
            left_prev.next_left = right_node
        else:
            left_prev.next_right = right_node
        if right_node == right_prev.next_left:
            right_prev.next_left = left_node
        else:
            right_prev.next_right = left_node
        left_node.prev = right_prev
        right_node.prev = left_prev
        left_tree.add_node(right_node)
        right_tree.add_node(left_node)


    def single_point_mutation(self, tree, variables):
        """
        Performs a random mutation on a randomly chosen node of the tree.
        :param tree:        The tree to apply mutation on
        :param variables:   The different available variables
        """
        random_node = tree.pick_random_node()
        if isinstance(random_node.value, int) or isinstance(random_node.value, str):
            rand = random.random()
            if rand <= self.var_ratio:
                random_node.value = random.choice(variables)
            else:
                random_node.value = random.choice(range(self.max_const))
        else:
            random_node.value = random.choice(self.functions)


    def expansion_mutation(self, tree, variables):
        """
        Randomly chooses a node that contains a value (constant or variable) and
        replace it by a subtree containing at least three nodes and with a
        maximum depth of self.min_depth.
        :param tree:        The tree to apply mutation on
        :param variables:   The different variables available
        """
        rand_node = tree.pick_random_node(content='value')
        rand_prev = rand_node.prev
        subtree = Tree(self.min_depth, self.max_const, self.func_ratio,
                        self.var_ratio, self.functions, variables, 'grow')
        subtree.root_node.prev = rand_prev
        if rand_node == rand_prev.next_left:
            rand_prev.next_left = subtree.root_node
        else:
            rand_prev.next_right = subtree.root_node
        tree.remove_children_nodes(rand_node)
        tree.add_node(subtree.root_node)


    def collapse_mutation(self, tree, variables):
        """
        Randomly chooses a node in the tree that contains a function and replace it
        with a node containing a value or a variable.
        :param tree:        The tree to apply mutation on
        :param variables:   The different variables available
        """
        if not tree.has_function_node(): return
        rand_node = tree.pick_random_node(content='function')
        rand = random.random()
        if rand <= self.var_ratio:
            new_node = Node(random.choice(variables), rand_node.prev)
        else:
            new_node = Node(random.choice(range(self.max_const)), rand_node.prev)
        if rand_node == rand_node.prev.next_left:
            rand_node.prev.next_left = new_node
        else:
            rand_node.prev.next_right = new_node
        tree.remove_children_nodes(rand_node)
        tree.add_node(new_node)
