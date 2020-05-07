#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementations of algorithms related to association rules.
"""

import typing
import numbers
import itertools

class Rule(object):
    """
    A class for a rule.
    """

    # Number of decimals used for printing
    _decimals = 3

    def __init__(
        self,
        lhs: tuple,
        rhs: tuple,
        count_full: int = 0,
        count_lhs: int = 0,
        count_rhs: int = 0,
        num_transactions: int = 0,
    ):
        """
        Initialize a new rule. This call is a thin wrapper around some data.

        Parameters
        ----------
        lhs : tuple
            The left hand side (antecedent) of the rule. Each item in the tuple
            must be hashable, e.g. a string or an integer.
        rhs : tuple
            The right hand side (consequent) of the rule.
        count_full : int
            The count of the union of the lhs and rhs in the dataset.
        count_lhs : int
            The count of the lhs in the dataset.
        count_rhs : int
            The count of the rhs in the dataset.
        num_transactions : int
            The number of transactions in the dataset.

        Examples
        --------
        >>> r = Rule(('a', 'b'), ('c',), 50, 100, 150, 200)
        >>> r.confidence  # Probability of 'c', given 'a' and 'b'
        0.5
        >>> r.support  # Probability of ('a', 'b', 'c') in the data
        0.25
        >>> # Ratio of observed over expected support if lhs, rhs = independent
        >>> r.lift == 2 / 3
        True
        >>> print(r)
        {a, b} -> {c} (conf: 0.500, supp: 0.250, lift: 0.667, conv: 0.500)
        >>> r
        {a, b} -> {c}
        """
        self.lhs = lhs  # antecedent
        self.rhs = rhs  # consequent
        self.count_full = count_full
        self.count_lhs = count_lhs
        self.count_rhs = count_rhs
        self.num_transactions = num_transactions

    @property
    def confidence(self):
        """
        The confidence of a rule is the probability of the rhs given the lhs.
        If X -> Y, then the confidence is P(Y|X).
        """
        try:
            return self.count_full / self.count_lhs
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def support(self):
        """
        The support of a rule is the frequency of which the lhs and rhs appear
        together in the dataset. If X -> Y, then the support is P(Y and X).
        """
        try:
            return self.count_full / self.num_transactions
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def lift(self):
        """
        The lift of a rule is the ratio of the observed support to the expected
        support if the lhs and rhs were independent.If X -> Y, then the lift is
        given by the fraction P(X and Y) / (P(X) * P(Y)).
        """
        try:
            observed_support = self.count_full / self.num_transactions
            prod_counts = self.count_lhs * self.count_rhs
            expected_support = prod_counts / self.num_transactions ** 2
            return observed_support / expected_support
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def conviction(self):
        """
        The conviction of a rule X -> Y is the ratio P(not Y) / P(not Y | X).
        It's the proportion of how often Y does not appear in the data to how
        often Y does not appear in the data, given X. If the ratio is large,
        then the confidence is large and Y appears often.
        """
        try:
            eps = 10e-10  # Avoid zero division
            prob_not_rhs = 1 - self.count_rhs / self.num_transactions
            prob_not_rhs_given_lhs = 1 - self.confidence
            return prob_not_rhs / (prob_not_rhs_given_lhs + eps)
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @property
    def rpf(self):
        """
        The RPF (Rule Power Factor) is the confidence times the support.
        """
        try:
            return self.confidence * self.support
        except ZeroDivisionError:
            return None
        except AttributeError:
            return None

    @staticmethod
    def _pf(s):
        """
        Pretty formatting of an iterable.
        """
        return "{" + ", ".join(str(k) for k in s) + "}"

    def __repr__(self):
        """
        Representation of a rule.
        """
        return "{} -> {}".format(self._pf(self.lhs), self._pf(self.rhs))

    def __str__(self):
        """
        Printing of a rule.
        """
        conf = "conf: {0:.3f}".format(self.confidence)
        supp = "supp: {0:.3f}".format(self.support)
        lift = "lift: {0:.3f}".format(self.lift)
        conv = "conv: {0:.3f}".format(self.conviction)

        return "{} -> {} ({}, {}, {}, {})".format(
            self._pf(self.lhs), self._pf(self.rhs), conf, supp, lift, conv
        )

    def __eq__(self, other):
        """
        Equality of two rules.
        """
        return (set(self.lhs) == set(other.lhs)) and (
            set(self.rhs) == set(other.rhs)
        )

    def __hash__(self):
        """
        Hashing a rule for efficient set and dict representation.
        """
        return hash(frozenset(self.lhs + self.rhs))

    def __len__(self):
        """
        The length of a rule, defined as the number of items in the rule.
        """
        return len(self.lhs + self.rhs)
    

def generate_rule_from_rule(rule_object):
    '''
        Allows me to copy rule objects from compatible libraries to the PyARMViz version
        in order to take advantage of its additional functionality if needed
    '''
    return Rule(rule_object.lhs, rule_object.rhs, rule_object.count_full, rule_object.count_lhs, rule_object.count_rhs, 
                rule_object.num_transactions)

def generate_rule_from_dict(rule_dict):
    '''
        Allows me to copy rule objects from compatible libraries to the PyARMViz version
        in order to take advantage of its additional functionality if needed
    '''
    return Rule(rule_dict['lhs'], rule_dict['rhs'], rule_dict['count_full'], 
                rule_dict['count_lhs'], rule_dict['count_rhs'], rule_dict['num_transactions'])