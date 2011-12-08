#!/usr/bin/python

import math, codecs, sys

from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
from Miscelaneous import bcolors
from Seeds import Seeds

class Measures:
	def __init__(self, ctx_freq_file, seedfile):
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

		try:
			ctxfreqfile = codecs.open(ctx_freq_file, 'r', 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the '+ctx_freq_file+' file'+bcolors.ENDC
			sys.exit()
		
		for line in ctxfreqfile:
			modifier, noun, freq = line.split('#')
			list_nouns.append(noun)
			freq = freq.replace('\n', '')
			self.dic_ctx[noun][modifier] = int(freq)
			if self.dic_sum_freq_noun.has_key(noun):
				self.dic_sum_freq_noun[noun] += int(freq)
			else:
				self.dic_sum_freq_noun[noun] = int(freq)
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

#if __name__ == '__main__':
#	term = Measures('/home/roger/Desktop/Temp/tempMergedFiles_T3.txt', '../misc/seeds.txt')
#	print term.getTopNJaccardToSeed('customer_information', 10)
