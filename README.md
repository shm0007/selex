# Simulating Chemical Evolution
This repositority implements the algorithm described by In Soo Oh, Yuu-Geun Lee and RI McKay in their paper "Simulating Chemical Evolution" [Paper Link](https://ieeexplore.ieee.org/document/5949958) 

# Contents
- energy_matrix.py: An implementation of calculating energy matrix described in the paper.
- simulation.py: This Python script runs the evolutionary algorithm described in the paper.
- simulation-threads.py: An alternative version of the code with multithreading capabilities.

# Usage
```bash
python simulation.py <POPULATION_SIZE> <TOTAL_GENERATION> <TOTAL_ROUND> <NEIGHBOR_EFFECT>
```
Arguments:
- POPULATION_SIZE = total size of the population. In the paper, they simulated with the value of 10^6
- TOTAL_GENERATION = total generetion number. In the paper, they used 60
- TOTAL_RUN = total number of runs. In the paper, the value was 100
- NEIGHBOR_EFFECT = Either 0,1 or 2. Three types of neighbor effects are demonstrated in the paper:
  - 0: No neighbor effect.
  - 1: Nearest neighbor effect.
  - 2: Second neighbor effect.
# Example
```bash
python simulation.py 100000 60 100 0
```
This command simulates Figure 1 of the paper, with a population of 100,000, 60 total rounds, 100 total runs, and no neighbor effect.
