#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, re, codecs, os

from collections import defaultdict
from StatisticalCorpus import StatisticalCorpus
from Parameters import Parameters
from Seeds import Seeds
from Thesaurus import Thesaurus
from Miscelaneous import bcolors

def main(type_atc, argv):
	parameters = Parameters(type_atc, argv)
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = parameters.getMinWordSize()
	max_qty_terms = parameters.getMaxQtyTerms()
	mi_precision = parameters.getMIPrecision()
	output_folder = parameters.getOutputFolder()
	window_size = parameters.getWindowSize()
	temp_folder = parameters.getTempFolder()
	seeds_file = parameters.getSeedsFile()

	seeds = Seeds(seeds_file)
	list_seeds = seeds.getSeeds()

	stat_corpus = StatisticalCorpus(input_folder, temp_folder, min_word_size, window_size)
	if language == 'pt':
		stat_corpus.buildCorpus_pt()
	elif language == 'en':
		stat_corpus.buildCorpus_en()

	"""
		Uses count.pl from NGram Statistical Package (NSP) to get Bigrams in a window
	
	print 'Getting bigrams to W'+window_size+'_Statistical_corpus.txt'
	command = 'count.pl --ngram 2 --token ../misc/tokens_nsp.pl --window '+window_size+' '+temp_folder+'W'+window_size+'_Statistical_corpus.txt '+temp_folder+'Statistical_corpus.txt'
	os.system(command)

	try:
		file_bigrams = codecs.open(temp_folder+'W'+window_size+'_Statistical_corpus.txt', 'r', 'utf-8')
	except IOError:
		print bcolors.FAIL+'ERROR: System cannot open the '+temp_folder+'W'+window_size+'_Statistical_corpus.txt file'+bcolors.ENDC
		sys.exit(2)

	first_line = ''
	dic_tuplas = defaultdict(dict)
	for line in file_bigrams:
		if first_line != '':
			part = line.split('<>')
			term_type1 = part[0]
			term_type2 = part[1]
			term1, type1 = term_type1.split('__')
			term2, type2 = term_type2.split('__')

			if len(term1) > 1 and len(term2) > 1:
				freq_tupla = part[2].split(' ')[0]
				freq_term1 = part[2].split(' ')[1]
				freq_term2 = part[2].split(' ')[2]

				if type1 == 'N' and type2 == 'N' and term1 != term2 and (term1 in list_seeds or term2 in list_seeds):				
					if dic_tuplas.has_key(term2+'<>'+term1+'<>'):
						dic_tuplas[term2+'<>'+term1+'<>']['freq_tupla'] += int(freq_tupla)
						dic_tuplas[term2+'<>'+term1+'<>']['freq_term1'] += int(freq_term2)
						dic_tuplas[term2+'<>'+term1+'<>']['freq_term2'] += int(freq_term1)
					else:
						dic_tuplas[term1+'<>'+term2+'<>']['freq_tupla'] = int(freq_tupla)
						dic_tuplas[term1+'<>'+term2+'<>']['freq_term1'] = int(freq_term1)
						dic_tuplas[term1+'<>'+term2+'<>']['freq_term2'] = int(freq_term2)
		else:
			first_line = line
	file_bigrams.close()

	print 'Getting bigrams with seeds to W'+window_size+'_Statistical_seeds.txt'
	try:
		file_stat_seeds = codecs.open(temp_folder+'W'+window_size+'_Statistical_seeds.txt', 'w', 'utf-8')
	except IOError:
		print bcolors.FAIL+'ERROR: System cannot open the '+temp_folder+'W'+window_size+'_Statistical_seeds.txt file'+bcolors.ENDC
		sys.exit(2)
	file_stat_seeds.write(first_line)
	for tupla in dic_tuplas:
		file_stat_seeds.write(tupla+''+str(dic_tuplas[tupla]['freq_tupla'])+' '+str(dic_tuplas[tupla]['freq_term1'])+' '+str(dic_tuplas[tupla]['freq_term2'])+'\n')
	file_stat_seeds.close()

	""" """
		Uses statistic.pl from NGram Statistical Package (NSP) to calculate the Mutual Information between terms
	
	print 'Getting Mutual Information to IMT_Statistical_corpus.txt'
	command = "statistic.pl tmi.pm -precision "+mi_precision+' '+temp_folder+'IM'+window_size+'_Statistical_corpus.txt '+temp_folder+'W'+window_size+'_Statistical_seeds.txt'
	os.system(command)

	dic_terms = defaultdict(dict)
	list_m = []
	try:
		file_mi = codecs.open(temp_folder+'IM'+window_size+'_Statistical_corpus.txt', 'r', 'utf-8')
	except IOError:
		print bcolors.FAIL+'ERROR: System cannot open the '+temp_folder+'IM'+window_size+'_Statistical_corpus.txt file'+bcolors.ENDC
		sys.exit(2)

	first_line = False
	list_used_seeds = []
	for line in file_mi:
		if first_line:
			terms, true_mi, freq_1, freq_2, freq_3 = line.split(' ')
			seed_temp, term_temp, rank = terms.split('<>')
			seed = seed_temp.split('__')[0]
			term = term_temp.split('__')[0]
			if seed not in list_used_seeds:
				list_used_seeds.append(seed)
				dic_terms[seed] = {'terms': []}
			dic_terms[seed]['terms'].append({term:true_mi})	
		else:
			first_line = True

	thesaurus = Thesaurus(output_folder+'T'+window_size+'_'+type_atc+'.xml',max_qty_terms)
	thesaurus.write(dic_terms)
	"""
if __name__ == "__main__":
   main('FirstOrder', sys.argv[1:])






