#!/usr/bin/python

import math, codecs, sys, os, re

from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous
from Seeds import Seeds

class Measures:
	def __init__(self, ctx_freq_file, seedfile):
		self.misc = Miscelaneous()
		seeds_file = Seeds(seedfile)
		self.list_seeds = seeds_file.getSeeds()
		self.dic_baseline = defaultdict(dict)
		self.dic_diceBin = defaultdict(dict)
		self.dic_diceMin = defaultdict(dict)
		self.dic_jaccard = defaultdict(dict)
		self.dic_cosineBin = defaultdict(dict)
		self.dic_cosine = defaultdict(dict)
		self.dic_city = defaultdict(dict)
		self.dic_euclidean = defaultdict(dict)
		self.dic_js = defaultdict(dict)
		self.dic_lin = defaultdict(dict)
		self.dic_jaccardMax = defaultdict(dict)
		self.dic_ctx = defaultdict(dict)
		self.dic_sum_freq_noun = {}
		self.dic_qty_noun = {}
		self.__buildHashs__(ctx_freq_file, seedfile)

	def __buildHashs__(self, ctx_freq_file, seedfile):
		list_nouns = []
		ctxfreqfile = self.misc.openFile(ctx_freq_file, 'r')
		
		for line in ctxfreqfile:
			modifier, noun, freq = line.split('#')
			list_nouns.append(noun)
			freq = freq.replace('\n', '')
			self.dic_ctx[noun][modifier] = float(freq)
			if self.dic_sum_freq_noun.has_key(noun):
				self.dic_sum_freq_noun[noun] += float(freq)
			else:
				self.dic_sum_freq_noun[noun] = float(freq)
			if self.dic_qty_noun.has_key(noun):
				self.dic_qty_noun[noun] += 1
			else:
				self.dic_qty_noun[noun] = 1

		for seed in self.list_seeds:
			for related in list_nouns:
				if seed != related:
					baseline = 0
					diceBin = 0
					diceMin = 0
					jaccard = 0
					cosineBin = 0
					cosine = 0
					city = 0
					euclidean = 0
					js = 0
					lin = 0
					jaccardMax = 0

					sun_min = 0
					sun_max = 0
					sum_intersection = 0
					intersection = 0
					square_freq_seed = 0
					square_freq_related = 0
					d_seed = 0
					d_related = 0

					for modifier in self.dic_ctx[seed]:
						freq_seed_modifier = 0
						freq_related_modifier = 0
						if self.dic_ctx[related].has_key(modifier):
							baseline += 1
							freq_seed_modifier = self.dic_ctx[seed][modifier]
							freq_related_modifier = self.dic_ctx[related][modifier]
							sun_min += min(freq_seed_modifier, freq_related_modifier)
							sun_max += max(freq_seed_modifier, freq_related_modifier)
							city += abs(freq_seed_modifier - freq_related_modifier)
							euclidean += (freq_seed_modifier - freq_related_modifier)**2

							relative_freq_seed = float(freq_seed_modifier) / self.dic_sum_freq_noun[seed]
							if self.dic_sum_freq_noun[related] == 0:
								print bcolors.FAIL+'ERROR: Frequency of '+related+' is zero.'+bcolors.ENDC
							else:
								relative_freq_related = float(freq_related_modifier) / self.dic_sum_freq_noun[related]
								relative_freq_seed_related = float(relative_freq_seed + relative_freq_related) / 2

							if relative_freq_seed > 0.0 and relative_freq_seed_related > 0.0:
								d_seed += relative_freq_seed * math.log(float(relative_freq_seed / relative_freq_seed_related))
							if relative_freq_related > 0.0 and relative_freq_seed_related > 0.0:
								d_related += relative_freq_related * math.log(float(relative_freq_related / relative_freq_seed_related))
							intersection += freq_seed_modifier * freq_related_modifier
							sum_intersection += freq_seed_modifier + freq_related_modifier
							square_freq_seed += freq_seed_modifier**2
							square_freq_related += freq_related_modifier**2
				
						elif self.dic_ctx[seed].has_key(modifier):
							freq_seed_modifier = self.dic_ctx[seed][modifier]
							sun_max += freq_seed_modifier
							city += freq_seed_modifier
							euclidean += freq_seed_modifier**2
							square_freq_seed += freq_seed_modifier**2
				
					for modifier in self.dic_ctx[related]:
						if not self.dic_ctx[seed].has_key(modifier):
							freq_related_modifier = self.dic_ctx[related][modifier]
							sun_max += freq_related_modifier
							city += freq_related_modifier
							euclidean += freq_related_modifier**2
							square_freq_related +=  freq_related_modifier**2

					if sun_max > 0:
						jaccardMax = float(sun_min) / sun_max

					if self.dic_qty_noun.has_key(seed) and self.dic_qty_noun.has_key(related):
						diceBin = float(2*baseline) / (self.dic_qty_noun[seed] + self.dic_qty_noun[related])
						cosineBin = baseline / math.sqrt(float(self.dic_qty_noun[seed] * self.dic_qty_noun[related]))
						jaccard = float(baseline) / (self.dic_qty_noun[seed] + self.dic_qty_noun[related] - baseline)
			
					if self.dic_sum_freq_noun.has_key(seed) and self.dic_sum_freq_noun.has_key(related):
						diceMin = float((2*sun_min)) / (self.dic_sum_freq_noun[seed] + self.dic_sum_freq_noun[related])
						lin = float(sum_intersection) / (self.dic_sum_freq_noun[seed] + self.dic_sum_freq_noun[related])

					if square_freq_seed > 0 and square_freq_related > 0:
						cosine = intersection / (math.sqrt(float(square_freq_seed * square_freq_related)))
					euclidean = math.sqrt(float(euclidean))
					js = float(d_seed + d_related) / 2

					if  baseline >= 1:
						self.dic_baseline[seed][related] = baseline
						self.dic_diceBin[seed][related] = diceBin
						self.dic_diceMin[seed][related] = diceMin
						self.dic_jaccard[seed][related] = jaccard
						self.dic_cosineBin[seed][related] = cosineBin
						self.dic_cosine[seed][related] = cosine
						self.dic_city[seed][related] = city
						self.dic_euclidean[seed][related] = euclidean
						self.dic_js[seed][related] = js
						self.dic_lin[seed][related] = lin
						self.dic_jaccardMax[seed][related] = jaccardMax
				
	""" Methods to get the entire dictionaries """
	def getDic(self, sim_measure):
		dic_measure = self.__verifyMeasure__(sim_measure)
		return self.__sortTopNFromAllDic__(dic_measure, 0)

	""" Methods to get the DICs to a specific seed """
	def getDicToSeed(self, sim_measure, seed):
		dic_measure = self.__verifyMeasure__(sim_measure)
		return self.__sortTopNFromDic__(dic_measure, seed, 0)

	""" Methods to get the TOP N to a specific seed """
	def getTopNToSeed(self, sim_measure, seed, n):
		dic_measure = self.__verifyMeasure__(sim_measure)
		return self.__sortTopNFromDic__(dic_measure, seed, n)

	""" Methods to get the TOP N to ALL seeds """
	def getTopNToAllSeeds(self, sim_measure, n):
		dic_measure = self.__verifyMeasure__(sim_measure)
		return self.__sortTopNFromAllDic__(dic_measure, n)

	""" Methods to print the TOP N to a specific seed """
	def printTopNToSeed(self, sim_measure, seed, n):
		dic_terms =  self.getTopNToSeed(sim_measure, seed, n)
		self.__printDic__(dic_terms)

	""" Methods to print the TOP N to ALL seeds """
	def printTopNToAllSeeds(self, sim_measure, n):
		dic_terms = self.getTopNToAllSeeds(sim_measure, n)
		self.__printDic__(dic_terms)

	""" Internal methods """
	def __verifyMeasure__(self, sim_measure):
		if sim_measure == 'baseline': dic_measure = self.dic_baseline
		elif sim_measure == 'dicebin': dic_measure = self.dic_diceBin
		elif sim_measure == 'dicemin': dic_measure = self.dic_diceMin
		elif sim_measure == 'jaccard': dic_measure = self.dic_jaccard
		elif sim_measure == 'cosinebin': dic_measure = self.dic_cosineBin
		elif sim_measure == 'cosine': dic_measure = self.dic_cosine
		elif sim_measure == 'city': dic_measure = self.dic_city
		elif sim_measure == 'euclidean': dic_measure = self.dic_euclidean
		elif sim_measure == 'js': dic_measure = self.dic_js
		elif sim_measure == 'lin': dic_measure = self.dic_lin
		elif sim_measure == 'jaccardmax': dic_measure = self.dic_jaccardMax
		return dic_measure

	def __sortTopNFromDic__(self, dic, seed, n):
		dic_terms = OrderedDict()
		if self.__existKeyInDic__(seed, dic):
			dic_related = {}
			dic_terms[seed] = {'terms': []}
			for related_term in dic[seed]:
				dic_related[related_term] = dic[seed][related_term]
			if n == 0: n = None
			dic_ordered = sorted(dic_related.items(), key=itemgetter(1), reverse=True)[0:n]
			for list_ordered in dic_ordered:
				dic_terms[seed]['terms'].append({list_ordered[0]:str(list_ordered[1])})
		return dic_terms

	def __sortTopNFromAllDic__(self, dic, n):
		dic_terms = OrderedDict()
		dic_related = {}
		for seed in self.list_seeds:
			if self.__existKeyInDic__(seed, dic):
				dic_terms[seed] = {'terms': []}
				for related_term in dic[seed]:
					dic_related[related_term] = dic[seed][related_term]
				if n == 0: n = None
				dic_ordered = sorted(dic_related.items(), key=itemgetter(1), reverse=True)[0:n]
				for list_ordered in dic_ordered:
					dic_terms[seed]['terms'].append({list_ordered[0]:str(list_ordered[1])})
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

		print 'Building list of terms and their relations in '+filename_input+'_to_MI.txt'
		file_relations = self.misc.openFile(self.temp_folder+''+filename_input+'_to_MI.txt', 'w')
		file_relations.write(self.first_line)
		for tupla in self.dic_tuplas:
			file_relations.write(tupla+''+str(self.dic_tuplas[tupla]['freq_tupla'])+' '+str(self.dic_tuplas[tupla]['freq_term1'])+' '+str(self.dic_tuplas[tupla]['freq_term2'])+'\n')
		file_relations.close()

		print 'Getting Mutual Information to IMT_Statistical_corpus.txt'
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
