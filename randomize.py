#!/usr/bin/env python

"""Randomize the requirements."""

import os
import logging

import doorstop

SYS = os.path.join('reqs', 'sys')
HLR = os.path.join('reqs', 'hlr')
LLR = os.path.join('docs', 'llr')
HLT = os.path.join('demo', 'cli', 'test', 'docs')
LLT = os.path.join('demo', 'core', 'test', 'docs')


def main():
    """Delete and create new random requirements."""

    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Get current requirements
    logging.info("loading the current requirements...")
    tree = doorstop.build()

    # Delete all requirements
    logging.info("deleting the current requirements...")
    tree.delete()

    # Generate random requirements
    logging.info("generating random requirements...")
    document = tree.new(SYS, 'SYS')
    item = document.add()
    document = tree.new(HLR, 'HLR', parent='SYS')
    item = document.add()
    document = tree.new(LLR, 'LLR', parent='HLR')
    item = document.add()
    document = tree.new(HLT, 'HLT', parent='HLR')
    item = document.add()
    document = tree.new(LLT, 'LLT', parent='LLR')
    item = document.add()


if __name__ == '__main__':
    main()
