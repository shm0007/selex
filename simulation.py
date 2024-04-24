import random
import numpy as np
import csv

import time
# Constants
ALPHABET = ['A', 'G', 'C', 'U']
GENOTYPE_LENGTH = 20
POPULATION_SIZE = 10
MAX_ROUNDS = 60
MUTATION_RATE = 0.0001
NUM_RUNS = 100

average = 0
best = 100


#sequence length
L = 20 
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
    global average
    direct_effect = direct_interaction_effect(s,s_star)
    right_effect = right_neighbor_effect(s,s_star)
    left_effect = left_neighbor_effect(s,s_star)
    fitness = direct_effect + right_effect + left_effect
    return fitness


def string_to_list(genome_string):

    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    
    genome_list = [char_to_index[char] for char in genome_string]
    
    return np.array(genome_list)
# Generate random genotype
def generate_genotype():
    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    genome_list =  [char_to_index[random.choice(ALPHABET)] for _ in range(GENOTYPE_LENGTH)]
    return np.array(genome_list)

# Selection function
def selection(population, sample):
    global average
    selected_population = []
    for _ in range(len(population)):
        contenders = random.sample(population, 2)
        fitness1 = calculate_fitness(contenders[0],sample)
        fitness2 = calculate_fitness(contenders[1],sample)
        average += min(fitness1, fitness2)
        #selected = min(contenders, key=lambda x: calculate_fitness(x, sample))
        if fitness1 < fitness2:
            selected_population.append(contenders[0])
        else:
            selected_population.append(contenders[1])
    return (selected_population)

# Mutation function
def mutate(genotype):
    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    mutated_genotype = []
    for base in genotype:
        if random.random() < MUTATION_RATE:
            mutated_base = char_to_index[random.choice(ALPHABET)]
            while mutated_base == base:
                mutated_base = char_to_index[random.choice(ALPHABET)]
            mutated_genotype.append(mutated_base)
        else:
            mutated_genotype.append(base)
    return np.array(mutated_genotype)

# Evolutionary algorithm
def evolutionary_algorithm(sample):
    global average
    global best
    runs = 0
    result_avg = [[] for _ in range(61)]
    avg_avg = [[] for _ in range(61)]
    before = int(time.time())
    for i in range(NUM_RUNS):
        if i%10 == 0:
            print(f'Running run {i+1}')
        population = [generate_genotype() for _ in range(POPULATION_SIZE)]
        runs = 0
        average = 0
        best = 10000
        for _ in range(MAX_ROUNDS):
            runs+=1
            average = 0
            population = selection(population, sample)
            population = [mutate(genotype) for genotype in population]
            best_genotype = min(population, key=lambda x: calculate_fitness(x, sample))

            best_fitness = calculate_fitness(best_genotype, sample)
        

            best = min(best, best_fitness)
            result_avg[runs-1].append(best)
            
            avg_avg[runs-1].append(average/POPULATION_SIZE)
            #print("Round: ", runs, "Average:", average/POPULATION_SIZE, "Best Fitness:", best)

    best_name = 'best_csv_' + str(POPULATION_SIZE) +"_" +  str(before) + ".csv"
    avg_name = 'average_csv_' + str(POPULATION_SIZE) +"_" +  str(before) + ".csv"
    print('Total Time ' + str(int(time.time()) - before) )
    with open( best_name, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result_avg)
    with open( avg_name, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(avg_avg)
    


# Run evolutionary algorithm
sample = string_to_list('UGCUAGAAAGCAUGCGGGGA')
evolutionary_algorithm(sample)

