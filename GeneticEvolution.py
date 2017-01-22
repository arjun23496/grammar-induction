from operator import attrgetter
from sets import Set

import numpy as np
import random

# Terminals are
# N: nouns, pronouns (NN, NNP, NNPS, NNS, PRP, WP)
# V: verbs, helping verbs (MD, VB, VBD, VBG, VBN, VBP, VBZ)
# J: adjectives, numeral, possessives (CD, JJ, JJR, JJS, PRP$, WP$)
# R: adverbs (RB, RBR, RBS, WRB)
# P: prepositions, particles (IN, RP, TO)
# T: conjunctions, determiners (CC, DT, EX, PDT, WDT)
# O: other (foreign words, symbols, and interjections) (FW, SYM, UH)

#Non Terminals are numbers

class GeneticEvolution:
	def __init__(self, terminals=['N','V','J','R','P','T','O'], non_terminals=['0','1','2','3','4','6','7','8']):
		self.terminals = terminals
		self.non_terminals = non_terminals
		self.population = []
		self.initial_len = 30
		self.population_limit = 10
		self.mutation_prob = 0.01
		self.generation = 0

		#evolution coefficients available for tuning
		self.discount_factor = 0.98 #To avoid generation of large grammars
		self.penalty_random = 2 #Penalty for accepting random grammar


	def get_random_rules(self, min_length=10):
		used_term = Set([])
		non_used_term = Set([])

		complete_pool = self.terminals+self.non_terminals

		grammar = ''
		ctr = 0

		while ctr<min_length or len(non_used_term) > 0 :
			if len(non_used_term) == 0:
				gen = random.choice(self.non_terminals)
			else:
				gen = non_used_term.pop()
			used_term.add(gen)
			grammar = grammar+gen
			el1 = random.choice(complete_pool)
			el2 = random.choice(complete_pool)

			if el1 in self.non_terminals and el1 not in used_term:
				non_used_term.add(el1)

			if el2 in self.non_terminals and el2 not in used_term:
				non_used_term.add(el2)

			grammar = grammar+el1+el2
			ctr = ctr+3

		return grammar


	def init_population(self, population_limit=10):
		complete_pool = self.terminals+self.non_terminals
		random.shuffle(complete_pool)
		for x in range(0,population_limit):
			chromosome = ''
			# for y in range(0,self.initial_len):
			# 	if y%3 == 0:
			# 		chromosome = chromosome+random.choice(self.non_terminals)
			# 	else:
			# 		chromosome = chromosome+random.choice(complete_pool)
			chromosome = self.get_random_rules()
			self.population.append({ 'chromosome': chromosome, 'fitness': 0.0})
			
		print self.population


#Use this function to get the fitness coefficent
	def get_fitness(self,pop,corpus,r_corpus):
		p = 7
		discount = self.discount_factor^(max(0,len(pop)-p))
		fitness = discount*corpus - (self.penalty_random*r_corpus)
		return fitness


	def get_next_generation(self):
		self.generation = self.generation+1
		new_gen=[]
		temp_pop = sorted(self.population, key=lambda y: y['fitness'], reverse=True)

		new_gen.append(self.population[0])

		#Crossover
		print "starting crossover"		
		cross_prob = 0.3

		for x in range(1,6):
			val = self.population[x]['chromosome']
			for y in range(0,len(val),3):
				prob = np.random.rand()
				if prob < cross_prob:
					val = val[0:y]+self.population[0]['chromosome'][y:3]+val[y+3:]
			new_gen.append({'chromosome': val, 'fitness': 0.0})

		print "crossover complete"
		# print len(new_gen)

		#Mutation
		print "Mutation starting"
		
		complete_pool = self.terminals+self.non_terminals

		for x in range(6,10):
			val = self.population[x]['chromosome']
			chromosome = ''

			for y in range(0,len(val)):
				prob = np.random.rand()
				if prob < self.mutation_prob: 
					if y%3 == 0:
						chromosome = chromosome+random.choice(self.non_terminals)
					else:
						chromosome = chromosome+random.choice(complete_pool)
				else:
					chromosome = chromosome+val[y]
			new_gen.append({'chromosome': chromosome, 'fitness': 0.0})

		print "mutation complete"
		# print len(new_gen)

		self.population = new_gen

		np.random.shuffle(self.population)

		return self.population
