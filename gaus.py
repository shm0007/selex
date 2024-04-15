import numpy as np


def get(c):
    c = c%4
    return chr(c+ 97)
# Define parameters
num_states = 4  # Number of nucleotide states
num_neighbors = 3  # Number of neighbors (including central position)

# Define standard deviations for sampling
sigma1 = 0.01
sigma2 = 0.001

# Generate random values for the energy matrix
energy_matrix = {}
for s_star_i in range(num_states):
    for s_i in range(num_states):
        for s_star_neighbor in range(num_states):
            # Determine standard deviation based on the neighbor's position
            if s_star_neighbor == s_star_i or s_star_neighbor == s_star_i - 2:
                std_dev = sigma2
            else:
                std_dev = sigma1
            
            # Generate random value from Gaussian distribution
            energy = np.random.normal(0, std_dev)
            
            # Store energy value in the energy matrix
            energy_matrix[(s_star_i, s_i, s_star_neighbor)] = energy

# Print the energy matrix
ct =0
for s_is in range(4):
    print(f"\ns_i* {get(s_is)}    s_i*+-1 = { get(s_is +1 )}           s_i*+-1 = {get(s_is+2)}         s_i*+-1 = {get(s_is+3)}           s_i*+-1 = {get(s_is)}")
    for s_i in range(4):
        if s_i == s_is:
            continue # same thing energy zero
        print(f'\ns_i = {get(s_i)}    ', end= "")
        for s_i_n in range(4):
            print(round(energy_matrix[(s_i, s_i, s_i_n)],3),end= "      ")


print(energy_matrix[(0,1,2)])
