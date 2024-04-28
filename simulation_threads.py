import random
import csv
import concurrent.futures
import time
from energy_matrix import get_energy_matrices
# Constants

#gene_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
gene_to_index = [0] * 128
gene_to_index[ord('A')] = 0
gene_to_index[ord('G')] = 1
gene_to_index[ord('C')] = 2
gene_to_index[ord('U')] = 3
gene_to_index[1] = 1
gene_to_index[2] = 2
gene_to_index[3] = 3



GENOTYPE_LENGTH = 20
POPULATION_SIZE = 500
MAX_ROUNDS = 60
MUTATION_RATE = 0.0001
NUM_RUNS = 100

average = 0
best = 100


# Number of nucleotide states
num_states = 4  

# Define standard deviations for sampling
sigma1 = 0.1
sigma2 = 0.01


# energy matrix for first neighbor
energy_mat_1st, energy_mat_2nd =  get_energy_matrices(num_states,sigma1,sigma2)


#calculating energy matrices


# Define functions to calculate each effect
def direct_interaction_effect(s, s_star):
        count = 0
        for i in range (len(s)):
            if s[i] != s_star[i]:
                count+=1
        return count
        #return np.sum(1 - np.equal(s, s_star))

def right_neighbor_effect(s, s_star):
    effect = 0
    for i in range(GENOTYPE_LENGTH):
        if i< GENOTYPE_LENGTH-1:
            # effect += energy_mat_1st[(s_star[i],s[i], s_star[i+1])]
            # effect -= energy_mat_1st[(s[i],s_star[i], s[i+1])]
            effect += energy_mat_1st[s_star[i]][s[i]][s_star[i+1]]
            effect -= energy_mat_1st[s[i]][s_star[i]][ s[i+1]]
        if i < GENOTYPE_LENGTH-2:
            effect += energy_mat_2nd[s_star[i]][s[i]][ s_star[i+2]]
            effect -= energy_mat_2nd[s[i]][s_star[i]][s[i+2]]
    return effect


def left_neighbor_effect(s, s_star):
    effect = 0
    for i in range(GENOTYPE_LENGTH):
        if i-1 >= 0:
            effect += energy_mat_1st[s_star[i]][s[i]][s_star[i-1]]
            effect -= energy_mat_1st[s[i]][s_star[i]][ s[i-1]]
        if i -2 >=0:
            effect += energy_mat_2nd[s_star[i]][s[i]][ s_star[i-2]]
            effect -= energy_mat_2nd[s[i]][s_star[i]][s[i-2]]

    return effect



# Define fitness calculation function using Equation 10
def calculate_fitness(s, s_star):
    direct_effect = direct_interaction_effect(s,s_star)
    right_effect = right_neighbor_effect(s,s_star)
    left_effect = left_neighbor_effect(s,s_star)
    fitness = direct_effect + right_effect + left_effect
    return fitness


# Takes a string as input and returns numpy array of genotype
# string_to_genotype("ACGU") -> [0,1,2,3]
def string_to_genotype(genome_string):
    genome_list = [gene_to_index[ord(char)] for char in genome_string]
    return (genome_list)

# Generate random genotype
def generate_genotype():
    genome_list =  [gene_to_index[random.randint(0,3)] for _ in range(GENOTYPE_LENGTH)]
    return (genome_list)

# Selection function
def selection(population, sample):
    average = 0
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
    return selected_population, average/len(population)

# Mutation function
def mutate(genotype):
    mutated_genotype = []
    for base in genotype:
        if random.random() < MUTATION_RATE:
            mutated_base = gene_to_index[random.randint(0,3)]
            while mutated_base == base:
                mutated_base = gene_to_index[random.randint(0,3)]
            mutated_genotype.append(mutated_base)
        else:
            mutated_genotype.append(base)
    return (mutated_genotype)

# Evolutionary algorithm
def evolutionary_algorithm(sample):

    runs = 0
    result_avg = [[] for _ in range(61)]
    avg_avg = [[] for _ in range(61)]
    before = int(time.time())
    def run_instance(i):
      
        print(f'Running run {i+1}')
        population = [generate_genotype() for _ in range(POPULATION_SIZE)]
        runs = 0
        best = 10000
        for _ in range(MAX_ROUNDS):
            runs+=1
            population,average = selection(population, sample)
            population = [mutate(genotype) for genotype in population]
            best_genotype = min(population, key=lambda x: calculate_fitness(x, sample))

            best_fitness = calculate_fitness(best_genotype, sample)
        

            best = min(best, best_fitness)
            result_avg[runs-1].append(best)
            
            avg_avg[runs-1].append(average)
        print(f'Finishing run {i+1}')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_instance, range(NUM_RUNS))
    best_name = 'data/best_csv_' + str(POPULATION_SIZE) +"_" +  str(before) + ".csv"
    avg_name = 'data/average_csv_' + str(POPULATION_SIZE) +"_" +  str(before) + ".csv"
    print('Total Time ' + str(int(time.time()) - before) )
    with open( best_name, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(result_avg)
    with open( avg_name, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(avg_avg)
    


# Run evolutionary algorithm
sample = string_to_genotype('UGCUAGAAAGCAUGCGGGGA')
evolutionary_algorithm(sample)

