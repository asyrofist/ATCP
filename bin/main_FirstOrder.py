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
	start = time.clock()
	date_now = datetime.datetime.now()
	date_now = date_now.strftime("%Y-%m-%d %H:%M:%S")

	parameters = Parameters(type_atc, argv)
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = int(parameters.getMinWordSize())
	max_qty_terms = int(parameters.getMaxQtyTerms())
	mi_precision = parameters.getMIPrecision()
	output_folder = parameters.getOutputFolder()
	window_size = parameters.getWindowSize()
	temp_folder = parameters.getTempFolder()
	record_log = parameters.getRecordLog()
	seeds_file = parameters.getSeedsFile()
	sim_measure = parameters.getSimilarityMeasure()
	del parameters
 
	if record_log:
		logfile = LogFile(str(date_now), None, input_folder, language, min_word_size, max_qty_terms, mi_precision, output_folder, window_size, temp_folder, seeds_file, sim_measure)
		logfile.writeLogfile('- Building statistical corpus at '+temp_folder+'\n')
	else:
		print '- Building statistical corpus at '+temp_folder

	stat_corpus = StatisticalCorpus(input_folder, temp_folder, min_word_size, window_size)

	if record_log:
		logfile.writeLogfile('- Choosen "'+language+'" as the main language\n')
	else:
		print '- Choosen "'+language+'" as the main language'
	
	if language == 'pt':
		stat_corpus.buildCorpus_pt()	
		param_nsp = '--token ../misc/tokens_nsp.pl'
	elif language == 'en':
		stat_corpus.buildCorpus_en()
		param_nsp = ''

	"""
		Uses count.pl from NGram Statistical Package (NSP) to get Bigrams in a window
	"""

	if record_log:
		logfile.writeLogfile('- Getting bigrams to W'+window_size+'_Statistical_corpus.txt \n')
	else:
		print '- Getting bigrams to W'+window_size+'_Statistical_corpus.txt'

	command = 'count.pl --ngram 2 '+param_nsp+' --window '+window_size+' '+temp_folder+'W'+window_size+'_Statistical_corpus.txt '+temp_folder+'Statistical_corpus.txt'
	os.system(command)

	if record_log:
		logfile.writeLogfile('- Using '+sim_measure+' as similarity measure \n')
	else:
		print '- Using '+sim_measure+' as similarity measure'

	if sim_measure == 'mutual_information':
		mi = MutualInformation(temp_folder, 'W'+window_size+'_Statistical_corpus.txt', seeds_file, mi_precision)
		dic_terms = mi.getDicMI()
	else:
		stat_corpus.buildSTRelations('W'+window_size+'_Statistical_corpus.txt', seeds_file)
		measures = Measures(temp_folder+'W'+window_size+'_Relations.txt', seeds_file)
		dic_terms = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)

	del stat_corpus

	if record_log:
		logfile.writeLogfile('- Building thesaurus in '+output_folder+'T'+window_size+'_'+type_atc+'_'+sim_measure+'.xml \n')
	else:
		print '- Building thesaurus in '+output_folder+'T'+window_size+'_'+type_atc+'_'+sim_measure+'.xml'

	thesaurus = Thesaurus(output_folder+'T'+window_size+'_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	thesaurus.write(dic_terms)

	del thesaurus

	end = time.clock()
	if record_log:
		logfile.writeLogfile('- Thesaurus sucessfully built!\nTime consuming: '+str(end - start)+' seconds\n\n')
	else:
		print '- Thesaurus sucessfully built!'

	del logfile
	
if __name__ == "__main__":
   main('FirstOrder', sys.argv[1:])
