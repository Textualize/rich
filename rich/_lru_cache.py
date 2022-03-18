from typing import Dict, Generic, TypeVar, TYPE_CHECKING
import sys

CacheKey = TypeVar("CacheKey")
CacheValue = TypeVar("CacheValue")

if sys.version_info < (3, 8):
    from typing_extensions import OrderedDict
else:
    from collections import OrderedDict


class LRUCache(OrderedDict[CacheKey, CacheValue]):
    """
    A dictionary-like container that stores a given maximum items.

    If an additional item is added when the LRUCache is full, the least
    recently used key is discarded to make room for the new item.

    """

    def __init__(self, cache_size: int) -> None:
        self.cache_size = cache_size
        super(LRUCache, self).__init__()

    def __setitem__(self, key: CacheKey, value: CacheValue) -> None:
        """Store a new views, potentially discarding an old value."""
        if key not in self:
            if len(self) >= self.cache_size:
                self.popitem(last=False)
        OrderedDict.__setitem__(self, key, value)

    def __getitem__(self: Dict[CacheKey, CacheValue], key: CacheKey) -> CacheValue:
        """Gets the item, but also makes it most recent."""
        value: CacheValue = OrderedDict.__getitem__(self, key)
        OrderedDict.__delitem__(self, key)
        OrderedDict.__setitem__(self, key, value)
        return value
