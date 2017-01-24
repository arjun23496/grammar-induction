from __future__ import division

import nltk
import warnings
import sys
import json_conv

from time import sleep
from tqdm import tqdm
from tqdm import trange
from GeneticEvolution import GeneticEvolution		

reload(sys)  
sys.setdefaultencoding('utf8')

def check_grammar(grammar, corpus, mapping):
	grammar_string = ''
	for x in range(0,len(grammar)):
		if x%3 == 0:
			if x!=0:
				grammar_string = grammar_string+"\n"
			grammar_string = grammar_string+grammar[x]+" ->"
		else:
			if not grammar[x].isdigit():
				grammar_string = grammar_string+" '"+grammar[x]+"'"
			else:
				grammar_string = grammar_string+" "+grammar[x]

	conv_tags = nltk.tokenize.casual.casual_tokenize(corpus)

	accept = False

	try:
		grammar_handle = nltk.CFG.fromstring(grammar_string)
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			parser = nltk.ShiftReduceParser(grammar_handle)
		tree = parser.parse(conv_tags)
		for y in tree:
			accept = True
	except ValueError:
		accept = False
	# except AttributeError:
	# 	accept = False
	# except Exception:
	# 	accept = True

	return accept

def convert_corpus(corpus, mapping, filepath):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sentence = sent_detector.tokenize(corpus)

	n_sentences = len(sentence)
	file_handle = open(filepath,'w')

	for x in sentence:
		text = nltk.word_tokenize(x)
		tagged_text = nltk.pos_tag(text)
		pos_tags = [pos for (token,pos) in nltk.pos_tag(text)]
		conv_tags = []
		# except Exception as e:
		# 	print "Issue in tokenization"
		# 	return False

		for x in pos_tags:
			f = False
			for y in mapping:
				if x in mapping[y]:
					conv_tags.append(y)
					f=True
					break
			if not f:
				conv_tags.append('O')
		conv_tags = ' '.join(conv_tags)
		conv_tags = conv_tags+"\n"
		file_handle.write(conv_tags)
	file_handle.close()

	print n_sentences," written"
	return n_sentences

# Terminals are
# N: nouns, pronouns (NN, NNP, NNPS, NNS, PRP, WP)
# V: verbs, helping verbs (MD, VB, VBD, VBG, VBN, VBP, VBZ)
# J: adjectives, numeral, possessives (CD, JJ, JJR, JJS, PRP$, WP$)
# R: adverbs (RB, RBR, RBS, WRB)
# P: prepositions, particles (IN, RP, TO)
# T: conjunctions, determiners (CC, DT, EX, PDT, WDT)
# O: other (foreign words, symbols, and interjections) (FW, SYM, UH)

evolution = GeneticEvolution(terminals=['N','V'])


mapping = {
	'N': ['NN', 'NNP', 'NNPS', 'NNS', 'PRP', 'WP'],
	'V': ['MD', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
	'J': ['CD', 'JJ', 'JJR', 'JJS', 'PRP$', 'WP$'],
	'R': ['RB', 'RBR', 'RBS', 'WRB'],
	'P': ['IN', 'RP', 'TO'],
	'T': ['CC', 'DT', 'EX', 'PDT', 'WDT'] # Assign rest to O
}

# pop = evolution.init_population()

pop = evolution.init_population_from_file("output_pop")

print pop

generation = 22
# n_lines_alice = 1091
# n_lines_random = 246
n_lines_alice = 30
n_lines_random = 29
corpus = ''

# with open('corpus/alice_in_wonderland') as f :
# 	for f in tqdm(f):
# 		corpus = corpus+f
# convert_corpus(corpus, mapping, "corpus/pre_alice")

# with open('corpus/random') as f :
# 	for f in tqdm(f):
# 		corpus = corpus+f
# convert_corpus(corpus, mapping, "corpus/pre_random")

# pop = [{"chromosome": u'0044001RT6TP11R4R26NP2304743VN27N7TP3P820J787', "fitness": 0.0}]
# pop = [{'chromosome': u'0048V642P3V63RO28V4NP6323734NN6V362R4JR66P7JV4RV4PR703', 'fitness': 0}, {'chromosome': u'1N74N887R8V077J87088707O7V22OR0PV28602262T0PV6PJ0PJ6T10R6', 'fitness': 0}, {'chromosome': u'1N74O78R606T7V186137T24364J1N46ON61J6VJ600', 'fitness': 0}, {'chromosome': u'1N77N41874NN03P2JV46607T3PO4483VJ2773NJ2868183RR68P', 'fitness': 0}, {'chromosome': u'2N70VP2323R738172382V22R88170807676400R41260V43862T4836P46J06O31876OO', 'fitness': 0}, {'chromosome': u'60J34N3808840JP0V70T24N401420473610T2V672O', 'fitness': 0}, {'chromosome': u'1N724146J4V24010PR4R60874877N06228P24337JO67N', 'fitness': 141}, {'chromosome': u'1N70171RN0OO74700147481R3272OP84V263', 'fitness': 0}, {'chromosome': u'60J2N33T846R41038301N8R61V80J1877', 'fitness': 0}, {'chromosome': u'1N78T28PO1O60667T608V73J78O6RO32V20171J684', 'fitness': 0}]

while True:
	print "\nGeneration"
	print generation

	generation = generation+1

	# print check_grammar("0TN0TJ0NV0NJ0PN0PV0PJ0RJ0VJ0RS0NS0PS0TS0JS0VS0SV0SJ0SN0OO","my but at any rate it would not open any of them. However, on the second", mapping)
	max_corpus = 0
	max_rand = 0
	i_max = 0

	for x in trange(len(pop)):
		grammar = pop[x]['chromosome']
		n_corpus = 0
		n_random = 0
		
		with open('corpus/palindrome') as f :
		    for f in tqdm(f):
		    	if check_grammar(grammar, f, mapping):
			    	n_corpus=n_corpus+1

		with open('corpus/palin_rand') as f :
		    for f in tqdm(f):
		    	if check_grammar(grammar, f, mapping):
					n_random=n_random+1

		if n_corpus > max_corpus:
			max_corpus = n_corpus
			max_rand = n_random
			i_max = x 

		pop[x]['fitness'] = evolution.get_fitness(pop[x]['chromosome'], n_corpus, n_random)
		# print "\n\n\n\n----------------------Debug------------------------"
		# print n_corpus
		# print n_random
		# print pop[x]['fitness']

	print "-----------------Generation Summary------------------------"
	print "Maximum Corpus"
	print max_corpus
	print i_max
	metrics = max_corpus*100/n_lines_alice
	print "% positive parsed: ",metrics,"%"
	metrics = max_rand*100/n_lines_random
	print "% negative parsed: ",metrics,"%"
	print pop
	json_conv.json_convert(pop, 'output_pop')

	if max_corpus == n_lines_alice:
		print "grammar found"
		break

	# break

	pop = evolution.get_next_generation()
	# print pop