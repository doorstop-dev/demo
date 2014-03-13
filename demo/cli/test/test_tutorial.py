#!/usr/bin/env python

"""Integration tests for the documentation tutorials."""

import unittest

import os
import shutil
import tempfile
import subprocess
import logging

from demo.cli.test import ENV, REASON, ROOT

if os.name == 'nt':
    PATH = os.path.join(ROOT, 'env', 'Scripts', 'doorstop-demo.exe')
    DEMO = os.path.normpath(PATH)
else:
    PATH = os.path.join(ROOT, 'env', 'bin', 'doorstop-demo')
    DEMO = os.path.normpath(PATH)


if __name__ == '__main__':
    os.environ[ENV] = '1'  # run the integration tests when called directly


@unittest.skipUnless(os.getenv(ENV), REASON)  # pylint: disable=R0904
class TestBase(unittest.TestCase):  # pylint: disable=R0904

    """Base class for tutorial tests."""

    def setUp(self):
        self.cwd = os.getcwd()
        self.temp = tempfile.mkdtemp()
        print("$ cd {}".format(self.temp))
        os.chdir(self.temp)
        os.mkdir('.mockvcs')  # simulate a working copy
        os.environ['EDITOR'] = 'cat'

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.temp)

    @staticmethod
    def demo(args=""):
        """Call 'doorstop-demo' with a string of arguments."""
        print("$ doorstop-demo {}".format(args))
        cmd = "{} {} -v".format(DEMO, args)
        if subprocess.call(cmd, shell=True, stderr=subprocess.PIPE) != 0:
            raise AssertionError("command failed: doorstop-demo {}".format(args))


@unittest.skipUnless(os.getenv(ENV), REASON)  # pylint: disable=R0904
class TestSection1(TestBase):  # pylint: disable=R0904

    """Integration tests for section 1.0 of the tutorial."""

    def test_tutorial_section_1(self):
        """Verify tutorial section 1.0 is working."""

        # 1.1

        self.demo("new REQ ./reqs")

        self.demo("add REQ")
        self.demo("add REQ")
        self.demo("add REQ")

        self.demo("edit REQ1 --tool cat")
        self.demo("edit REQ2 --tool cat")

        # 1.2

        self.demo("new TST ./reqs/tests --parent REQ")

        self.demo("add TST")
        self.demo("add TST")

        self.demo("edit TST1 --tool cat")
        self.demo("edit TST2 --tool cat")

        self.demo("link TST1 REQ1")
        self.demo("link TST1 REQ3")
        self.demo("link TST2 REQ1")
        self.demo("link TST2 REQ2")

        # 1.3

        self.demo("unlink TST1 REQ3")

        self.demo("remove REQ3")

        # 1.4

        self.demo()

    def test_tutorial_section_2(self):
        """Verify tutorial section 2.0 is working."""

        # Create a basic document
        self.demo("new REQ ./reqs")
        self.demo("add REQ")
        self.demo("add REQ")
        self.demo("new TST ./reqs/tests --parent REQ")
        self.demo("add TST")
        self.demo("add TST")
        self.demo("link TST1 REQ1")
        self.demo("link TST2 REQ1")
        self.demo("link TST2 REQ2")

        # 2.1

        self.demo("publish REQ")
        self.demo("publish TST")


if __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    unittest.main()
