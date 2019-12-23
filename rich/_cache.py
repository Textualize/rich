from collections import OrderedDict
from typing import Generic, TypeVar


CacheType = TypeVar("CacheType")


class LRUCache(Generic[CacheType], OrderedDict):
    """
    A dictionary-like container that stores a given maximum items.

    If an additional item is added when the LRUCache is full, the least
    recently used key is discarded to make room for the new item.

    """

    def __init__(self, cache_size: int) -> None:
        self.cache_size = cache_size
        super(LRUCache, self).__init__()

    def __setitem__(self, key: bytes, value: CacheType) -> None:
        """Store a new views, potentially discarding an old value."""
        if key not in self:
            if len(self) >= self.cache_size:
                self.popitem(last=False)
        OrderedDict.__setitem__(self, key, value)

    def __getitem__(self, key: bytes) -> CacheType:
        """Gets the item, but also makes it most recent."""
        value: CacheType = OrderedDict.__getitem__(self, key)
        OrderedDict.__delitem__(self, key)
        OrderedDict.__setitem__(self, key, value)
        return value
