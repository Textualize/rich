from __future__ import unicode_literals


from rich._lru_cache import LRUCache


def test_lru_cache():
    cache = LRUCache(3)

    # insert some values
    cache["foo"] = 1
    cache["bar"] = 2
    cache["baz"] = 3
    assert "foo" in cache

    #  Cache size is 3, so the following should kick oldest one out
    cache["egg"] = 4
    assert "foo" not in cache
    assert "egg" in "egg" in cache

    # cache is now full
    # look up two keys
    cache["bar"]
    cache["baz"]

    # Insert a new value
    cache["eggegg"] = 5
    # Check it kicked out the 'oldest' key
    assert "egg" not in cache
