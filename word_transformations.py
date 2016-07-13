#!/usr/bin/env python
import os, sys, re

import nltk
from nltk.corpus import wordnet
from nltk.corpus import cmudict

from random import Random

global rhymes, random, rhymelevel, antonyms, synonyms, hypernyms, hyponyms

random=Random()

antonyms={}
synonyms={}
hypernyms={}
hyponyms={}
rhymes={}
rhymelevel=2


# from http://kashthealien.wordpress.com/2013/06/15/213/
def rhyme(inp, level):
	entries=cmudict.entries()
	syllables = [(word, syl) for word, syl in entries if word == inp]
	myRhymes = []
	for (word, syllable) in syllables:
		myRhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
	return list(set(myRhymes))

def randomRhyme(w):
	global rhymes, random, rhymelevel
	if not (w in rhymes):
		rhymes[w]=rhyme(w, rhymelevel)
		rhymes[w].append(w)
	if len(rhymes[w])==0: return w
	return random.choice(rhymes[w])

def randomAnt(w):
	global random, antonyms
	if not (w in antonyms):
		ret=[]
		for syn in wordnet.synsets(w):
			for l in syn.lemmas():
				if l.antonyms():
					ret.append(l.antonyms()[0].name())
		ret.append(w)
		antonyms[w]=list(set(ret))
	if len(antonyms[w])==0: return w
	return random.choice(antonyms[w])

def randomSyn(w):
	global random, synonyms
	if not (w in synonyms):
		ret=[]
		for syn in wordnet.synsets(w):
			for l in syn.lemmas():
				ret.append(l.name())
		ret.append(w)
		synonyms[w]=list(set(ret))
	if len(synonyms[w])==0: return w
	return random.choice(synonyms[w])

def randomHyper(w):
	global random, hypernyms
	if not (w in hypernyms):
		ret=[]
		for syn in wordnet.synsets(w):
			for l in syn.lemmas():
				if l.hypernyms():
					ret.append(l.hypernyms()[0].name())
		ret.append(w)
		hypernyms[w]=list(set(ret))
	if len(hypernyms[w])==0: return w
	return random.choice(hypernyms[w])

def randomHypo(w):
	global random, hyponyms
	if not (w in hyponyms):
		ret=[]
		for syn in wordnet.synsets(w):
			for l in syn.lemmas():
				if l.hyponyms():
					ret.append(l.hyponyms()[0].name())
		ret.append(w)
		hyponyms[w]=list(set(ret))
	if len(hyponyms[w])==0: return w
	return random.choice(hyponyms[w])

def main():
	def printHelp(w):
		print("Usage: "+sys.argv[0]+" mode\nwhere mode is one of rhyme|syn|ant|hyper|hypo")
		sys.exit(1)
	if(len(sys.argv)<2): printHelp("")
	mode=sys.argv[1]
	fn=printHelp
	if(mode=="rhyme"): fn=randomRhyme
	elif(mode=="syn"): fn=randomSyn
	elif(mode=="ant"): fn=randomAnt
	elif(mode=="hyper"): fn=randomHyper
	elif(mode=="hypo"): fn=randomHypo
	for line in sys.stdin.readlines():
		for word in re.split(r'([A-Za-z0-9]+|[^A-Za-z0-9]+)', line):
			sys.stdout.write(fn(word))
			sys.stdout.flush()
	
if __name__=="__main__": main()