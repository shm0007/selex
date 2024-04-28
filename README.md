# Simulating Chemical Evolution
This repositority implements the algorithm described by In Soo Oh, Yuu-Geun Lee and RI McKay in their paper "Simulating Chemical Evolution"(Paper Link: https://ieeexplore.ieee.org/document/5949958)
# Usage
```bash
python simulation.py <POPULATION_SIZE> <TOTAL_GENERATION> <TOTAL_ROUND> <NEIGHBOR_EFFECT>
```
Arguments:
- POPULATION_SIZE = total size of the population. In the paper, they simulated with the value 10^6
- TOTAL_GENERATION = total generetion number. In the paper, they used 60
- TOTAL_RUN = total number of runs. In the paper, the value was 100
- NEIGHBOR_EFFECT = 0/1/2 Paper demostrated three type of neighbor effect, 0 is no neighbor effect, 1 is nearest neighbor effect, 2 is second neighbor effect

# Example
```bash
python simulation.py 100000 60 100 0
```
This will simulate Figure 1 of the paper(Population 100000, total round 60, total run 100 and no neighbor effect)
