import numpy as np



#sequence length
L = 13 
# Number of nucleotide states
num_states = 4  

# Define standard deviations for sampling
sigma1 = 0.1
sigma2 = 0.01


# energy matrix for first neighbor
energy_mat_1st = {}

# energy matrix for second neighbor
energy_mat_2nd = {}

#calculating energy matrices
for s_star_i in range(num_states):
    for s_i in range(num_states):
        for s_star_neighbor in range(num_states):
            # Generate random value from Gaussian distribution
            energy1 = np.random.normal(0, sigma1)
            energy2 = np.random.normal(0, sigma2)
            
            
            if s_i == s_star_i:
                energy = 0
            # Store energy value in the energy matrix
            energy_mat_1st[((s_star_i), (s_i), (s_star_neighbor))] = energy1
            energy_mat_2nd[((s_star_i), (s_i), (s_star_neighbor))] = energy2


# Define functions to calculate each effect
def direct_interaction_effect(s, s_star):
    return np.sum(1 - np.equal(s, s_star))

def right_neighbor_effect(s, s_star):
    effect = 0
    for i in range(L):
        if i< L-1:
            effect += energy_mat_1st[(s_star[i],s[i], s_star[i+1])]
            effect -= energy_mat_1st[(s[i],s_star[i], s[i+1])]
        if i < L-2:
            effect += energy_mat_2nd[(s_star[i],s[i], s_star[i+2])]
            effect -= energy_mat_2nd[(s[i],s_star[i], s[i+2])]
    return effect


def left_neighbor_effect(s, s_star):
    effect = 0
    for i in range(L):
        if i-1 >= 0:
            effect += energy_mat_1st[(s_star[i],s[i], s_star[i-1])]
            effect -= energy_mat_1st[(s[i],s_star[i], s[i-1])]
        if i -2 >=0:
            effect += energy_mat_2nd[(s_star[i],s[i], s_star[i-2])]
            effect -= energy_mat_2nd[(s[i],s_star[i], s[i-2])]
    return effect

def string_to_list(genome_string):

    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    
    genome_list = [char_to_index[char] for char in genome_string]
    
    return np.array(genome_list)

# Define fitness calculation function using Equation 10
def calculate_fitness(s, s_star):
    direct_effect = direct_interaction_effect(s,s_star)
    right_effect = right_neighbor_effect(s,s_star)
    left_effect = left_neighbor_effect(s,s_star)
    fitness = direct_effect + right_effect + left_effect
    return fitness

# Example genotype and target genotype (s and s_star)
s = string_to_list('UCUAAGGCAGUAU')
s_star = string_to_list('CUGACUGAACGUU')

# Calculate fitness using Equation 10
fitness = calculate_fitness(s, s_star)
print("Fitness:", fitness)

