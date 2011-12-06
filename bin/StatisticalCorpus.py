#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, re, codecs, time
from collections import defaultdict
from ParseXml import ParseXml
from ParseStanfordXml import ParseStanfordXml
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous

class StatisticalCorpus:
	def __init__(self, input_folder, temp_folder, min_word_size, window_size):
		try:
			self.root, self.dirs, self.files = os.walk(input_folder).next()[:3]
		except IOError:
			print bcolors.FAIL+'ERROR: It was not possible to open the '+input_folder+' folder'+bcolors.ENDC
			sys.exit(2)

		self.min_word_size = int(min_word_size)
		self.window_size = int(window_size)
		self.temp_folder = temp_folder
		self.qty_documents = len(self.files)
		self.misc = Miscelaneous()

		os.system('rm '+self.temp_folder+'Statistical_corpus.txt')
		try:
			self.temp_file = codecs.open(self.temp_folder+'Statistical_corpus.txt', 'a', 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the '+self.temp_folder+'Statistical_corpus.txt file'+bcolors.ENDC
			sys.exit(2)

	def buildCorpus_pt(self):
		print 'Building statistical corpus file at '+self.temp_folder+'...'
		i = 0
		for corpus_file in self.files:
			i += 1
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xmlfile = ParseXml(self.root+''+corpus_file)
				dic_terms = xmlfile.getDicTerms()
				dic_nouns = xmlfile.getNouns()
				#dic_verbs = xmlfile.getVerbs()

				id_sentence = 1
				id_word = 1
				id_t = 's'+str(id_sentence)+'_'+str(id_word)

				string_corpus = ''
				while dic_terms.has_key(id_t):
					while dic_terms.has_key(id_t):
						lemma = re.sub('(--|/|,|;|\(|\)|\$|\+|\')', '', dic_terms[id_t]['lemma'])
						lemma = re.sub('-', '_', lemma)
						lemma = re.sub('_$', '', lemma)

						if not re.match('^(pu|num|conj|art|prp|spec)', dic_terms[id_t]['pos']) and (len(lemma) >= self.min_word_size):
							if dic_nouns.has_key(id_t):
								string_corpus += lemma+'__N '
							#elif dic_verbs.has_key(id_t):
							#	string_corpus += lemma+'__V '
							else:
								string_corpus += lemma+'__O '
						id_word += 1
						id_t = 's'+str(id_sentence)+'_'+str(id_word)
					id_word = 1
					id_sentence += 1
					id_t = 's'+str(id_sentence)+'_'+str(id_word)
					#print string_corpus
				#print string_corpus
				self.temp_file.write(string_corpus)
				self.misc.progress_bar(i, self.qty_documents, 100)

		self.temp_file.close()

	def buildCorpus_en(self):
		print 'Building statistical corpus file at '+self.temp_folder+'...'
		i = 0
		for corpus_file in self.files:
			i += 1
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xmlfile = ParseStanfordXml(self.root+''+corpus_file)
				dic_terms = xmlfile.getDicTerms()
				self.__getRelationsInAWindow__(dic_terms, self.window_size)
				self.__progress_bar__(i, self.qty_documents, 100)
		self.temp_file.close()
				
	""" GET RELATIONS IN A WINDOW """
	def __getRelationsInAWindow__(self, dic_terms, window_size):
		i = 0
		id_sentence = 1
		id_word = 1
		id_t = 's'+str(id_sentence)+'_'+str(id_word)
		string_corpus = ''
		while dic_terms.has_key(id_t):
			while dic_terms.has_key(id_t):
				lemma = re.sub('(--|/|,|;|\(|\)|\$|\+|\'|[.])', '', dic_terms[id_t]['lemma']).lower()
				lemma = re.sub('-', '_', lemma)
				lemma = re.sub('_$', '', lemma)
				
				if len(lemma) >= self.min_word_size:
					if re.match('^NN', dic_terms[id_t]['pos']):
						string_corpus += lemma+'__N '
					elif re.match('^(AMOD|JJ|VB|MD|RB|RP)', dic_terms[id_t]['pos']):
						string_corpus += lemma+'__O '
				id_word += 1
				id_t = 's'+str(id_sentence)+'_'+str(id_word)
			id_word = 1
			id_sentence += 1
			id_t = 's'+str(id_sentence)+'_'+str(id_word)
		self.temp_file.write(string_corpus)

