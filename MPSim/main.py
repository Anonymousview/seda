import os
import sys
import time
import math
from tqdm import tqdm

from merkle_tree import MerkelTree
from lru_cache import LRUCache
from mac import MegAuCode

###### 1 Setup params
secure_mem_size = 8*2**30 # 8GB=8*2^30=8*8^10=8^11
data_block_size = 64 #64B
cacheline_size = 64 #64B

mac_size = 8 #8B
# mac_size = 16 #8B
vn_size = 8 #8B for data block
vn_mac_size = 8 #8B for merkle tree
ary = cacheline_size // vn_mac_size #8B

print("\n************************************** initialization start *************************************")
###### 1.1 Build Merkle Tree, create level_table
print("Building Merkle Tree >>> ")
mt = MerkelTree(secure_mem_size, data_block_size, cacheline_size, ary)
print(f"level_num: {mt.get_level_num()}") # number of merkle tree, which stores vn_macs form root to leaf, but not vns
# Print built Merkel Tree (no leaf level)
mt.print_no_leaf_level() # first address of every level in merkle tree (root in both dram and sram!)

###### 1.2 Setup Message Authentication Code (MAC)
print("Building MAC >>> ")
mac = MegAuCode(secure_mem_size, mac_size, data_block_size)

###### 1.3 Setup LRU Cache
print("Building LRU Cache >>> ")
vn_cache_capacity = 16 * 2**10 
mac_cache_capacity = 8 * 2**10 
total_vn_miss_list = []
total_mac_miss_list = []
vn_cache = LRUCache(vn_cache_capacity, cacheline_size)
mac_cache = LRUCache(mac_cache_capacity, cacheline_size)
# print(f"Total number of vn cacheline: {vn_cache.cacheline_num}")
# print(f"Total number of mac cacheline: {mac_cache.cacheline_num}")
print(f"Total number of vn cache: {vn_cache.cache_num}")
print(f"Total number of mac cache: {mac_cache.cache_num}")
print("************************************** initialization done **************************************\n")

################################ Set params ###############################
# 2 Read trace file
model = "alexnet" # alexnet, mobilenet, Resnet, Googlenet, DLRM, VGG16, lenet, Transformer
mode = "filter_read" # ifmap_read, filter_read, ofmap_write
flag_rw = 0 # 0:read, 1:write
# accelerator = 'server' # server, edge (samsung exynos)

# 3 Save results to a file
def write_total_miss_list(total_miss_list, input_file: str, name: str) -> None:
    with open(input_file, 'w') as file:
        if len(total_miss_list) != 0:
            print(f"Write {name} missing hit list into file: {input_file}")
            for node in total_miss_list:
                file.write(f"{node}\n")


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

ini_vn_addr = mt.ini_vn_addr
ini_vn_mac_addr = mt.ini_vn_mac_addr


models = [
    "lenet",
    "alexnet",
    "mobilenet",
    "resnet18",
    "Googlenet",
    "DLRM",
    "AlphaGoZero",
    "DeepSpeech2",
    "FasterRCNN",
    "NCF_recommendation",
    "Sentimental_seqCNN",
    "transformer_fwd",
    "yolo_tiny"
]
modes = ["ifmap_read", "filter_read", "ofmap_write"]
# dataflow = "is" # os ws is
dataflows = ["os", "ws", "is"] # os ws is
accelerators = [
    f"server_GoogleTPU_v1",
    f"edge_samsung_exynos"
]

total_start_time = time.time()

# output_file_result = 'results_traffic.txt'
output_file_results = ["results_traffic_os.txt", "results_traffic_ws.txt", "results_traffic_is.txt"]
res_idx = 0

for idx_df in range(len(dataflows)):
    with open(output_file_results[idx_df], 'w') as out_file:
        out_file.write(f"***************** memory protection traffic *****************\n")
        print(f"\n{GREEN}[output_file_result]>>>>>>>>>>>>>>>>>>>>>: {output_file_results[idx_df]}{RESET}")
        for model in models:
            for accelerator in accelerators:

                acce_flow = f"{accelerator}_{dataflows[idx_df]}"
                output_path = f'output_secsim_benchmarks/{model}_{acce_flow}'
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                
                for mode in modes:
                    out_file.write(f"\n[{model}-{acce_flow}-{mode}]\n")
                    print("\n************************************** simulation start **************************************")
                    input_path = f'output_scalesim_benchmarks/{model}_{acce_flow}'
                    input_file = f'{input_path}/{mode}_origin.txt'
                    print(f"Input file: {input_file}")
                    if not os.path.exists(input_file):
                        print(f"Error: The file {input_file} does not exist.")
                        sys.exit(1)

                    start_time = time.time()
                    total_lines = 0
                    
                    with open(input_file, 'r') as file:
                        lines = file.readlines()
                        if mode != "ofmap_write": 
                            for line in tqdm(lines, desc="Processing lines (read)", ncols=100):
                                total_lines += 1
                                data_addr = int(line, 16) 
                                
                                cur_vn_addr = ini_vn_addr + math.floor(data_addr / data_block_size) * vn_size
                                vn_addr_list = [cur_vn_addr + i * vn_size for i in range(cacheline_size // vn_size)]
                                vn_cache.check_node_list(vn_addr_list, "LD")
                                total_vn_miss_list += vn_cache.get_miss_list()

                                vn_addr_list.clear()
                                vn_cache.clear_all()

                                mt.generate_node_list_traversed(data_addr)
                                vn_mac_addr_list = mt.get_node_list_traversed()

                                extended_node_list = []
                                for node_id in vn_mac_addr_list:
                                    extended_node_list.extend([node_id + i * vn_mac_size for i in range(cacheline_size // vn_mac_size)])
                                    vn_cache.check_node_list(extended_node_list, "LD")
                                    total_vn_miss_list += vn_cache.get_miss_list()

                                    extended_node_list.clear()
                                    vn_cache.clear_all()

                                vn_mac_addr_list.clear()

                                macs_in_cur_cacheline = mac.get_mac_addr(data_addr)
                                mac_cache.check_node_list(macs_in_cur_cacheline, "LD") 
                                total_mac_miss_list += mac_cache.get_miss_list()
                                # with open(output_file_mac, 'a') as file:
                                #     for node in mac_cache.get_miss_list():
                                #         file.write(f"{node}\n")
                                # mac_cache.print_cache()
                                mac_cache.clear_all()
                            
                            # print on terminal
                            num_mac_miss_read = mac_cache.get_total_miss_count()
                            num_vn_miss_read = vn_cache.get_total_miss_count()
                            total_num_read = (num_vn_miss_read + num_mac_miss_read + total_lines)

                            mac_miss_hit_rate = num_mac_miss_read / total_lines
                            mac_miss_traffic = num_mac_miss_read / total_num_read

                            vn_miss_hit_rate = num_vn_miss_read / total_lines
                            vn_miss_traffic = num_vn_miss_read / total_num_read

                            print("\n***********************************************************")
                            print(f"Total mac miss count: {num_mac_miss_read}")
                            print(f"MAC miss hit rate: {num_mac_miss_read} / {total_lines} = {mac_miss_hit_rate:.4f}")
                            print(f"MAC traffic: {num_mac_miss_read} / ({num_vn_miss_read}+{num_mac_miss_read}+{total_lines}) = {mac_miss_traffic:.4f}")

                            print(f"\nTotal vn miss count: {num_vn_miss_read}")
                            print(f"VN miss hit rate: {num_vn_miss_read} / {total_lines} = {vn_miss_hit_rate:.4f}")
                            print(f"VN traffic: {num_vn_miss_read} / ({num_vn_miss_read}+{num_mac_miss_read}+{total_lines}) = {vn_miss_traffic:.4f}")
                            print("***********************************************************\n")

                            out_file.write(f"Total origin traffic: {total_lines}\n")
                            out_file.write(f"Total mac traffic: {num_mac_miss_read}\n")
                            out_file.write(f"Total vn traffic: {num_vn_miss_read}\n")
                            out_file.write(f"Total mac traffic overhead: {mac_miss_traffic}\n")
                            out_file.write(f"Total vn traffic overhead: {vn_miss_traffic}\n")

                            name = "mac"
                            output_file = f"{output_path}/{mode}_secure_mac.txt" 
                            write_total_miss_list(total_mac_miss_list, output_file, name)


                            name = "vn"
                            output_file = f"{output_path}/{mode}_secure_vn.txt" 
                            write_total_miss_list(total_vn_miss_list, output_file, name)

                            total_mac_miss_list.clear()
                            total_vn_miss_list.clear()
                            vn_cache.clear_all_params()
                            mac_cache.clear_all_params()

                        else:
                            total_vn_mac_miss_set = set()
                            for line in tqdm(lines, desc="Processing lines (write)", ncols=100):
                                total_lines += 1
                                data_addr = int(line, 16)

                                if total_lines % (cacheline_size // mac_size) == 1:
                                    total_mac_miss_list += [mac.get_mac_addr_w(data_addr)]
                                    total_vn_miss_list += [mt.get_vn_addr_w(data_addr)]

                                    mt.generate_node_list_traversed(data_addr)
                                    total_vn_mac_miss_set.update(mt.get_node_list_traversed())
                                    
                            num_mac_miss_write = len(total_mac_miss_list)
                            num_vn_miss_write = len(total_vn_miss_list)
                            num_vn_mac_miss_write = len(total_vn_mac_miss_set)
                            total_num_write = num_mac_miss_write + num_vn_miss_write + num_vn_mac_miss_write + total_lines

                            mac_miss_hit_rate = num_mac_miss_write / total_lines
                            mac_miss_traffic = num_mac_miss_write / total_num_write

                            vn_miss_hit_rate = (num_vn_miss_write + num_vn_mac_miss_write) / total_lines
                            vn_miss_traffic = (num_vn_miss_write + num_vn_mac_miss_write) / total_num_write

                            print(f"Total mac miss count: {num_mac_miss_write}")
                            print(f"MAC miss hit rate: {num_mac_miss_write} / {total_lines} = {num_mac_miss_write / total_lines:.4f}")
                            print(f"MAC traffic: {num_mac_miss_write} / ({num_mac_miss_write}+{num_vn_miss_write}+{num_vn_mac_miss_write}+{total_lines}) = {num_mac_miss_write / total_num_write:.4f}")

                            print(f"\nTotal vn miss count: {num_vn_miss_write}")
                            print(f"Total vn_mac miss count: {num_vn_mac_miss_write}")
                            print(f"Total vn+vn_mac miss count: {num_vn_miss_write + num_vn_mac_miss_write}")
                            print(f"VN+VN_MAC miss hit rate: ({num_vn_miss_write}+{num_vn_mac_miss_write}) / {total_lines} = {(num_vn_miss_write + num_vn_mac_miss_write) / total_lines:.4f}")
                            print(f"VN+VN_MAC traffic: ({num_vn_miss_write}+{num_vn_mac_miss_write}) / ({num_mac_miss_write}+{num_vn_miss_write}+{num_vn_mac_miss_write}+{total_lines}) = {(num_vn_miss_write + num_vn_mac_miss_write) / total_num_write:.4f}")

                            out_file.write(f"Total origin traffic: {total_lines}\n")
                            out_file.write(f"Total mac traffic: {num_mac_miss_write}\n")
                            out_file.write(f"Total vn traffic: {num_vn_miss_write + num_vn_mac_miss_write}\n")
                            out_file.write(f"Total mac traffic overhead: {mac_miss_traffic}\n")
                            out_file.write(f"Total vn traffic overhead: {vn_miss_traffic}\n")
                            

                            name = "mac"
                            output_file = f"{output_path}/{mode}_secure_mac.txt" 
                            print(f"Output file: {output_file}")
                            write_total_miss_list(total_mac_miss_list, output_file, name)

                            name = "vn"
                            output_file = f"{output_path}/{mode}_secure_vn.txt" 
                            total_vn_mac_miss_list = total_vn_miss_list + list(total_vn_mac_miss_set)
                            write_total_miss_list(total_vn_mac_miss_list, output_file, name)

                            total_mac_miss_list.clear()
                            total_vn_miss_list.clear()
                            total_vn_mac_miss_set.clear()

                            mac_cache.clear_all_params()


                        vn_cache.flush_dirty_cache()
                        mac_cache.flush_dirty_cache()
                
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"\nTotal lines: {total_lines}")
                    print(f"Elapsed time: {elapsed_time:.2f} seconds")
                    print(f"input_file: {input_file}")
                    print("************************************** simulation done **************************************\n\n")

total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time
print(f"Total elapsed time: {total_elapsed_time:.2f} seconds")
print("done!")