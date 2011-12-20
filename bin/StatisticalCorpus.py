#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, re
from collections import defaultdict
from collections import OrderedDict
from ParsePalavrasXml import ParsePalavrasXml
from ParseStanfordXml import ParseStanfordXml
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous
from Seeds import Seeds

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

		if os.path.exists(self.temp_folder+'Statistical_corpus.txt'):
			os.system('rm '+self.temp_folder+'Statistical_corpus.txt')
		self.temp_file = self.misc.openFile(self.temp_folder+'Statistical_corpus.txt', 'a')

	def __del__(self):
		pass

	def buildCorpus_pt(self):
		i = 0
		for corpus_file in self.files:
			i += 1
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xmlfile = ParsePalavrasXml(self.root+''+corpus_file)
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
		i = 0
		for corpus_file in self.files:
			i += 1
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xmlfile = ParseStanfordXml(self.root+''+corpus_file)
				dic_terms = xmlfile.getDicTerms()
				self.__getRelationsInAWindow__(dic_terms, self.window_size)
				self.misc.progress_bar(i, self.qty_documents, 100)
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

	def buildSTRelations(self, file_input, seeds_file):
		seeds = Seeds(seeds_file)
		list_seeds = seeds.getSeeds()
		dic_tuplas = {}
		file_bigrams = self.misc.openFile(self.temp_folder+''+file_input, 'r')
		first_line = ''

		for line in file_bigrams:
			if first_line != '':
				part = line.split('<>')
				term_type1 = part[0]
				term_type2 = part[1]
				term1, type1 = term_type1.split('__')
				term2, type2 = term_type2.split('__')

				freq_tupla = part[2].split(' ')[0]
				freq_term1 = part[2].split(' ')[1]
				freq_term2 = part[2].split(' ')[2]
				
				if type1 == 'N' and term1 != term2:
					if dic_tuplas.has_key(term2+'#'+term1+'#'):
						dic_tuplas[term2+'#'+term1+'#'] += int(freq_tupla)
					else:
						dic_tuplas[term2+'#'+term1+'#'] = int(freq_tupla)
				if type2 == 'N' and term1 != term2:
					if dic_tuplas.has_key(term1+'#'+term2+'#'):
						dic_tuplas[term1+'#'+term2+'#'] += int(freq_tupla)
					else:
						dic_tuplas[term1+'#'+term2+'#'] = int(freq_tupla)
			else:
				first_line = line
		file_bigrams.close()

		file_relations = self.misc.openFile(self.temp_folder+'W'+str(self.window_size)+'_Relations.txt', 'w')
		for tupla in dic_tuplas:
			file_relations.write(tupla+''+str(dic_tuplas[tupla])+'\n')
		file_relations.close()

