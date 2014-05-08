#!/usr/bin/env python

"""Randomize the requirements."""

import os
import re
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
HLR_COUNT = SYS_COUNT * 2  # 100
LLR_COUNT = HLR_COUNT * 2  # 200
HLT_COUNT = HLR_COUNT * 2  # 200
LLT_COUNT = LLR_COUNT * 2  # 400
assert 950 == (SYS_COUNT + LLR_COUNT + LLR_COUNT + HLT_COUNT + LLT_COUNT)

MAX_LINKS = 5


def main():
    """Create new random requirements if none exist."""

    # Parse arguments
    delete_items = '--items' in sys.argv
    delete_links = '--links' in sys.argv

    # Configure logging
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Get current requirements
    logging.info("loading the current requirements...")
    tree = doorstop.build()
    tree.load()

    # Delete old requirements
    if delete_items:
        logging.info("deleting the current requirements...")
        tree.delete()

    # Delete old links
    if delete_links and not delete_items:
        logging.info("deleting the current links...")
        for document in tree:
            for item in document:
                item.links = []

    # Generate random requirements if needed
    _randomize_items(tree)
    _randomize_links(tree)

    # Fix levels
    for document in tree:
        items = document.items
        for index in range(1, len(items)):
            level = list(items[index].level)
            level_prev = list(items[index - 1].level)
            logging.info("checking {} level {}...".format(document.prefix, level))
            while level <= level_prev:
                logging.info("fixing {} level {}...".format(items[index], level))
                level[-1] += 1
            items[index].level = level


def _randomize_items(tree):
    """Create random item text if no items exist."""

    # Generate new random requirements
    items = []
    for document in tree:
        for item in document:
            logging.debug("item: {}".format(item))
            items.append(item)
    if not any(items):

        logging.info("generating random requirements...")

        document_sys = tree.new(SYS, 'SYS')
        for _ in range(SYS_COUNT):
            _generate_item(document_sys, shall=True)

        document_hlr = tree.new(HLR, 'HLR', parent=document_sys.prefix)
        for _ in range(HLR_COUNT):
            _generate_item(document_hlr, shall=True)

        document_llr = tree.new(LLR, 'LLR', parent=document_hlr.prefix)
        for _ in range(LLR_COUNT):
            _generate_item(document_llr, shall=True)

        document_hlt = tree.new(HLT, 'HLT', parent=document_hlr.prefix)
        for _ in range(HLT_COUNT):
            _generate_item(document_hlt, verify=True)

        document_llt = tree.new(LLT, 'LLT', parent=document_llr.prefix)
        for _ in range(LLT_COUNT):
            _generate_item(document_llt, verify=True)


def _randomize_links(tree):
    """Create random item links if none exist."""

    # Get documents
    document_sys = tree.find_document('SYS')
    document_hlr = tree.find_document('HLR')
    document_llr = tree.find_document('LLR')
    document_hlt = tree.find_document('HLT')
    document_llt = tree.find_document('LLT')

    # Generate random levels
    links = []
    for document in tree:
        for item in document:
            for identifier in item.links:
                link = "{} -> {}".format(item, identifier)
                logging.debug("link: {}".format(link))
                links.append(link)
    if not links:

        logging.info("generating random links...")

        for parent, child in ((document_sys, document_hlr),
                              (document_hlr, document_llr),
                              (document_hlr, document_hlt),
                              (document_llr, document_llt)):
            for item in child:
                _randomize_links_item(item, parent)


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

    if item.level == (1, 0) or (item.level[-1] > 2 and random.random() > 0.75):
        text = re.sub("[^a-zA-Z0-9_ ]", '', text)  # remove special characters
        words = text.split(' ', 10)[2:random.randint(3, 10)]
        text = ' '.join(words)
        if item.level != (1, 0):
            item.level = [item.level[0] + 1]
        item.heading = True

    elif shall:
        assert verify == False
        text = text.replace(_LM, _LM + " **SHALL**", 1)
    elif verify:
        assert shall == False
        text = text.replace(_LM, "Verify l" + _LM[1:], 1)
    item.text = text

    logging.info("generated: {}".format(item))


def _get_random_text():
    """Get random text using lorem-markdownum."""
    response = requests.get(_LM_URL)
    assert response.status_code == 200
    paragraphs = response.text.split('\n\n')
    count = random.randint(1, min(3, len(paragraphs)))
    text = '\n\n'.join(paragraphs[:count])
    return text


def _randomize_links_item(item, document):
    """Randomize an item's links."""
    logging.info("randomly linking {}...".format(item))
    item.links = []
    if not item.normative:
        return
    items = [item for item in document.items if item.normative]
    for _ in range(random.randint(1, MAX_LINKS)):
        item.add_link(random.choice(items).id)


if __name__ == '__main__':
    main()
