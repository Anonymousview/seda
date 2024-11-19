from collections import OrderedDict
import math

class LRUCache:
    def __init__(self, capacity: int = 8*2**10, cache_line_size: int = 64):
        self.cache = OrderedDict()
        self.cache_size = 8
        self.cache_num = math.floor(capacity / self.cache_size)
        self.total_miss_cnt = 0
        self.curr_miss_cnt = 0
        self.write_cnt = 0
        self.miss_list = []
        self.dirty = set()  
        self.dirty_list = [] 

    def update_cache(self, nodes: list, flag: str = 'LD') -> None:
        # Add new cacheline: miss a new MAC/Hash row into cacheline
        for node in nodes: 
            # self.cache[node.node] = flag
            self.cache[node] = flag # update timestamp
        while len(self.cache) > self.cache_num:
            evicted_node, evicted_level_info = self.cache.popitem(last=False)


    def write_back(self, node: int, level_info: str) -> None:
        # Simulate writing back to main memory or storage
        self.write_cnt += 1
        
    def check_node_list(self, nodes: list, flag: str) -> None:
        if nodes[0] in self.cache: # hit
            if flag == 'LD':
                pass

        else: # miss
            self.miss_list.append(nodes[0]) 
            self.total_miss_cnt += 1
            self.curr_miss_cnt += 1 
            self.update_cache(nodes, flag) 

    def flush_dirty_cache(self):
        for node in self.dirty:
            self.write_cnt += 1
        self.dirty.clear()


    def get_total_miss_count(self) -> int:
        return self.total_miss_cnt
    
    def get_curr_miss_count(self) -> int:
        return self.curr_miss_cnt
    
    def get_miss_list(self) -> list:
        # self.print_miss_list()
        return self.miss_list
    
    def get_cache_list(self) -> list:
        # self.print_cache()
        return self.cache
    
    def get_write_count(self) -> int:
        return self.write_cnt

    def print_cache(self) -> None:
        print("LRUCache: ")
        print(self.cache)
        print(f"len: {len(self.cache)}\n")

    def print_miss_list(self) -> None:
        if len(self.miss_list) != 0:
            print("Missing list: ")
        for node in self.miss_list:
            print(f"{node}")
    
    def clear_all(self) -> None:
        self.miss_list.clear()
        self.curr_miss_cnt = 0
    
    def clear_all_params(self) -> None:
        self.cache.clear()
        self.miss_list.clear()
        self.total_miss_cnt = 0
        self.curr_miss_cnt = 0
        self.write_cnt = 0
        self.dirty.clear()
        self.dirty_list.clear()

