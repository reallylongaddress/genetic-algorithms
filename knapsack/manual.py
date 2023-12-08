'''
VERY VERY heavily influenced by:

https://github.com/Ishikawa7/Quick-paths-to-start/tree/main/Genetic%20algorithms
https://github.com/kiecodes/genetic-algorithms/tree/master
'''

from random import choices, randint, randrange, random

max_generations = 50
max_mass_g = 3000
mutate_prob = .25
mutates_per_knapsack = 2
fitness_limit = 5000

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

#generat3 an array of [0,1] of size k
def generate_knapsack(num_items):
    return choices([0,1], k=num_items)

#generate a set of knapsacks
def generate_knapsacks(num_knapsacks, num_items_per_knapsack):
    return_value = [generate_knapsack(num_items_per_knapsack) for i in range(1, num_knapsacks+1)]
    return return_value

#fitness function.  return weight if sum items weight < weight_limit, else return 0
def fitness(all_items, knapsack, weight_limit):
    total_mass_g = 0
    total_value = 0
    for i, item in enumerate(all_items):
        if knapsack[i] == 1:
            total_mass_g += item.mass_g
            total_value += item.value
            #mass exceeded, return 0
            if (total_mass_g > weight_limit):
                return 0
    #mass not exceeded, return knapsack value
    return total_value

def select_next_generation(knapsacks, all_items, weight_limit):

    weights = [fitness(all_items, knapsack, weight_limit) for knapsack in knapsacks]
    if sum(weights) == 0:
        next_gen = knapsacks[0:2]
    else:
        next_gen = choices(population=knapsacks,
                           weights=weights,
                           k=2)
    return next_gen

#breed function
def crossover(a, b):
    p = randint(1, len(a)-1)
    ab = a[0:p] + b[p:]
    ba = b[0:p] + a[p:]
    return ab, ba

#mutate function, flip each bit based on a prob(ability)
def mutate(knapsack, num, prob):

    #how many potential mutations per knapsack
    for _ in range (num):
        #generate a random [0,1] to see if a mutation exists
        rand = random()
        if prob > rand:
            index = randrange(len(knapsack))
            knapsack[index] = abs(knapsack[index] - 1)
    return knapsack

#test set 1
first_example = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
]
#test set 2
second_example = [
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70)
] + first_example

def run_evolution(fitness_limit, max_generations):

    #generate a random initial population
    population = generate_knapsacks(15, len(thing_set))
    for i in range(max_generations):

        #sort based on fitness function (knapsack value if mass < max_mass_g)
        population_sorted = sorted(population,
                                   key=lambda x:fitness(thing_set, x, max_mass_g),
                                   reverse=True)

        best_knapsack = population_sorted[0]
        best_fitness = fitness(thing_set, population_sorted[0], max_mass_g)
        if best_fitness >= fitness_limit:
            best_knapsack = population_sorted[0]
            break

        #'parents' = the best 2 from the previous gneration
        next_generation = population_sorted[0:2]

        #'breed' children for the next generation an thorw in a few (potential) mutations
        for i in range(int(len(population)/2 - 1)):

            #select 2 parents
            parent_a, parent_b = select_next_generation(population, thing_set, max_mass_g)

            #breed
            child_a, child_b = crossover(parent_a, parent_b)

            #mutate
            child_a = mutate(child_a, mutates_per_knapsack, mutate_prob)
            child_b = mutate(child_b, mutates_per_knapsack, mutate_prob)

            next_generation += [child_a, child_b]

        population = next_generation

        population_sorted = sorted(population,
                                    key=lambda x:fitness(thing_set, x, max_mass_g),
                                    reverse=True)

    #figure out what items are in our 'best_knapsack'
    best_items = ([i for i in [tf and item for tf, item in zip(list(map(bool,best_knapsack)), thing_set)] if i != False])
    #display items in the best_knapsack
    best_item_names = ''
    sum_mass = 0
    for best_item in best_items:
        best_item_names = (f'{best_item_names} {best_item.name}')
        sum_mass += best_item.mass_g
    print(f'best_items_names: {best_item_names}')
    print(f'best_items_mass: {fitness(thing_set, best_knapsack, max_mass_g)}')
    print(f'best_items_value: {sum_mass}')

#run the program
thing_set = second_example
run_evolution(fitness_limit, max_generations)
