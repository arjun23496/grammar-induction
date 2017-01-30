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
			if not grammar[x].isdigit() and grammar[x]!=' ':
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

pop = evolution.init_population()

# pop = evolution.init_population_from_file("output_pop")

print pop

generation = 375
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
# pop = [{'chromosome': u'80N01V1NV0620N21180V13V278638N0V600V238602', 'fitness': 1.972298482472312}, {'chromosome': u'80N64433068V0NN421147241016243710', 'fitness': 0.0}, {'chromosome': u'80N4784062676220206NN6407NV608', 'fitness': 0.0}, {'chromosome': u'80N07378443V174411010307381', 'fitness': 0.0}, {'chromosome': u'80N1V32V037236N74801848078834748177866V', 'fitness': 0.0}, {'chromosome': u'80N17403N4N868N33301V767071433', 'fitness': 0.0}, {'chromosome': u'84404V2002031221782414463624V64248778410VV70844V8388121803461V71V60038763VV77076736833831841386V6444023V67404V734N16073382N7NN12432408821741671263732707744634838226684471820023V8N03074736131N73034164374V46028084NN7736N2280603230812128636078178', 'fitness': -3.9653113195997314}, {'chromosome': u'67486623N24V86266407207N74276686086V22372311631V80808N08728174706N1040V03604060NN6441N33822168082783840142243844126840V20447673V28766NN2143341072770400V210117273212436043834N13867188V42138478208110123N806608278', 'fitness': 0.0}, {'chromosome': u'2V743V3V707N82242718N8N14262VN26640873404122N32402N68882V3622266681602NN06063483327N0630112610748N31007804624624V203283V41376732782833768881232N40383736067484113707V2686VV1488046310772824V4', 'fitness': 0.1807247948194214}, {'chromosome': u'1N428207221N22336612N6VN8441841002813482N83780023NV6N32160322N881332316N64146886674V84883140V6628V404736801486N6833N34N24712N600V4VN14N8187236627N820813N673876473', 'fitness': 0.044546712249676636}]

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
		# print pop[x]['chromosome']
		# print len(pop[x]['chromosome'])
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

	if max_corpus == n_lines_alice and max_rand == 0:
		print "grammar found"
		break

	# break

	pop = evolution.get_next_generation()
	# print pop