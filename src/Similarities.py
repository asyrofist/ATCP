#!/usr/bin/python

import math, codecs, sys, os, re

from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous
from Seeds import Seeds

class Similarities:
	def __init__(self, seedfile, temp_folder, sim_measure):
		self.misc = Miscelaneous()
		seeds_file = Seeds(seedfile)
		self.temp_folder = temp_folder
		self.dic_nouns = {}
		self.dic_seeds = defaultdict(dict)
		#self.dic_seeds_freqObj = {}
		#self.dic_seeds_Obj = {}
		self.list_seeds = seeds_file.getSeeds()
		self.dic_measure = defaultdict(dict)
		self.dic_Obj2 = defaultdict(dict)
		self.dic_freqObj = {}
		self.dic_Obj = {}

		self.__buildHashs__(sim_measure)

	def __del__(self):
		pass

	def __buildHashs__(self, sim_measure):
		file_nouns = self.misc.openFile(self.temp_folder+'Matrix_nouns.txt', 'r')
		for line in file_nouns:
			line = re.sub('\n', '', line)
			doc, noun = line.split(' : ')
			self.dic_nouns[doc] = noun
			if noun in self.list_seeds:
				file_doc_seed = self.misc.openFile(self.temp_folder+'Matrix/'+doc+'.txt', 'r')
				self.dic_freqObj[doc] = 0
				self.dic_Obj[doc] = 0
				for line in file_doc_seed:
					line = re.sub('\n', '', line)
					modifier, noun, freq = line.split('#')
					self.dic_seeds[doc][modifier] = float(freq)
					#self.dic_seeds_freqObj[doc] += float(freq)
					#self.dic_seeds_Obj[doc] += 1 
				file_doc_seed.close()
		
		for doc_noun in self.dic_nouns:
			file_doc_nouns = self.misc.openFile(self.temp_folder+'Matrix/'+doc_noun+'.txt', 'r')
			for line in file_doc_nouns:
				line = re.sub('\n', '', line)
				modifier, noun, freq = line.split('#')
				self.dic_Obj2[doc_noun][modifier] = float(freq)
				#self.dic_freqObj[doc] += float(freq)
				#self.dic_Obj[doc] += 1
			file_doc_nouns.close()
		# Colocar o limitador do array para n valores, não consumindo muita memória OU imprimir a lista em um arquivo 
			for doc_seed in self.dic_seeds:
				if doc_noun != doc_seed:
					if sim_measure == 'jaccardMax':
						self.dic_measure[doc_seed][doc_noun] = self.getJaccardMaxMeasure(doc_seed, doc_noun)
					elif sim_measure == 'cosine':
						self.dic_measure[doc_seed][doc_noun] = self.getCosineMeasure(doc_seed, doc_noun)
			del self.dic_Obj2[doc_noun]
		# Deletar a hash criada Obj2


	def getTopNOrderedDic(self, n):
		dic_measure_ordered = self.__sortTopNFromAllDic__(self.dic_measure, n)
		return dic_measure_ordered

	def getJaccardMaxMeasure(self, doc_seed, doc_noun):
		minimum = 0
		maximum = 0
		for attr in self.dic_seeds[doc_seed]:
			if self.dic_Obj2[doc_noun].has_key(attr):
				assoc1 = self.dic_seeds[doc_seed][attr]
				assoc2 = self.dic_Obj2[doc_noun][attr]
				minimum += min(assoc1, assoc2)
				maximum += max(assoc1, assoc2)
			elif self.dic_seeds[doc_seed].has_key(attr):
				maximum += self.dic_seeds[doc_seed][attr]

		for attr2 in self.dic_Obj2[doc_noun]:
			if not self.dic_seeds[doc_seed].has_key(attr2):
				maximum += self.dic_Obj2[doc_noun][attr2]

		if maximum > 0:
			return minimum/maximum
		else:
			return -1

	def getCosineMeasure(self, doc_seed, doc_noun):
		intersection = 0
		o1 = 0
		o2 = 0
		for attr in self.dic_seeds[doc_seed]:
			if self.dic_Obj2[doc_noun].has_key(attr):
				assoc1 = self.dic_seeds[doc_seed][attr]
				assoc2 = self.dic_Obj2[doc_noun][attr]
				intersection += assoc1 * assoc2
				o1 += assoc1**2
				o2 += assoc2**2
			elif self.dic_seeds[doc_seed].has_key(attr):
				o1 += self.dic_seeds[doc_seed][attr]**2

		for attr2 in self.dic_Obj2[doc_noun]:
			if not self.dic_seeds[doc_seed].has_key(attr2):
				o2 += self.dic_Obj2[doc_noun][attr2]**2

		if o1 > 0 and o2 > 0:
			return intersection/math.sqrt(float(o1 * o2))
		else:
			return -1

	def __sortTopNFromAllDic__(self, dic, n):
		dic_terms = OrderedDict()
		self.dic_seeds = sorted(self.dic_seedsp)
		for doc in self.dic_seeds:
			if self.__existKeyInDic__(doc, dic):
				seed = self.dic_nouns[doc]
				dic_terms[seed] = {'terms': []}
				dic_related = {}
				for related_term in dic[doc]:
					dic_related[related_term] = dic[doc][related_term]
				if n == 0: n = None
				dic_ordered = sorted(dic_related.items(), key=itemgetter(1), reverse=True)[0:n]
				for list_ordered in dic_ordered:
					dic_terms[seed]['terms'].append({self.dic_nouns[list_ordered[0]]:str(list_ordered[1])})
		return dic_terms

	def __existKeyInDic__(self, key, dic):
		if dic.has_key(key):
			return dic
		else:
			print bcolors.WARNING+'WARNING: System cannot found the term "'+key+'" in corpus'+bcolors.ENDC
			print ''
			return False

	def __printDic__(self, dic_terms):
		for seed in dic_terms:
			print 'Seed: '+seed
			for index_related_term in dic_terms[seed]['terms']:
					similarity = index_related_term[index_related_term.keys()[0]]
					term = index_related_term.keys()[0]
					print 'Related term: '+term+'\nSimilarity  : '+similarity
			print ''

class MutualInformation:
	def __init__(self, temp_folder, file_input, seedfile, mi_precision):
		self.window_size = file_input[1:-23]
		self.temp_folder = temp_folder
		self.misc = Miscelaneous()
		seeds_file = Seeds(seedfile)
		self.list_seeds = seeds_file.getSeeds()
		self.first_line = ''
		self.dic_tuplas = defaultdict(dict)
		self.dic_terms = OrderedDict()
		self.__buildMI__(file_input, mi_precision)

	def __del__(self):
		pass

	def __buildMI__(self, file_input, mi_precision):
		filename_input = file_input[:-4]
		file_bigrams = self.misc.openFile(self.temp_folder+''+file_input, 'r')
		for line in file_bigrams:
			if self.first_line != '':
				part = line.split('<>')
				term_type1 = part[0]
				term_type2 = part[1]
				term1, type1 = term_type1.split('__')
				term2, type2 = term_type2.split('__')

				freq_tupla = part[2].split(' ')[0]
				freq_term1 = part[2].split(' ')[1]
				freq_term2 = part[2].split(' ')[2]

				if type1 == 'N' and type2 == 'N' and term1 != term2:
					if term1 in self.list_seeds:				
						self.dic_tuplas[term1+'<>'+term2+'<>']['freq_tupla'] = int(freq_tupla)
						self.dic_tuplas[term1+'<>'+term2+'<>']['freq_term1'] = int(freq_term1)
						self.dic_tuplas[term1+'<>'+term2+'<>']['freq_term2'] = int(freq_term2)
					elif term2 in self.list_seeds:
						if self.dic_tuplas.has_key(term2):
							self.dic_tuplas[term2+'<>'+term1+'<>']['freq_tupla'] += int(freq_tupla)
						else:
							self.dic_tuplas[term2+'<>'+term1+'<>']['freq_tupla'] = int(freq_tupla)
							self.dic_tuplas[term2+'<>'+term1+'<>']['freq_term1'] = int(freq_term2)
							self.dic_tuplas[term2+'<>'+term1+'<>']['freq_term2'] = int(freq_term1)

			else:
				self.first_line = line
		file_bigrams.close()

		file_relations = self.misc.openFile(self.temp_folder+''+filename_input+'_to_MI.txt', 'w')
		file_relations.write(self.first_line)
		for tupla in self.dic_tuplas:
			file_relations.write(tupla+''+str(self.dic_tuplas[tupla]['freq_tupla'])+' '+str(self.dic_tuplas[tupla]['freq_term1'])+' '+str(self.dic_tuplas[tupla]['freq_term2'])+'\n')
		file_relations.close()

		command = "statistic.pl tmi.pm -precision "+mi_precision+' '+self.temp_folder+'IM'+self.window_size+'_SecondOrder.txt '+self.temp_folder+''+filename_input+'_to_MI.txt'
		os.system(command)

	def getDicMI(self):
		file_mi = self.misc.openFile(self.temp_folder+'IM'+self.window_size+'_SecondOrder.txt', 'r')

		first_line = False
		list_used_seeds = []
		for line in file_mi:
			if first_line:
				seed, none, term, none, rank, true_mi, freq_1, freq_2, freq_3 = re.split(r'[ |<>]', line)
				if seed in self.list_seeds and seed not in list_used_seeds:
					list_used_seeds.append(seed)
					self.dic_terms[seed] = {'terms': []}
				if seed in self.list_seeds: 
					self.dic_terms[seed]['terms'].append({term:true_mi})	
			else:
				first_line = True
		return self.dic_terms

	def getDicBigrams(self):
		return self.dic_tuplas

	def printDicBigrams(self):
		print self.first_line,
		for tupla in self.dic_tuplas:
			print tupla,self.dic_tuplas[tupla]['freq_tupla'],self.dic_tuplas[tupla]['freq_term1'],self.dic_tuplas[tupla]['freq_term2']
	

#if __name__ == '__main__':
#	term = Measures('/home/roger/Desktop/Temp/tempMergedFiles_T3.txt', '../misc/seeds.txt')
#	print term.getTopNJaccardToSeed('customer_information', 10)

"""
This script is based on the PERL script to Lingua Toolkit built by Pablo Gamallo Otero called "measures.perl". 
This script can be found in Lingua Toolkit package in http://gramatica.usc.es/~gamallo/thesaurus/index.htm
"""
