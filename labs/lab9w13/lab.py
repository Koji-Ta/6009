import sys
import doctest
from http009 import http_response

sys.setrecursionlimit(10000)

# NO ADDITIONAL IMPORTS!

CHUNK_SIZE = 8192


def download_file(loc):
    """
    Yield the raw data from the given URL, in segments of CHUNK_SIZE bytes.

    If the request results in a redirect, yield bytes from the endpoint of the
    redirect.

    If the given URL represents a manifest, yield bytes from the parts
    represented therein, in the order they are specified.

    Raises a RuntimeError if the URL can't be reached, or in the case of a 500
    status code.  Raises a FileNotFoundError in the case of a 404 status code.
    """
    raise NotImplementedError


def files_from_sequence(stream):
    """
    Given a generator from download_file that represents a file sequence, yield
    the files from the sequence in the order they are specified.
    """
    raise NotImplementedError


if __name__ == '__main__':
    pass
