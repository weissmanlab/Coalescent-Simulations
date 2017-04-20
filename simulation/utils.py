# -*- coding: utf-8 -*-

import numpy as np
from models import T

__author__ = 'Jayeol Chun'


def project_onto_plane(a, b):
    """
    finds the vector projection of points onto the hyperplane
    a : coefficients of the hyperplane
    b : original vector
    return  : new vector projected onto the hyperplane
    """
    dot = np.dot(a, b) / np.linalg.norm(a)
    p = dot * a / np.linalg.norm(a)
    return b - p


def display_params(args):
    """
    displays the simulation's parameber values
    """
    print("\n******* Current Simulation Params *******")
    print('\tSample Size: {}'.format(args[0]))
    print('\tMutation Rate: {:.3f}'.format(args[1]))


def display_stats(data):
    """
    displays the cumulative statistics of all trees observed for the models
    """
    k, b = data
    print("\n<< Kingman vs. Bolthausen-Sznitman Stats >>")
    print("\t{}:\t{:.2f} vs {:.2f}".format("AVG", np.mean(k), np.mean(b)))
    print("\t{}:\t{:.2f} vs {:.2f}".format("VAR", np.var(k), np.var(b)))


def display_tree(root: T, verbose=False):
    """
    displays the tree's Newick representation
    """
    from Bio import Phylo
    from io import StringIO
    newick = _traversal(root)
    tree = Phylo.read(StringIO(str(newick)), 'newick')
    Phylo.draw(tree)
    if verbose:
        print("\n*** Displaying Each Tree Results ***")
        print(newick)
        print(tree)


def _traversal(sample: T) -> str:
    """
    iterates through the tree rooted at the sample recursively in pre-order
    builds up a Newick representation
    """
    output = ''
    current = sample.right
    output = _recur_traversal((output + '('), current)
    while current.next != sample.left:
        current = current.next
        output = _recur_traversal(output + ', ', current)
    current = sample.left
    output = _recur_traversal(output + ', ', current) + ')' + str(sample.identity)
    return output


def _recur_traversal(output: str, sample: T) -> str:
    """
    appends the sample's information to the current Newick format
    recursively travels to the sample's (right) leaves
    """
    if sample.is_sample():
        # output = output + str(sample.identity) + ':' + str(sample.mutations)
        output = output + str(sample.identity) + ':' + str(sample.time)
        return output
    current = sample.right
    output = _recur_traversal((output + '('), current)
    while current.next != sample.left:
        current = current.next
        output = _recur_traversal(output + ', ', current)
    current = sample.left
    output = _recur_traversal((output + ', '), current)
    # output = output + ')' + str(sample.identity) + ':' + str(sample.mutations)
    output = output + ')' + str(sample.identity) + ':' + str(sample.time)
    return output
