import math

class MegAuCode:
    def __init__(self, secure_mem_size: int, mac_size: int, data_block_size: int, cacheline_size: int=64) -> None:

        self.ini_mac_addr = secure_mem_size
        self.data_block_size = data_block_size
        self.num_macs = int(secure_mem_size / data_block_size)
        self.mac_size = mac_size
        self.macs_in_cacheline = int(cacheline_size / mac_size) 

    def get_mac_addr(self, data_block_addr: int) -> int:
        cur_mac_addr = self.ini_mac_addr + math.floor(data_block_addr / self.data_block_size) * self.mac_size
        macs_in_cur_cacheline = [cur_mac_addr + i * self.mac_size for i in range(self.macs_in_cacheline)] 

        return macs_in_cur_cacheline

    def get_mac_addr_w(self, data_block_addr: int) -> int:
        cur_mac_addr = self.ini_mac_addr + math.floor(data_block_addr / self.data_block_size) * self.mac_size
        return cur_mac_addr



# capacity = 64 * 4 # 448B
# cache_line_size = 64 #64B
# mac_cache = LRUCache(capacity, cache_line_size)

# mac_size = 8 # 8B = 64-bit
# data_block_size = 64 # 64B
# mac = MegAuCode(cache_line_size, mac_size, data_block_size)

# data_block_addr = {0, 1, 2, 64*8-1, 64*8, 64*8*2, 64*8*3, 64*8*4, 64*8*4+1, 64*8*4+2}
# sorted_data_block_addr = sorted(data_block_addr)

# total_miss_list = []

# for addr in sorted_data_block_addr:
#     print(f"\nCurrent data block address: {addr}")
#     # mac_addr = math.ceil((addr + 1) / (data_block_size * num_mac_each_cacheline))
#     mac_addr = mac.get_mac_addr(addr)
#     print(f"Current mac address: {mac_addr}")
#     mac_cache.check_node_list([(mac_addr, "MAC-ADDR")])
#     total_miss_list += mac_cache.get_miss_list()
#     print(f"Current miss count: {mac_cache.get_curr_miss_count()}")
#     print(f"Total miss count: {mac_cache.get_total_miss_count()}")
#     mac_cache.clear_all()

# mac_miss_hit_rate = mac_cache.get_total_miss_count() / len(sorted_data_block_addr)
# print(f"\nMAC miss hit rate: {mac_cache.get_total_miss_count()} / {len(sorted_data_block_addr)} = {mac_miss_hit_rate:.4f}\n")

# mac_cache.print_cache()
# mac_cache.print_miss_list()

# def print_total_miss_list(total_miss_list) -> None:
#         cnt = 1
#         if len(total_miss_list) != 0:
#             print("\n\nTotal missing hit list: ")
#         for node, level_info in total_miss_list:
#             print(f"[{cnt}] {level_info}: {node}")
#             cnt += 1

# print_total_miss_list(total_miss_list)
