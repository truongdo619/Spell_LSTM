class LRUValue(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.nxt = None

    def set_next(self, nxt):
        self.nxt = nxt

    def set_prev(self, prev):
        self.prev = prev


class LRUCache(object):
    MAX_ITEMS_IN_CACHE = 512

    def __init__(self, max_items):
        LRUCache.MAX_ITEMS_IN_CACHE = max_items
        self.current_cache = {}
        self.head = None
        self.tail = None

    def get_item(self, key):
        norm_key = tuple(sorted(key.items()))
        if norm_key in self.current_cache.keys():
            # Move to head
            if self.current_cache[norm_key] != self.head:
                nxt = self.current_cache[norm_key].nxt
                if self.current_cache[norm_key] != self.tail:
                    prev = self.current_cache[norm_key].prev
                    prev.set_next(nxt)
                    nxt.set_prev(prev)
                else:
                    nxt.set_prev(None)
                    self.tail = nxt
                self.head.set_next(self.current_cache[norm_key])
                self.current_cache[norm_key].set_prev(self.head)
                self.head = self.current_cache[norm_key]
            return self.current_cache[norm_key].value
        else:
            return None

    def insert_item(self, key, value):
        norm_key = key
        if self.head is None and self.tail is None:
            self.current_cache[norm_key] = LRUValue(key, value)
            self.tail = self.current_cache[norm_key]
            self.head = self.current_cache[norm_key]
        else:
            if norm_key in self.current_cache.keys():
                # Move to head
                if self.current_cache[norm_key] != self.head:
                    nxt = self.current_cache[norm_key].nxt
                    if self.current_cache[norm_key] != self.tail:
                        prev = self.current_cache[norm_key].prev
                        prev.set_next(nxt)
                        nxt.set_prev(prev)
                    else:
                        nxt.set_prev(None)
                        self.tail = nxt
                    self.head.set_next(self.current_cache[norm_key])
                    self.head = self.current_cache[norm_key]
            else:
                # Add to head
                self.current_cache[norm_key] = LRUValue(key, value)
                self.head.set_next(self.current_cache[norm_key])
                self.current_cache[norm_key].set_prev(self.head)
                self.head = self.current_cache[norm_key]

        self.update_cache()
        return 1

    def update_cache(self):

        while len(self.current_cache) > LRUCache.MAX_ITEMS_IN_CACHE and len(self.current_cache) > 1:
            cur_tail = self.tail
            cur_tail_key = cur_tail.key
            nxt_tail = cur_tail.nxt
            nxt_tail.set_prev(None)
            self.tail = nxt_tail
            del self.current_cache[cur_tail_key]
            del cur_tail
            del cur_tail_key
