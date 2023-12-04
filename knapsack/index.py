from random import choices, randint, randrange, random

max_generations = 50
max_mass_g = 3000
mutate_prob = .25
mutates_per_knapsack = 2
fitness_limit = 1310

class Thing:
    def __init__(self, name, value, mass_g):
        self.name = name
        self.value = value
        self.mass_g = mass_g

    def __str__(self):
        return f'\nname: {self.name}\nvalue: {self.value}\nmass_g: {self.mass_g}\n--------\n'

    def __repr__(self):
        return str(self)

def print_things(things):
    for thing in things:
        print(f'{thing.name}::{thing.value}::{thing.mass_g}')

def generate_knapsack(num_items):
    return choices([0,1], k=num_items)

def generate_knapsacks(num_knapsacks, num_items_per_knapsack):
    return_value = [generate_knapsack(num_items_per_knapsack) for i in range(1, num_knapsacks+1)]
    return return_value

def fitness(all_items, knapsack, weight_limit):
    # print(f'fitness: {knapsack}')
    total_mass_g = 0
    total_value = 0
    for i, item in enumerate(all_items):
        # print(f'{i}::{item}')
        if knapsack[i] == 1:
            total_mass_g += item.mass_g
            total_value += item.value
            # print(f'total_mass_g: {total_mass_g}')
            if (total_mass_g > weight_limit):
                # print('EXCEEDED')
                return 0
    # return total_mass_g
    print(f'fitness mass/value: {total_mass_g}/{total_value}')
    return total_value

def select_next_generation(knapsacks, all_items, weight_limit):

    weights = [fitness(all_items, knapsack, weight_limit) for knapsack in knapsacks]
    if sum(weights) == 0:
        print('-------------ALL WEIGHTS 0')
        next_gen = knapsacks[0:2]
    else:

        next_gen = choices(population=knapsacks,
                        weights=weights,
                        k=2)
    # print(f'next_gen: {next_gen}')

    return next_gen

def crossover(a, b):
    p = randint(1, len(a)-1)
    # print(f'p: {p}')
    ab = a[0:p] + b[p:]
    ba = b[0:p] + a[p:]

    # print(f'a: {a}')
    # print(f'b: {b}')
    # print(f'ab: {ab}')
    # print(f'ba: {ba}')
    return ab, ba

def mutate(knapsack, num, prob):

    #how many potential mutations per knapsack
    for _ in range (num):

        #generate a random [0,1] to see if a mutation exists
        rand = random()
        if prob > rand:
            index = randrange(len(knapsack))
            # print(f'index: {index}, {prob}>{rand}')
            # print(f'0:: {knapsack}')
            knapsack[index] = abs(knapsack[index] - 1)
            # print(f'1:: {knapsack}')
    return knapsack

#item/value/mass_g
# first_example = [
#     Thing('Laptop', 500, 1200),
#     Thing('Headphones', 150, 160),
#     Thing('Coffee Mug', 60, 350),
#     Thing('Notepad', 40, 333),
#     Thing('Water Bottle', 30, 192),
# ]

# second_example = [
#     Thing('Mints', 5, 25),
#     Thing('Socks', 10, 38),
#     Thing('Tissues', 15, 80),
#     Thing('Phone', 500, 200),
#     Thing('Baseball Cap', 100, 70)
# ] + first_example


# third_example = [
#     Thing('Thing A', 115, 45),
#     Thing('Thing B', 20, 22),
#     Thing('Thing C', 215, 95),
#     Thing('Thing D', 200, 120),
#     Thing('Thing E', 250, 170),
#     Thing('Thing Aa', 115, 45),
#     Thing('Thing Bb', 90, 22),
#     Thing('Thing Cc', 215, 295),
#     Thing('Thing Dd', 290, 20),
#     Thing('Thing Ee', 1250, 700),
# ] + second_example

first_example = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
]

second_example = [
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70)
] + first_example


def run_evolution(fitness_limit, max_generations):

    population = generate_knapsacks(15, len(thing_set))
    for i in range(max_generations):
        # print(f'--------------------')
        population_sorted = sorted(population,
                                   key=lambda x:fitness(thing_set, x, max_mass_g),
                                   reverse=True)

        best_knapsack = population_sorted[0]
        best_fitness = fitness(thing_set, population_sorted[0], max_mass_g)
        print(f'GENERATION {i} best: {best_fitness} {population_sorted[0]}')
        if best_fitness >= fitness_limit:
            print(f'{best_fitness} >= {fitness_limit}')
            best_knapsack = population_sorted[0]
            break
        # print(f'2 fitness: {fitness(thing_set, population_sorted[1], max_mass_g)}')

        next_generation = population_sorted[0:2]

        for i in range(int(len(population)/2 - 1)):
            parent_a, parent_b = select_next_generation(population, thing_set, max_mass_g)

            child_a, child_b = crossover(parent_a, parent_b)
            child_a = mutate(child_a, mutates_per_knapsack, mutate_prob)
            child_b = mutate(child_b, mutates_per_knapsack, mutate_prob)
            # print(f'child_a fitness: {fitness(thing_set, child_a, max_mass_g)}')
            # print(f'child_b fitness: {fitness(thing_set, child_b, max_mass_g)}')

            next_generation += [child_a, child_b]
            # print(f'{i}, {len(next_generation)}')

        population = next_generation
        # print(f'population: {len(population)}')


        population_sorted = sorted(population,
                                    key=lambda x:fitness(thing_set, x, max_mass_g),
                                    reverse=True)

    print(f'BEST: {fitness(thing_set, best_knapsack, max_mass_g)}, {best_knapsack}')
    print(f'>>{best_knapsack}<<')
        # if best_fitness >= fitness

        # knapsack_fitness = fitness(thing_set, population, max_mass_g)
        # print(f'run_evolution a/b: {a}/{b}')
        # next_population = generate_knapsacks(8, len(thing_set))
        # # print(f'A run_evolution next_population: {next_population}')
        # next_population.extend([a, b])
        # print(f'B run_evolution next_population: {next_population}')

thing_set = second_example
# thing_set = first_example

# print_things(thing_set)

# knapsack = generate_knapsack(len(thing_set))
# print(knapsack)

# knapsacks = generate_knapsacks(10, len(thing_set))
# print(knapsacks)

# knapsack_fitness = fitness(thing_set, knapsack, max_mass_g)
# print(f'knapsack_fitness: {knapsack_fitness}')

# for knapsack in knapsacks:
#     print(knapsack)
#     print(fitness(thing_set, knapsack, max_mass_g))

# print('-------')
# a, b = select_next_generation(knapsacks, thing_set, max_mass_g)
# print('-------')

# print(f'next a: {a}')
# print(f'next b: {b}')

# print('---crossover----')
# ab, ba = crossover(a, b)
# print(f'ab: {ab}')
# print(f'ba: {ba}')

# ab = mutate(ab, mutates_per_knapsack, mutate_prob)

run_evolution(fitness_limit, max_generations)
