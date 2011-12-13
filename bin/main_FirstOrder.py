#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, re, os

from collections import defaultdict
from StatisticalCorpus import StatisticalCorpus
from Parameters import Parameters
from Thesaurus import Thesaurus
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous
from Measures import MutualInformation
from Measures import Measures

def main(type_atc, argv):
	parameters = Parameters(type_atc, argv)
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = int(parameters.getMinWordSize())
	max_qty_terms = parameters.getMaxQtyTerms()
	mi_precision = parameters.getMIPrecision()
	output_folder = parameters.getOutputFolder()
	window_size = parameters.getWindowSize()
	temp_folder = parameters.getTempFolder()
	seeds_file = parameters.getSeedsFile()
	sim_measure = parameters.getSimilarityMeasure() 
	misc = Miscelaneous()
	stat_corpus = StatisticalCorpus(input_folder, temp_folder, min_word_size, window_size)
	
	if language == 'pt':
		stat_corpus.buildCorpus_pt()	
		param_nsp = '--token ../misc/tokens_nsp.pl'
	elif language == 'en':
		stat_corpus.buildCorpus_en()
		param_nsp = ''

	"""
		Uses count.pl from NGram Statistical Package (NSP) to get Bigrams in a window
	"""

	print 'Getting bigrams to W'+window_size+'_Statistical_corpus.txt'
	command = 'count.pl --ngram 2 '+param_nsp+' --window '+window_size+' '+temp_folder+'W'+window_size+'_Statistical_corpus.txt '+temp_folder+'Statistical_corpus.txt'
	os.system(command)

	if sim_measure == 'mutual_information':
		mi = MutualInformation(temp_folder, 'W'+window_size+'_Statistical_corpus.txt', seeds_file, mi_precision)
		dic_terms = mi.getDicMI()
	else:
		stat_corpus.buildSTRelations('W'+window_size+'_Statistical_corpus.txt', seeds_file)
		measures = Measures(temp_folder+'W'+window_size+'_Relations.txt', seeds_file)
		dic_terms = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)

	thesaurus = Thesaurus(output_folder+'T'+window_size+'_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	thesaurus.write(dic_terms)
	
if __name__ == "__main__":
   main('FirstOrder', sys.argv[1:])
