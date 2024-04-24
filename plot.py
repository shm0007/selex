import csv
import matplotlib.pyplot as plt

def read_csv(filename):
    data = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) ==0:
                break 
            average = sum(map(float, row)) / len(row)
            data.append(average)
    return data
def plot_line_graph(x_values, y_values,label):
    plt.plot(x_values, y_values,label = label)

y_values =  [i+1 for i in range(60)]
x_best = read_csv('best_csv_10000_1713922913.csv')
x_avg = read_csv('average_csv_10000_1713922913.csv')
print(x_avg)
print(x_best)
plot_line_graph(y_values, x_best, 'Best')
plot_line_graph(y_values, x_avg,'Avg')

plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.title('Best and Average for UGCUAGAAAGCAUGCGGGGA')
plt.grid(True)
plt.legend()
plt.show()