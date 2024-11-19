# Secure and Efficient DNN Accelerators with Hardware/Software Synergy


## DNN Simulator (SCALE-Sim2)

- Download the SCALE-Sim2 from https://github.com/scalesim-project/scale-sim-v2.git

### 1. Setup Server and Edge Devices configurations
path: scale-sim-v2-main/configs

server_google_tpu_v1.cfg
edge_samsung_exynos.cfg

### 2. Obtain the DRAM traces of accelerators

- Open file scale-sim-v2-main/scalesim/scale_sim.py 
- Change the code `save_trace = not self.save_space` to `save_trace = self.save_space`.
- Then, recompile scale-sim-v2 from the source code:

```
sudo python3 setup.py install
```

### 3. Run the script program in batch mode

```
cd scale-sim-v2-main
./run_batch.py
```


## DRAM Simulator (Ramulator2-main)

- Download the Ramulator2-main from https://github.com/CMU-SAFARI/ramulator2.git


## Memory Protection Simulator (MPSim)

- lru_cache.py: LRU Cache Simulator
- mac.py: MAC Address Generator
- merkle_tree.py: Merkle Tree Simulator
- mpsim.py: Memory Protection Simulator

