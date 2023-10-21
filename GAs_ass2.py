import random as rn
import matplotlib.pyplot as plt


input_file_path = "input-2.txt"
population = []
number_of_population = 100
number_of_generation = 10
all_input_file = []
fitness_array = []
roulette = []

def generate_population(degree):
    population.clear()
    for i in range(number_of_population):
        chromosome = []
        for j in range(degree + 1):
            chromosome.append(round(rn.uniform(-10, 10), 2))
        population.append(chromosome)

def read_file():
    listFile = []
    file = open(input_file_path, "r")
    for row in file:
        line = row.strip("\n")
        listFile.append(line.split())
    file.close()
    return listFile

all_input_file = read_file()

def get_cost(row_pop, row_file, degree):
    Y_calc = 0
    X = float(all_input_file[row_file][0])
    for i in range(1, degree + 1):
        Y_calc += ((population[row_pop][i]) * pow(X, i))
    Y_calc += population[row_pop][0]
    Y_actual = float(all_input_file[row_file][1])
    return pow((Y_calc - Y_actual), 2)


def get_fitness(row_pop, degree, number_of_point):
    cost = 0.0
    for i in range(number_of_point):
        cost += get_cost(row_pop, i, degree)
    return cost / number_of_point

def fill_fitness_array(degree, number_of_point):
    fitness_array.clear()
    for i in range(number_of_population):
        fitness_array.append(get_fitness(i, degree, number_of_point))

def selection(degree, number_of_point):
    roulette.clear()
    fill_fitness_array(degree, number_of_point)
    MaxNumber = max(fitness_array) * 2
    NewFitnessArray = [MaxNumber - x for x in fitness_array]
    Total = 0
    for x in NewFitnessArray:
        Total += x
    for i in range(number_of_population):
        if i == 0:
            roulette.append(NewFitnessArray[i] / Total)
        else:
            roulette.append(NewFitnessArray[i] / Total + roulette[i - 1])
    R = rn.uniform(0, 1)
    for i in range(number_of_population):
        if R <= roulette[i]: return i
    else:
        return -1

def cross_over(indx1, indx2, degree):
    R = rn.uniform(0, 1)
    if R < 0.07:
        R2 = rn.randint(0, degree)
        for i in range(R2, degree):
            population[indx1][i], population[indx2][i] = population[indx2][i], population[indx1][i]

def mutation(poprow, degree, t, T):
    LB = -10
    UB = 10

    for i in range(degree + 1):
        Dl = population[poprow][i] - LB
        DU = UB - population[poprow][i]
        R1 = rn.uniform(0, 1)
        if R1 <= 0.5:
            y = Dl
        else:
            y = DU
        r = rn.uniform(0, 1)
        b = rn.randint(1, 5)
        Delta = y * (1 - pow(r, ((1 - t) / T) ** b))
        if y == Dl:
            population[poprow][i] = population[poprow][i] - Delta
        else:
            population[poprow][i] = Delta - population[poprow][i]

def get_points(n):
    X = []
    Y = []
    X.clear()
    Y.clear()
    for i in range(n):
        X.append(float(all_input_file[i][0]))
        Y.append(float(all_input_file[i][1]))
    return X, Y

def calc_new_y(x, coeff):
    Y = []
    Y.clear()
    for j in range(len(x)):
        Y_calc = 0
        for i in range(1, len(coeff)):
            Y_calc += (coeff[i] * pow(x[j], i))
        Y_calc += coeff[0]
        Y.append(Y_calc)
    return Y

def main():
    global index_of_min

    number_of_data_set = int(all_input_file[0][0])
    all_input_file.remove(all_input_file[0])

    f = open("output.txt", "w")
    X = []
    Y = []
    for case in range(number_of_data_set):
        X.clear()
        Y.clear()
        number_of_point = int(all_input_file[0][0])
        degree = int(all_input_file[0][1])
        all_input_file.remove(all_input_file[0])
        generate_population(degree)

        for index_of_generation in range(number_of_generation):
            parent_1 = selection(degree, number_of_point)
            parent_2 = selection(degree, number_of_point)
            cross_over(parent_1, parent_2, degree)
            mutation(parent_1, degree, index_of_generation, number_of_generation)
            mutation(parent_2, degree, index_of_generation, number_of_generation)
        fill_fitness_array(degree, number_of_point)
        Min = min(fitness_array)
        for i in range(len(fitness_array)):
            if fitness_array[i] == Min:
                index_of_min = i
                break

        X, Y = get_points(number_of_point)
        predicted_Y = calc_new_y(X, population[index_of_min])
        plt.figure()
        plt.scatter(X, Y, color='red')
        print("\n")
        plt.plot(X, predicted_Y, color='blue')
        f.write("\nCase: ")
        f.write(str(case + 1))
        f.write("\n" + str(population[index_of_min]))

        print("Case: ", case + 1, population[index_of_min])
        all_input_file[:number_of_point] = []
        fitness_array.clear()
        plt.show()

print("start ...")
main()
print("end ...")