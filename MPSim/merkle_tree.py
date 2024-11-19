import math

#            0              -> Level-1 (Root)
#        /       \
#       1         2         -> Level-2
#      / \       /  \
#     3    4    5    6      -> Level-3
#    / \  / \  / \   / \
#   7   8 9 10 11 12 13 14  -> Level-4 (Leaf nodes)

class MerkelTree:
    level_num = 0
    level_table = {}
    node_list_traversed = []
    ary = 0
    curr_level_num = 0

    def __init__(self, secure_mem_size: int, data_block_size: int, cacheline_size: int, ary: int): # ary=8

        self.ini_vn_addr = secure_mem_size + int(secure_mem_size / data_block_size) * 8 
        self.ini_vn_mac_addr = secure_mem_size + 2 * int(secure_mem_size / data_block_size) * 8

        self.ary = ary
        self.data_block_size = data_block_size
        self.cacheline_size = cacheline_size
        self.num_vns = int(secure_mem_size / data_block_size)
        self.vn_size = 8 
        self.vn_mac_size = 8 
        self.merkletree_last_level_num = int(self.num_vns / (self.data_block_size / self.vn_mac_size)) 
        self.level_num = int(math.log(self.merkletree_last_level_num, self.ary)) + 1
        
        self.level_table[1] = self.ini_vn_mac_addr
        total = self.ini_vn_mac_addr

        for level_idx in range(1, self.level_num):
            total += self.ary ** (level_idx - 1)
            self.level_table[level_idx+1] = total
    
    def get_node_id_by_level_idx(self, level_idx: int) -> int:
        if level_idx < 0 or level_idx > self.level_num:
            return -1000000 # ERROR tag
        
        return self.level_table.get(level_idx, None)

    def get_level_num(self) -> int:
        return self.level_num

    def generate_node_list_traversed(self, address: int):
        offset = math.floor(address / (self.data_block_size * (self.data_block_size / self.vn_mac_size))) 
        self.curr_level_num = self.level_num
        parent_node_id = offset + self.get_node_id_by_level_idx(self.curr_level_num) 
        str_level_info = f"L-{self.curr_level_num}-{offset+1}"
        self.node_list_traversed.append(parent_node_id)

        self.curr_level_num -= 1
        while self.curr_level_num > 1:
            offset = math.floor(offset / self.ary)
            parent_node_id = offset + self.get_node_id_by_level_idx(self.curr_level_num)
            str_level_info = f"L-{self.curr_level_num}-{offset+1}"
            self.node_list_traversed.append(parent_node_id)
            self.curr_level_num -= 1

    def get_vn_addr(self, data_block_addr: int) -> int: 
        cur_vn_addr = self.ini_vn_addr + math.floor(data_block_addr / self.data_block_size) * self.vn_size
        vns_in_cur_cacheline = [cur_vn_addr + i * self.vn_size for i in range(self.cacheline_size // self.vn_size)]

        return vns_in_cur_cacheline

    def get_vn_addr_w(self, data_block_addr: int) -> int: 
        cur_vn_addr = self.ini_vn_addr + math.floor(data_block_addr / self.data_block_size) * self.vn_size

        return cur_vn_addr

    def get_node_list_traversed(self) -> list: # root stored in SRAM, other nodes stored in DRAM
        cur_list = [self.ini_vn_mac_addr + (node - self.ini_vn_mac_addr -1) * self.vn_mac_size for node in self.node_list_traversed]
        self.node_list_traversed.clear()
        return cur_list
    
    def clear_all(self):
        self.node_list_traversed.clear()

    
    def print_node_list_traversed(self) -> None:
        print("generate_node_list_traversed: ")
        print(f"len: {len(self.node_list_traversed)}")
        if len(self.node_list_traversed) == 0:
            print("This is root.")
        # for node, level_info in self.node_list_traversed:
        #     print(f"{level_info}: {node}")
        for node in self.node_list_traversed:
            print(f"{node}")

    def print_no_leaf_level(self):
        print("Merkel Tree's Level Table: index of first node of each level{no leaf nodes (data blocks)}")
        for level_idx, level_idx_node_1 in self.level_table.items():
            print(f"Level {level_idx} (L-{level_idx}-1): {level_idx_node_1}")
        print("Merkel Tree's Level Table: addr of first node of each level{no leaf nodes (data blocks)}, no root node")
        for level_idx, level_idx_node_1 in self.level_table.items(): 
            print(f"Level {level_idx} (L-{level_idx}-1): {self.ini_vn_mac_addr + (level_idx_node_1 - self.ini_vn_mac_addr -1) * self.vn_mac_size}")
