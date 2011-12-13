#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os

from Parameters import Parameters
from Seeds import Seeds
from Measures import Measures
from Thesaurus import Thesaurus
from StanfordSyntacticContexts import StanfordSyntacticContexts
from Miscelaneous import bcolors

def main(type_atc, argv):
	parameters = Parameters(type_atc, argv)
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = parameters.getMinWordSize()
	max_qty_terms = int(parameters.getMaxQtyTerms())
	output_folder = parameters.getOutputFolder()
	temp_folder = parameters.getTempFolder()
	seeds_file = parameters.getSeedsFile()
	sim_measure = parameters.getSimilarityMeasure() 
	thesaurus = Thesaurus(output_folder+'T_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)

	ling_corpus = StanfordSyntacticContexts(input_folder, temp_folder, min_word_size)
	ling_corpus.writeDic('AN')
	ling_corpus.writeDic('SV')
	ling_corpus.writeDic('VO')

	print 'Merging terms to Relations2ndOrder.txt'
	command = "cat "+temp_folder+'AN_Relations.txt '+temp_folder+'SV_Relations.txt '+temp_folder+'VO_Relations.txt '+' > '+temp_folder+'Relations2ndOrder.txt'
	os.system(command)

	measures = Measures(temp_folder+'Relations2ndOrder.txt', seeds_file)
	dic_topn = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)
	thesaurus.write(dic_topn)

if __name__ == "__main__":
   main('SecondOrder', sys.argv[1:])

