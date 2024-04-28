import numpy as np

def get_energy_matrices(num_states,sigma1, sigma2):
    
    matrix1 = [[[0] * num_states for _ in range(num_states)] for _ in range(num_states)]
    matrix2 = [[[0] * num_states for _ in range(num_states)] for _ in range(num_states)]

    for s_star_i in range(num_states):
        for s_i in range(num_states):
            for s_star_neighbor in range(num_states):

                # Generate random value from Gaussian distribution
                energy1 = np.random.normal(0, sigma1)
                energy2 = np.random.normal(0, sigma2)
                
                
                if s_i == s_star_i: # For same character, energy is zero according to paper
                    energy1,energy2 = 0,0

                # Store energy value in the energy matrix
                matrix1[s_star_i][ s_i][s_star_neighbor] = energy1
                matrix2[s_star_i][ s_i][ s_star_neighbor]  = energy2

    return matrix1,matrix2