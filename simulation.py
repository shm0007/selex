import random
import numpy as np
from fitness import calculate_fitness, string_to_list
import csv
# Constants
ALPHABET = ['A', 'G', 'C', 'U']
GENOTYPE_LENGTH = 20
POPULATION_SIZE = 10000
MAX_ROUNDS = 60
MUTATION_RATE = 0.0001
NUM_RUNS = 100

aveg = 0
best = 10000
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
        selected = min(contenders, key=lambda x: calculate_fitness(x, sample))
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
    sample = string_to_list('UGCUAGAAAGCAUGCGGGGA')
    result_avg = [[] for _ in range(61)]
    avg_avg = [[] for _ in range(61)]
    for i in range(NUM_RUNS):
        print(f'Running run {i+1}')
        population = [generate_genotype() for _ in range(POPULATION_SIZE)]
        runs = 0
        aveg = 0
        best = 10000
        for _ in range(MAX_ROUNDS):
            runs+=1
            population = selection(population, sample)
            population = [mutate(genotype) for genotype in population]
            best_genotype = min(population, key=lambda x: calculate_fitness(x, sample))
            best_fitness = calculate_fitness(best_genotype, sample)
        
            aveg+= best_fitness
            best = min(best, best_fitness)
            result_avg[runs-1].append(best)
            avg_avg[runs-1].append(aveg/runs)
            #print("Round: ", runs, "Average:", aveg/runs, "Best Fitness:", best)
    with open( 'best_csv.csv', "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result_avg)
    with open( 'avg_csv.csv', "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(avg_avg)
    


# Run evolutionary algorithm
evolutionary_algorithm()


