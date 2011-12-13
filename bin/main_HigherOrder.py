#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os

from Parameters import Parameters
from Measures import Measures
from Matrix import Matrix
from Thesaurus import Thesaurus
from StanfordSyntacticContexts import StanfordSyntacticContexts

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
	svd_dimension = int(parameters.getSvdDimension())

	ling_corpus = StanfordSyntacticContexts(input_folder, temp_folder, min_word_size)
	ling_corpus.writeDic('AN')
	ling_corpus.writeDic('SV')
	ling_corpus.writeDic('VO')
	del ling_corpus

	matrix_an = Matrix(temp_folder, svd_dimension, 'AN')	
	matrix_an.buildMatrixFromFile()
	matrix_an.applySvd()
	matrix_an.buildRelationsSvd()
	del matrix_an

	matrix_sv = Matrix(temp_folder, svd_dimension, 'SV')	
	matrix_sv.buildMatrixFromFile()
	matrix_sv.applySvd()
	matrix_sv.buildRelationsSvd()
	del matrix_sv

	matrix_vo = Matrix(temp_folder, svd_dimension, 'VO')	
	matrix_vo.buildMatrixFromFile()
	matrix_vo.applySvd()
	matrix_vo.buildRelationsSvd()
	del matrix_vo

	print 'Merging terms to RelationsHigherOrder.txt'
	command = "cat "+temp_folder+'AN_Relations_SVD.txt '+temp_folder+'SV_Relations_SVD.txt '+temp_folder+'VO_Relations_SVD.txt '+' > '+temp_folder+'RelationsHigherOrder.txt'
	os.system(command)

	measures = Measures(temp_folder+'RelationsHigherOrder.txt', seeds_file)
	dic_topn = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)
	thesaurus = Thesaurus(output_folder+'T_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	thesaurus.write(dic_topn)

if __name__ == "__main__":
   main('HigherOrder', sys.argv[1:])

