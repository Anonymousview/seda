# Secure and Efficient DNN Accelerators with Hardware/Software Synergy

## Insight of typical secure accelerators

<div align=center>
<img src="https://github.com/user-attachments/assets/f510c0a4-0c2f-428a-a222-0c1901c8b40d" width="40%">
</div>

## Overview of SeDA architecture

<div align=center>
<img src="https://github.com/user-attachments/assets/a61b41d6-111e-47ec-8d4c-920883d11cc1" width="60%">
</div>


## Experiments

- [ ] Use the open-source cycle-level DNN simulator [scale-sim-v2](https://github.com/scalesim-project/scale-sim-v2.git) to analyze DNN model inference behaviors and memory protection scheme performance.
- [ ] Process DRAM access traces with a security simulator MPSim to calculate execution time and bandwidth usage.
- [ ] Simulate total DRAM access traces using  cycle-accurate DRAM simulator [ramulator2](https://github.com/CMU-SAFARI/ramulator2.git).




### DNN Simulation (SCALE-Sim2)

- Download the SCALE-Sim2 from [https://github.com/scalesim-project/scale-sim-v2.git](https://github.com/scalesim-project/scale-sim-v2.git).

#### 1. Setup Server and Edge devices configurations
path: `scale-sim-v2-main/configs`

- `server_google_tpu_v1.cfg`
- `edge_samsung_exynos.cfg`

#### 2. Obtain the DRAM traces of accelerators

- Open the file `scale-sim-v2-main/scalesim/scale_sim.py` 
- Change the code `save_trace = not self.save_space` to `save_trace = self.save_space`.
- Recompile scale-sim-v2 from the source code by the following command:

```
sudo python3 setup.py install
```

#### 3. Run the script program in batch mode

```
cd scale-sim-v2-main
./run_batch.py
```


### DRAM Simulation (Ramulator2-main)

- Download the Ramulator2-main from [ttps://github.com/CMU-SAFARI/ramulator2.git](https://github.com/CMU-SAFARI/ramulator2.git).


### Memory Protection Simulation (MPSim)


- lru_cache.py: LRU Cache Simulator
- mac.py: MAC Address Generator
- merkle_tree.py: Merkle Tree Simulator
- mpsim.py: Memory Protection Simulator


### AES-CTR

- aes-ctr-lib
- aes-ctr-py
- aes-ctr-verilog
- generate_sbox_c
- aes-ctr-diagram


### SHA256

- sha-256-lib
- sha-256-py
- sha-256-verilog
- sha256-diagram


<br>
<br>




> Updating...
