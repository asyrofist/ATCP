#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, time, datetime

from StatisticalCorpus import StatisticalCorpus
from Parameters import Parameters
from Thesaurus import Thesaurus
from Miscelaneous import LogFile
from Measures import MutualInformation
from Measures import Measures

def main(type_atc, argv):
	date_start = datetime.datetime.now()
	date_start = date_start.strftime("%Y-%m-%d %H:%M:%S")

	parameters = Parameters(type_atc, argv)
	contexts = parameters.getContexts()
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = int(parameters.getMinWordSize())
	max_qty_terms = int(parameters.getMaxQtyTerms())
	mi_precision = parameters.getMIPrecision()
	output_folder = parameters.getOutputFolder()
	window_size = parameters.getWindowSize()
	temp_folder = parameters.getTempFolder()
	record_log = parameters.getRecordLog()
	record_intermediate = parameters.getRecordIntermediate()
	seeds_file = parameters.getSeedsFile()
	sim_measure = parameters.getSimilarityMeasure()
	del parameters
 
	logfile = LogFile(record_log, str(date_start), None, input_folder, language, None, min_word_size, max_qty_terms, mi_precision, output_folder, window_size, temp_folder, seeds_file, sim_measure)
	stat_corpus = StatisticalCorpus(input_folder, temp_folder, min_word_size, window_size)

	if not contexts:
		logfile.writeLogfile('- Building statistical corpus at '+temp_folder)
	
		if language == 'pt':
			stat_corpus.buildCorpus_pt()	
			param_nsp = '--token ../misc/tokens_nsp.pl'
		elif language == 'en':
			stat_corpus.buildCorpus_en()
			param_nsp = ''

		"""
			Uses count.pl from NGram Statistical Package (NSP) to get Bigrams in a window
		"""

		logfile.writeLogfile('- Getting bigrams to W'+window_size+'_Statistical_corpus.txt')

		command = 'count.pl --ngram 2 '+param_nsp+' --window '+window_size+' '+temp_folder+'W'+window_size+'_Statistical_corpus.txt '+temp_folder+'Statistical_corpus.txt'
		os.system(command)

		logfile.writeLogfile('- Using '+sim_measure+' as similarity measure')

		if sim_measure == 'mutual_information':
			mi = MutualInformation(temp_folder, 'W'+window_size+'_Statistical_corpus.txt', seeds_file, mi_precision)
			dic_terms = mi.getDicMI()
			del mi
		else:
			stat_corpus.buildSTRelations('W'+window_size+'_Statistical_corpus.txt', seeds_file)
			measures = Measures(temp_folder+'W'+window_size+'_Relations.txt', seeds_file)
			dic_terms = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)
			del measures

	else:
		measures = Measures(temp_folder+'W'+window_size+'_Relations.txt', seeds_file)
		dic_terms = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)
		del measures

	del stat_corpus

	logfile.writeLogfile('- Building thesaurus in '+output_folder+'T'+window_size+'_'+type_atc+'_'+sim_measure+'.xml')

	thesaurus = Thesaurus(output_folder+'T'+window_size+'_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	thesaurus.write(dic_terms)
	del thesaurus

	date_end = datetime.datetime.now()
	date_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
	logfile.writeLogfile('- Thesaurus sucessfully built!\nEnding process at: '+str(date_end)+'.\n')
	del logfile
	
if __name__ == "__main__":
   main('FirstOrder', sys.argv[1:])
