import numpy as np

def string_to_list(genome_string):

    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'U': 3}
    
    genome_list = [char_to_index[char] for char in genome_string]
    
    return np.array(genome_list)

A = string_to_list("ACGUG")
B = string_to_list("ACGUA")
print(np.sum( 1- np.equal(A,B)))
