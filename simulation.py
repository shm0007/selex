import random
import numpy as np
from fitness import calculate_fitness
# Constants
ALPHABET = ['A', 'G', 'C', 'U']
GENOTYPE_LENGTH = 20
POPULATION_SIZE = 100
MAX_ROUNDS = 60
MUTATION_RATE = 0.0001
NUM_RUNS = 100

aveg = 0
best = 100000
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
    selected_population = []
    for _ in range(len(population)):
        contenders = random.sample(population, 2)
        selected = max(contenders, key=lambda x: calculate_fitness(x, sample))
        selected_population.append(selected)
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

def evolutionary_algorithm():
    global aveg
    global best
    runs = 0
    sample = generate_genotype()  # Generate sample
    for _ in range(NUM_RUNS):
        runs+=1
        population = [generate_genotype() for _ in range(POPULATION_SIZE)]

        for _ in range(MAX_ROUNDS):
            population = selection(population, sample)
            population = [mutate(genotype) for genotype in population]
        best_genotype = max(population, key=lambda x: calculate_fitness(x, sample))
        best_fitness = calculate_fitness(best_genotype, sample)
        
        aveg+= best_fitness
        best = min(best, best_fitness)
        print("Average:", aveg/runs, "Best Fitness:", best)

# Run evolutionary algorithm
evolutionary_algorithm()

