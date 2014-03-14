#!/usr/bin/env python

"""Randomize the requirements."""

import os
import sys
import random
import logging

import doorstop
import requests

SYS = os.path.join('reqs', 'sys')
HLR = os.path.join('reqs', 'hlr')
LLR = os.path.join('docs', 'llr')
HLT = os.path.join('demo', 'cli', 'test', 'docs')
LLT = os.path.join('demo', 'core', 'test', 'docs')

SYS_COUNT = 50
HLR_COUNT = SYS_COUNT * 2
LLR_COUNT = HLR_COUNT * 2
HLT_COUNT = HLR_COUNT * 2
LLT_COUNT = LLR_COUNT * 2


def main():
    """Delete and create new random requirements."""

    # Parse arguments
    delete = '--delete' in sys.argv

    # Configure logging

    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Get current requirements
    logging.info("loading the current requirements...")
    tree = doorstop.build()

    # Delete the old requirements
    if delete:
        logging.info("deleting the current requirements...")
        tree.delete()

    # Generate new random requirements
    if not len((item for item in (document for document in tree))):

        logging.info("generating random requirements...")
        document = tree.new(SYS, 'SYS')
        for _ in range(SYS_COUNT):
            _generate_item(document, shall=True)
        document = tree.new(HLR, 'HLR', parent='SYS')
        for _ in range(HLR_COUNT):
            _generate_item(document, shall=True)
        document = tree.new(LLR, 'LLR', parent='HLR')
        for _ in range(LLR_COUNT):
            _generate_item(document, shall=True)
        document = tree.new(HLT, 'HLT', parent='HLR')
        for _ in range(HLT_COUNT):
            _generate_item(document, verify=True)
        document = tree.new(LLT, 'LLT', parent='LLR')
        for _ in range(LLT_COUNT):
            _generate_item(document, verify=True)


_LM = "Lorem markdownum"
_LM_URL = ("http://jaspervdj.be/lorem-markdownum/markdown.txt"
           "?"
           "no-headers=on"
           "&"
           "no-quotes=on"
           "&"
           "reference-links=off")


def _generate_item(document, shall=False, verify=False):
    """Generate a new requirement or test case."""
    item = document.add()
    text = _get_random_text()
    if shall:
        assert verify == False
        text = text.replace(_LM, _LM + " **SHALL**", 1)
    if verify:
        assert shall == False
        text = text.replace(_LM, "Verify l" + _LM[1:], 1)
    item.text = text
    logging.info("generated: {}".format(item))


def _get_random_text():
    """Get random text using lorem-markdownum."""
    response = requests.get(_LM_URL)
    assert response.status_code == 200
    return response.text


if __name__ == '__main__':
    main()
