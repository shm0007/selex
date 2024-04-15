import numpy as np


L = 13 
NUM_NEIGHBORS = 2  

# Define functions to calculate each effect
def direct_interaction_effect(s, s_star):
    return np.sum(1 - np.equal(s, s_star))

def right_neighbor_effect(s, s_star):
    effect = 0
    for i in range(L):
        for j in range(1, NUM_NEIGHBORS+1):
            effect += s_star[j][i] - s[j][i]
    return effect

def left_neighbor_effect(s, s_star):
    effect = 0
    for i in range(L):
        for j in range(1, NUM_NEIGHBORS+1):
            effect += s_star[j][i] - s[j][i]
    return effect

def string_to_list(genome_string):

    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    
    genome_list = [char_to_index[char] for char in genome_string]
    
    return np.array(genome_list)

# Define fitness calculation function using Equation 10
def calculate_fitness(s, s_star):
    direct_effect = np.sum([direct_interaction_effect(s[i], s_star[i]) for i in range(L)])
    right_effect = np.sum([right_neighbor_effect(s, s_star) for i in range(L)])
    left_effect = np.sum([left_neighbor_effect(s, s_star) for i in range(L)])
    fitness = direct_effect + right_effect + left_effect
    return fitness

# Example genotype and target genotype (s and s_star)
s = np.random.randint(0, 4, size=(NUM_NEIGHBORS+1, L))  # Random genotype
s_star = np.random.randint(0, 4, size=(NUM_NEIGHBORS+1, L))  # Random target genotype

S_ORG = string_to_list('UCUAAGGCAGUAU')
print(s)
print(S_ORG)

# Calculate fitness using Equation 10
fitness = calculate_fitness(s, s_star)
print("Fitness:", fitness)

