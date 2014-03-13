"""Integration tests for the demo.cli package."""

import unittest
from unittest.mock import patch, Mock

import os
import tempfile
import shutil

from demo.cli.main import main
from demo import common
from demo import settings

from demo.cli.test import ENV, REASON


@unittest.skipUnless(os.getenv(ENV), REASON)  # pylint: disable=R0904
class TestMain(unittest.TestCase):  # pylint: disable=R0904

    """Integration tests for the 'demo' command."""

    def setUp(self):
        self.cwd = os.getcwd()
        self.temp = tempfile.mkdtemp()
        self.backup = (settings.REFORMAT,
                       settings.CHECK_REF,
                       settings.CHECK_RLINKS)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.temp)
        (settings.REFORMAT,
         settings.CHECK_REF,
         settings.CHECK_RLINKS) = self.backup

    def test_main(self):
        """Verify 'demo' can be called."""
        self.assertIs(None, main([]))

    def test_main_help(self):
        """Verify 'demo --help' can be requested."""
        self.assertRaises(SystemExit, main, ['--help'])

    def test_main_error(self):
        """Verify 'demo' returns an error in an empty directory."""
        os.chdir(self.temp)
        self.assertRaises(SystemExit, main, [])

    def test_main_custom_root(self):
        """Verify 'demo' can be provided a custom root path."""
        os.chdir(self.temp)
        self.assertIs(None, main(['--project', '.']))

    @patch('demo.cli.main._run', Mock(return_value=False))
    def test_exit(self):
        """Verify 'demo' treats False as an error ."""
        self.assertRaises(SystemExit, main, [])

    @patch('demo.cli.main._run', Mock(side_effect=KeyboardInterrupt))
    def test_interrupt(self):
        """Verify 'demo' treats KeyboardInterrupt as an error."""
        self.assertRaises(SystemExit, main, [])

    def test_empty(self):
        """Verify 'demo' can be run in a working copy with no docs."""
        os.mkdir(os.path.join(self.temp, '.mockvcs'))
        os.chdir(self.temp)
        self.assertIs(None, main([]))
        self.assertTrue(settings.REFORMAT)
        self.assertTrue(settings.CHECK_REF)
        self.assertTrue(settings.CHECK_RLINKS)

    def test_options(self):
        """Verify 'demo' can be run with options."""
        os.mkdir(os.path.join(self.temp, '.mockvcs'))
        os.chdir(self.temp)
        self.assertIs(None, main(['--no-reformat',
                                  '--no-ref-check',
                                  '--no-rlinks-check']))
        self.assertFalse(settings.REFORMAT)
        self.assertFalse(settings.CHECK_REF)
        self.assertFalse(settings.CHECK_RLINKS)

    @patch('demo.cli.main.gui', Mock(return_value=True))
    def test_gui(self):
        """Verify 'demo --gui' launches the GUI."""
        self.assertIs(None, main(['--gui']))


@patch('demo.cli.main._run', Mock(return_value=True))  # pylint: disable=R0904
class TestLogging(unittest.TestCase):  # pylint: disable=R0904

    """Integration tests for the DoorstopDemo CLI logging."""

    def test_verbose_1(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main(['-v']))

    def test_verbose_2(self):
        """Verify verbose level 2 can be set."""
        self.assertIs(None, main(['-vv']))

    def test_verbose_3(self):
        """Verify verbose level 3 can be set."""
        self.assertIs(None, main(['-vvv']))

    def test_verbose_4(self):
        """Verify verbose level 4 can be set."""
        self.assertIs(None, main(['-vvvv']))

    def test_verbose_5(self):
        """Verify verbose level 5 cannot be set."""
        self.assertIs(None, main(['-vvvvv']))
        self.assertEqual(4, common.VERBOSITY)
