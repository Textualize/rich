from collections import OrderedDict
from typing import Generic, TypeVar

CacheKey = TypeVar("CacheKey")
CacheValue = TypeVar("CacheValue")


class LRUCache(Generic[CacheKey, CacheValue], OrderedDict):  # type: ignore # https://github.com/python/mypy/issues/6904
    """
    A dictionary-like container that stores a given maximum items.

    If an additional item is added when the LRUCache is full, the least
    recently used key is discarded to make room for the new item.

    """

    def __init__(self, cache_size: int) -> None:
        self.cache_size = cache_size
        super().__init__()

    def __setitem__(self, key: CacheKey, value: CacheValue) -> None:
        """Store a new views, potentially discarding an old value."""
        if key not in self:
            if len(self) >= self.cache_size:
                self.popitem(last=False)
        super().__setitem__(key, value)

    def __getitem__(
        self: "LRUCache[CacheKey, CacheValue]", key: CacheKey
    ) -> CacheValue:
        """Gets the item, but also makes it most recent."""
        value: CacheValue = super().__getitem__(key)
        super().__delitem__(key)
        super().__setitem__(key, value)
        return value
