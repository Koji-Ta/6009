with open('words2.txt') as f:
    allwords = set(f.read().splitlines())


def subwords_helper(x):
    """
    Helper function, returns all possible permutations of subsequences of x
    regardless of whether they are real words or not
    """
    raise NotImplementedError


def subwords_helper_iter(x):
    """
    Helper function, returns all possible permutations of subsequences of x
    regardless of whether they are real words or not
    """
    raise NotImplementedError


def subwords(word):
    """
    Return all valid words that can be made from a subset of the letters in
    the given original word.
    """
    raise NotImplementedError
