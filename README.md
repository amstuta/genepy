# Evolutionary Algorithm \- Genetic Programming

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/amstuta/genetic.py/blob/master/LICENSE.md)

This package is a high-level library implementing a
genetic programming algorithm using a tree representation for individuals. It
is compatible with Python 2.7 and all the following versions and uses only the
standard library (no dependencies).

It can be used to solve linear and nonlinear regression problems and is
usable through a simple interface:
- A fit function that takes as inputs the training examples, target values and the number of iterations
- A predict function that takes as parameter an input for prediction

An example of usage can be found in the example.py script. This example requires to
have the libraries numpy and matplotlib installed.

### Installation

The package can be installed simply using Pypi:
```sh
pip install genetic
```

### Usage

To use it, you need to give the algorithm:
- A fitness function that takes as parameters:
    - An instance of the class Tree
    - The training examples: array-like object of shape [n_samples, n_features]
    - The target values: array-like object of shape [n_samples]
- The function set that can be used in the tree

Basic example:
```python
from operator import add, sub, mul
from genetic.core import EvolutionaryAlgorithm

# Load your dataset
train_features, train_targets = ...
test_features, test_targets   = ...

# Define a fitness function
def compute_fitness(tree, features, targets):
    ...
    return fitness

# Define the parameters of the algorithm
parameters = {
  'min_depth':        2,
  'max_depth':        5,
  'nb_trees':         50,
  'max_const':        100,
  'func_ratio':       0.5,
  'var_ratio':        0.5,
  'crossover_prob':   0.8,
  'mutation_prob':    0.2,
  'iterations':       80,
  'functions':        [add,sub,mul],
  'fitness_function': compute_fitness
}

# Create object and train algorithm
ea = EvolutionaryAlgorithm(**parameters)
ea.fit(train_features, train_targets)

# Make a prediction
predicted = ea.predict(test_features[0])
```
