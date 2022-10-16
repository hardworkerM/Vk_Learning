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


def filter_file(file, sc_list: list):
    for i, val in enumerate(sc_list):
        sc_list[i] = val.lower()
    for line in file:
        flag = False
        for word in line[:-1].split(' '):
            if word.lower() in sc_list:
                flag = True
                break
        if flag:
            yield line[:-1]
        else:
            yield None
