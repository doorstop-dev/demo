"""Integration tests for the demo.cli package."""

import unittest
from unittest.mock import patch, Mock

import sys
import imp

from demo.gui.main import main
from demo.gui import main as gui


class TestMain(unittest.TestCase):  # pylint: disable=R0904

    """Integration tests for the 'doorstop-demo-gui' command."""

    @patch('demo.gui.main._run', Mock(return_value=True))
    def test_gui(self):
        """Verify 'doorstop-demo-gui' launches the GUI."""
        self.assertIs(None, main([]))

    @patch('demo.gui.main._run', Mock(return_value=False))
    def test_exit(self):
        """Verify 'doorstop-demo-gui' treats False as an error ."""
        self.assertRaises(SystemExit, main, [])

    @patch('demo.gui.main._run', Mock(side_effect=KeyboardInterrupt))
    def test_interrupt(self):
        """Verify 'doorstop-demo-gui' treats KeyboardInterrupt as an error."""
        self.assertRaises(SystemExit, main, [])


class TestImport(unittest.TestCase):  # pylint: disable=R0904

    """Integration tests for importing the GUI module."""

    def test_import(self):
        """Verify tkinter import errors are handled."""
        sys.modules['tkinter'] = Mock(side_effect=ImportError)
        imp.reload(gui)
        self.assertFalse(gui._run(None, None, lambda x: False))  # pylint: disable=W0212
        self.assertIsInstance(gui.tk, Mock)


@patch('demo.gui.main._run', Mock(return_value=True))  # pylint: disable=R0904
class TestLogging(unittest.TestCase):  # pylint: disable=R0904

    """Integration tests for the DoorstopDemo GUI logging."""

    def test_verbose_1(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main(['-v']))

    def test_verbose_2(self):
        """Verify verbose level 2 can be set."""
        self.assertIs(None, main(['-v', '-v']))

    def test_verbose_3(self):
        """Verify verbose level 1 can be set."""
        self.assertIs(None, main(['-v', '-v', '-v']))
