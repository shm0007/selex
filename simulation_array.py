import random
import csv
import concurrent.futures
import time
from energy_matrix import get_energy_matrices
import matplotlib.pyplot as plt
import sys
argv = sys.argv



# Constants
GENOTYPE_LENGTH = 20
POPULATION_SIZE = 50
MAX_ROUNDS = 60
MUTATION_RATE = 0.0001
NUM_RUNS = 100
NEIGHBOR_EFFECT = 2 # 0 - no neigbor effect, 1- nearest neighbor effect, 2- two nearest neighbot effect

#gene_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
gene_to_index = [0] * 128
gene_to_index[ord('A')] = 0
gene_to_index[ord('G')] = 1
gene_to_index[ord('C')] = 2
gene_to_index[ord('U')] = 3
gene_to_index[1] = 1
gene_to_index[2] = 2
gene_to_index[3] = 3


# Total Number of nucleotide states (A,C,G,U)
num_states = 4  

# standard deviations for normal distribution, sigma1 is for first neighbor, sigma2 is for second neighbor
sigma1 = 0.1
sigma2 = 0.01


# energy matrix for first neighbor and second neighbor effect
energy_mat_1st, energy_mat_2nd =  get_energy_matrices(num_states,sigma1,sigma2)


# Function to find direct interaction effect of s and s*.  
def direct_interaction_effect(s, s_star):
        count = 0
        for i in range (len(s)):
            if s[i] != s_star[i]: 
                count+=1 # Kronecker delta function implementation according to equation 9
        return count
        #return np.sum(1 - np.equal(s, s_star))

# Function to calculate right neighbor effect of s and s*. 
def right_neighbor_effect(s, s_star):
    effect = 0
    for i in range(GENOTYPE_LENGTH):
        if i< GENOTYPE_LENGTH-1 and NEIGHBOR_EFFECT !=0 : # Nearest Neighbor effect
            effect += energy_mat_1st[s_star[i]][s[i]][s_star[i+1]] 
            effect -= energy_mat_1st[s[i]][s_star[i]][ s[i+1]]
        if i < GENOTYPE_LENGTH-2 and NEIGHBOR_EFFECT == 2: # Second Neighbor effect
            effect += energy_mat_2nd[s_star[i]][s[i]][ s_star[i+2]]
            effect -= energy_mat_2nd[s[i]][s_star[i]][s[i+2]]
    return effect

# Function to calculate left neighbor effect of s and s*. 
def left_neighbor_effect(s, s_star):
    effect = 0
    for i in range(GENOTYPE_LENGTH):
        if i-1 >= 0 and NEIGHBOR_EFFECT != 0: # Nearest Neighbor effect
            effect += energy_mat_1st[s_star[i]][s[i]][s_star[i-1]]
            effect -= energy_mat_1st[s[i]][s_star[i]][ s[i-1]]
        if i -2 >=0 and NEIGHBOR_EFFECT == 2: # Second Nearest Neighbor effect
            effect += energy_mat_2nd[s_star[i]][s[i]][ s_star[i-2]]
            effect -= energy_mat_2nd[s[i]][s_star[i]][s[i-2]]

    return effect



# Fitness function according to Equation 10
def calculate_fitness(s, s_star):
    direct_effect = direct_interaction_effect(s,s_star)
    right_effect = right_neighbor_effect(s,s_star)
    left_effect = left_neighbor_effect(s,s_star)
    fitness = direct_effect + right_effect + left_effect
    return fitness


# Takes a string as input and returns numpy array of genotype
# Example: string_to_genotype("ACGU") -> [0,1,2,3]
def string_to_genotype(genome_string):
    genome_list = [gene_to_index[ord(char)] for char in genome_string]
    return genome_list

# Generate a random genotype of length GENOTYPE_LENGTH
def generate_genotype():
    genome_list =  [gene_to_index[random.randint(0,3)] for _ in range(GENOTYPE_LENGTH)]
    return genome_list

# Selection function. It takes a population and a target, It loops through GENOTYPE_LENGTH times
# and picks the fittest between 2 random genotype from the current population and select them for next generation.
# It also returns the average fitness of the selected population along with the population
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

# Mutation function. It takes a single genotype and mutates the data based of MUTATION_RATE value 
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
    return mutated_genotype

# Evolutionary algorithm. It takes a target string as input.
def evolutionary_algorithm(target_string):

    print("Evolutionary algorithm for target : ",target_string)
    target  = string_to_genotype(target_string)
    # These two MAX_ROUNDS* NUM_RUNS array stores best and average fitness after each round for each run.
    best_fitnesses = [[] for _ in range(MAX_ROUNDS)]
    average_fitnesses = [[] for _ in range(MAX_ROUNDS)]

    start_time = int(time.time()) #timestamp to calculate total time, and to provide unique name for the file
    for i in range(NUM_RUNS):
        
        if(i%10 == 0):
            print(f'Running run {i+1}')
        
        population = [generate_genotype() for _ in range(POPULATION_SIZE)] # Generate Random population
        best = 100000 
        for round in range(MAX_ROUNDS):
            
            population,average = selection(population, target) 
            population = [mutate(genotype) for genotype in population]
            best_genotype = min(population, key=lambda x: calculate_fitness(x, target))

            best_fitness = calculate_fitness(best_genotype, target)
            best = min(best, best_fitness)

            best_fitnesses[round].append(best)
            average_fitnesses[round].append(average)
    
    print('Total Time ' + str(int(time.time()) - start_time) )


    # Plotting the data as two line curve

    # For each genenration, get the average of all the best fitnesses
    line1 = [] 
    for fitnesses in best_fitnesses:
        line1.append(sum(map(float, fitnesses)) / len(fitnesses))

    # For each genenration, get the average of all the average fitnesses across all the runs
    line2 = []
    for fitnesses in average_fitnesses:
        line2.append(sum(map(float, fitnesses)) / len(fitnesses))

    x_values =  [i+1 for i in range(MAX_ROUNDS)]    
    plt.plot( x_values,line1, label = 'Best '+ target_string)
    plt.plot( x_values,line2, label = 'Average ' + target_string)
    




if len(argv) != 5: # not enough arguments
    print("ERROR!!! Not Enough Arguments")
    print("Usage: Python simupation.py population generation total_run neighbor_effect")
    sys.exit(1)

POPULATION_SIZE = int(argv[1])
MAX_ROUNDS = int(argv[2])
NUM_RUNS = int(argv[3])
NEIGHBOR_EFFECT = int(argv[4])


evolutionary_algorithm('AAAAAAAAAAAAAAAAAAAA')
evolutionary_algorithm('GGGGGGGGGGGGGGGGGGGG')
evolutionary_algorithm('CCCCCCCCCCCCCCCCCCCC')
evolutionary_algorithm('UUUUUUUUUUUUUUUUUUUU')
evolutionary_algorithm('AGCUAGCUAGCUAGCUAGCU')
evolutionary_algorithm('CGUGCGGGGAUCGCAUGCUA')
evolutionary_algorithm('UGCUAGAAAGCAUGCGGGGA')


effect_text = [" No Neighbor Effect", " Nearest Neighbor Effect", " Second Neighbor effect"]
plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.title('Best and Average for' + effect_text[NEIGHBOR_EFFECT])
plt.grid(True)
plt.legend()
plt.show()
