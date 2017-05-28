# Evolutionary Algorithm \- Genetic Programming

This project is a simple implementation of a genetic programming algorithm
using a tree representation for individuals. It is written in Python 3.5 and uses only the
standard library (no dependencies).

It can be used to solve linear and nonlinear regression problems and is
usable through a simple interface:
- A fit function that takes as inputs the training examples, target values and the number of iterations
- A predict function that takes as parameter an input for prediction

An example of usage can be found in the example.py script. This example requires to
have the libraries numpy and matplotlib installed.

### Usage

To use it, you need to give the algorithm:
- A fitness function that takes as parameters:
    - An instance of the class Tree
    - The training examples: array-like object of shape [n_samples, n_features]
    - The target values: array-like object of shape [n_samples]
- The function set that can be used in the tree
