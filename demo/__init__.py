"""Package for demo."""

__project__ = 'DoorstopDemo'
__version__ = '0.0.0'

CLI = 'doorstop-demo'
GUI = 'doorstop-demo-gui'
VERSION = __project__ + '-' + __version__

try:
    from demo.common import DemoError, DemoWarning, DemoInfo
    from demo.core import Item, Document, Tree
    from demo.core import build, report, find_document, find_item
except ImportError:  # pragma: no cover, manual test
    pass
