"""
pytest configuration and setup for GitRadar.
"""

import sys
import typing

# Ensure typing backports are attached to standard typing module for Python < 3.11
# prior to pytest collecting test modules or importing dependencies like litellm.
if sys.version_info < (3, 11):
    try:
        import typing_extensions

        for _name in (
            "NotRequired",
            "Required",
            "Self",
            "Never",
            "LiteralString",
            "TypeAlias",
            "Override",
            "dataclass_transform",
        ):
            if not hasattr(typing, _name) and hasattr(typing_extensions, _name):
                setattr(typing, _name, getattr(typing_extensions, _name))
    except ImportError:
        pass
