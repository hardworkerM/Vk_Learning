from collections import deque


class LRUCache:
    Cache_dict = {}
    queue = deque()

    def __init__(self, limit=42):
        self.limit = limit

    def cache_check(self, key):
        if key in self.queue:
            self.queue.remove(key)
        self.queue.append(key)
        if len(self.queue) > self.limit:
            del self.Cache_dict[self.queue.popleft()]

    def get(self, key):
        self.cache_check(key)
        return self.Cache_dict[key]

    def set(self, key, value):
        self.Cache_dict[key] = value
        self.cache_check(key)

cache = LRUCache(2)
cache.set('k1', 'val1')
cache.set("k2", "val2")
cache.set("k1", "val3")
cache.set("k3", "val3")
cache.get('k1')
cache.get('k3')
cache.get('k3')
cache.get('k1')
cache.set("k2", "val2")
print(cache.Cache_dict)
print(cache.queue)


# print(cache.get("k3"))  # None
# print(cache.get("k2"))  # "val2"
# print(cache.get("k1"))  # "val1"
#
# cache.set("k3", "val3")
#
# print(cache.get("k3"))  # "val3"
# print(cache.get("k2"))  # None
# print(cache.get("k1"))  # "val1"
