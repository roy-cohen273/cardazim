"""A driver is registered to `Driver.drivers` only if it's imported.
This file imports all drivers, and thus registers them.
"""

__all__ = ('FSDriver', 'MongoDBDriver')

from fs_driver import FSDriver
from mongodb_driver import MongoDBDriver
