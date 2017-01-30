from sets import Set

import nltk
import sys
import collections
from tqdm import tqdm

reload(sys)  
sys.setdefaultencoding('utf8')

text_set = []
tokens = Set([])

with open('corpus/alice_in_wonderland') as f:
	for x in tqdm(f):
		l = nltk.word_tokenize(x)
		if len(l)>0:
			# print l[0]
			text_set=text_set+l
			for y in l:
				tokens.add(y)

ttr = len(text_set)/len(tokens)
print "ttr: ",ttr
term_freq = collections.Counter(text_set)
freq_list = []
for x in term_freq:
	freq_list.append(term_freq[x])
fof = collections.Counter(freq_list)
print "frequency of frequency: ",fof
print "------------Heaps law-----------"
print "total number of tokens in collection: ",len(text_set)
print "vocabulary size: ",len(tokens)
heaps_constant = len(tokens)/(len(text_set)**(0.49))
print "constant: ",heaps_constant