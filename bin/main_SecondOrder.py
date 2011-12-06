#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, re, codecs, os

from collections import defaultdict
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
	max_qty_terms = parameters.getMaxQtyTerms()
	output_folder = parameters.getOutputFolder()
	temp_folder = parameters.getTempFolder()
	seeds_file = parameters.getSeedsFile()

	ling_corpus = StanfordSyntacticContexts(input_folder, temp_folder, min_word_size)
	ling_corpus.writeDicAN(temp_folder+'AN_Relations.txt')
	ling_corpus.writeDicSV(temp_folder+'SV_Relations.txt')
	ling_corpus.writeDicVO(temp_folder+'VO_Relations.txt')

	print 'Merging terms to Relations2ndOrder.txt'
	command = "cat "+temp_folder+'AN_Relations.txt '+temp_folder+'SV_Relations.txt '+temp_folder+'VO_Relations.txt '+' > '+temp_folder+'Relations2ndOrder.txt'
	os.system(command)
	
	measures = Measures(temp_folder+'Relations2ndOrder.txt', seeds_file)
	measures.getTopNJaccardToSeed('customer_information', max_qty_terms)

if __name__ == "__main__":
   main('SecondOrder', sys.argv[1:])

