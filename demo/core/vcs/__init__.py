"""Interfaces to version control systems."""

import os
import logging

from demo.common import DemoError

from demo.core.vcs import git
from demo.core.vcs import veracity
from demo.core.vcs import subversion
from demo.core.vcs import mockvcs

from demo.core.vcs.base import BaseWorkingCopy as _bwc
DIRECTORIES = {wc.DIRECTORY: wc for wc in _bwc.__subclasses__()}  # pylint: disable=E1101


def find_root(cwd):
    """Find the root of the working copy.

    @param cwd: current working directory

    @return: path to root of working copy

    @raise DemoError: if the root cannot be found

    """
    path = cwd

    logging.debug("looking for working copy from {}...".format(path))
    logging.debug("options: {}".format(', '.join([d for d in DIRECTORIES])))
    while not any(d in DIRECTORIES for d in os.listdir(path)):
        parent = os.path.dirname(path)
        if path == parent:
            msg = "no working copy found from: {}".format(cwd)
            raise DemoError(msg)
        else:
            path = parent

    logging.debug("found working copy: {}".format(path))
    return path


def load(path):
    """Return a working copy for the specified path."""
    for directory in os.listdir(path):
        if directory in DIRECTORIES:
            return DIRECTORIES[directory](path)
    logging.warning("no working copy found at: {}".format(path))
    return mockvcs.WorkingCopy(path)
