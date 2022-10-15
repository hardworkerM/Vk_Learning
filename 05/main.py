from collections import deque
import io


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


def filter_file(name: str, sc_list: list):
    for i in range(len(sc_list)):
        sc_list[i] = sc_list[i].lower()
    print(sc_list)
    with io.open(name, encoding='utf-8') as f:
        for line in f:
            for word in line.split(' '):
                if word.lower() in sc_list:
                    yield line
            yield None


gen = filter_file('file.txt', ['И', 'Белая', 'В'])
for i in range(20):
    print(next(gen))
