#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, datetime

from Parameters import Parameters
#from Similarities import Similarities
from Miscelaneous import LogFile
from Thesaurus import Thesaurus
from Contexts import Contexts
from StanfordSyntacticContexts import StanfordSyntacticContexts
from Matrix import Matrix

def main(type_atc, argv):
	list_relations = ['AN', 'SV', 'VO']

	date_start = datetime.datetime.now()
	date_start = date_start.strftime("%Y-%m-%d %H:%M:%S")

	parameters = Parameters(type_atc, argv)
	contexts = parameters.getContexts()
	svd_dimension = int(parameters.getSvdDimension())
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = parameters.getMinWordSize()
	max_qty_terms = int(parameters.getMaxQtyTerms())
	output_folder = parameters.getOutputFolder()
	temp_folder = parameters.getTempFolder()
	record_log = parameters.getRecordLog()
	record_intermediate = parameters.getRecordIntermediate()
	seeds_file = parameters.getSeedsFile()
	stoplist_file = parameters.getStoplistFile()
	sim_measure = parameters.getSimilarityMeasure()
	del parameters

	logfile = LogFile(record_log, str(date_start), svd_dimension, input_folder, language, stoplist_file, min_word_size, max_qty_terms, None, output_folder, None, temp_folder, seeds_file, sim_measure)

	#if contexts:
	#	logfile.writeLogfile('- Building syntactics relations from '+temp_folder)
	#	contexts = Contexts(temp_folder)
	#	del contexts
	#else:
	#	logfile.writeLogfile('- Building syntactics relations from '+input_folder)
	#	ling_corpus = StanfordSyntacticContexts(input_folder, temp_folder, stoplist_file, min_word_size, record_intermediate)
	#	del ling_corpus

	matrix_relation = Matrix(temp_folder, svd_dimension, record_intermediate)		
	del matrix_relation

	#similarities = Similarities(seeds_file, temp_folder, 'cosine')
	#dic_topn = similarities.getTopNOrderedDic(10)
	#del Similarities
	
	#logfile.writeLogfile('- Building thesaurus in '+output_folder+'T_'+type_atc+'_'+sim_measure+'.xml')
	#thesaurus = Thesaurus(output_folder+'T_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	#thesaurus.write(dic_topn)
	#del thesaurus

	date_end = datetime.datetime.now()
	date_end = date_end.strftime("%Y-%m-%d %H:%M:%S")
	logfile.writeLogfile('- Thesaurus sucessfully built!\nEnding process at: '+str(date_end)+'.\n')
	del logfile

if __name__ == "__main__":
   main('HigherOrder', sys.argv[1:])

