#!/usr/bin/env python

"""Randomize the requirements."""

import os
import logging

import doorstop

REQ = os.path.join('docs', 'reqs')
TUT = os.path.join('docs', 'reqs', 'tutorial')
HLR = os.path.join('demo', 'cli', 'test', 'docs')
LLR = os.path.join('demo', 'core', 'test', 'docs')


def main():
    """Delete and create new random requirements."""

    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Get current requirements
    tree = doorstop.build()

    # Delete all requirements
    logging.info("deleting all requirements...")
    for document in tree:
        for item in document:
            item.delete()

    # Generate random requirements
    logging.info("generating random requirements...")
    for document in tree:
        item = document.add()

if __name__ == '__main__':
    main()
