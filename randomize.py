#!/usr/bin/env python

"""Randomize the requirements."""

import os
import random
import logging

import doorstop

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
    for _ in range(SYS_COUNT):
        _generate_item(document)
    document = tree.new(HLR, 'HLR', parent='SYS')
    for _ in range(HLR_COUNT):
        _generate_item(document)
    document = tree.new(LLR, 'LLR', parent='HLR')
    for _ in range(LLR_COUNT):
        _generate_item(document)
    document = tree.new(HLT, 'HLT', parent='HLR')
    for _ in range(HLT_COUNT):
        _generate_item(document)
    document = tree.new(LLT, 'LLT', parent='LLR')
    for _ in range(LLT_COUNT):
        _generate_item(document)


def _generate_item(document):
    item = document.add()
    item.text = _get_random_text()
    logging.info("generated: {}".format(item))

# taken from http://pythonfiddle.com/random-sentence-generator/
s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]


def _get_random_text():
    return ' '.join((random.choice(s_nouns),
                     '**SHALL**',
                     random.choice(p_verbs),
                     random.choice(infinitives)))


if __name__ == '__main__':
    main()
