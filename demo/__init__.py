"""Package for demo."""

__project__ = 'Doorstop'
__version__ = '0.2'

CLI = 'demo-demo'
GUI = 'demo-demo-gui'
VERSION = __project__ + '-' + __version__

try:
    from demo.common import DemoError, DemoWarning, DemoInfo
    from demo.core import Item, Document, Tree
    from demo.core import build, report, find_document, find_item
except ImportError:  # pragma: no cover, manual test
    pass
