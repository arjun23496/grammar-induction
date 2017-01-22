from GeneticEvolution import GeneticEvolution		

evolution = GeneticEvolution(terminals=['a','b'],non_terminals=['0','1','3'])

pop = evolution.init_population()
# print evolution.get_random_rules()

with open('corpus/palindrome') as f:
    for line in f:
        <do something with line>