"""
GitRadar: Smart GitHub Market & Gap Analysis CLI tool.
"""

import sys
import typing

# Fix compatibility issue on Python < 3.11 where third-party packages (e.g. litellm)
# attempt to import 'NotRequired' or other PEP 655/673 types directly from 'typing'.
if sys.version_info < (3, 11):
    try:
        import typing_extensions

        for _name in ("NotRequired", "Required", "Self", "Never", "LiteralString", "TypeAlias", "Override", "dataclass_transform"):
            if not hasattr(typing, _name) and hasattr(typing_extensions, _name):
                setattr(typing, _name, getattr(typing_extensions, _name))
    except ImportError:
        pass

__version__ = "0.1.4"
__author__ = "GitRadar Developer"

