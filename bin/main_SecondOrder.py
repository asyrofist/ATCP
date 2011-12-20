#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, time, datetime

from Parameters import Parameters
from Seeds import Seeds
from Measures import Measures
from Thesaurus import Thesaurus
from StanfordSyntacticContexts import StanfordSyntacticContexts
from Miscelaneous import LogFile

def main(type_atc, argv):
	start = time.clock()
	date_now = datetime.datetime.now()
	date_now = date_now.strftime("%Y-%m-%d %H:%M:%S")
	
	parameters = Parameters(type_atc, argv)
	contexts = parameters.getContexts()
	input_folder = parameters.getInputFolder()
	language = parameters.getLanguage()
	min_word_size = parameters.getMinWordSize()
	max_qty_terms = int(parameters.getMaxQtyTerms())
	output_folder = parameters.getOutputFolder()
	temp_folder = parameters.getTempFolder()
	record_log = parameters.getRecordLog()
	record_intermediate = parameters.getRecordIntermediate()
	seeds_file = parameters.getSeedsFile()
	sim_measure = parameters.getSimilarityMeasure()
	del parameters

	logfile = LogFile(str(date_now), None, input_folder, language, min_word_size, max_qty_terms, None, output_folder, None, temp_folder, seeds_file, sim_measure)

	if not contexts:
		if record_log:
			logfile.writeLogfile('- Building syntactics relations from '+input_folder+'\n')
		else:
			print '- Building syntactics relations from '+input_folder

		ling_corpus = StanfordSyntacticContexts(input_folder, temp_folder, min_word_size, record_intermediate)
		del ling_corpus

	if record_log:
		logfile.writeLogfile('- Merging terms to '+temp_folder+'Relations2ndOrder.txt\n')
	else:
		print '- Merging terms to '+temp_folder+'Relations2ndOrder.txt'

	if contexts or record_intermediate:
		command = 'cat '+temp_folder+'AN/* '+temp_folder+'SV/* '+temp_folder+'VO/* > '+temp_folder+'Relations2ndOrder.txt'
	else:
		command = 'cat '+temp_folder+'AN_Relations.txt '+temp_folder+'SV_Relations.txt '+temp_folder+'VO_Relations.txt '+' > '+temp_folder+'Relations2ndOrder.txt'
	os.system(command)

	measures = Measures(temp_folder+'Relations2ndOrder.txt', seeds_file)
	dic_topn = measures.getTopNToAllSeeds(sim_measure, max_qty_terms)
	del measures

	if record_log:
		logfile.writeLogfile('- Building thesaurus in '+output_folder+'T_'+type_atc+'_'+sim_measure+'.xml \n')
	else:
		print '- Building thesaurus in '+output_folder+'T_'+type_atc+'_'+sim_measure+'.xml'

	thesaurus = Thesaurus(output_folder+'T_'+type_atc+'_'+sim_measure+'.xml',max_qty_terms)
	thesaurus.write(dic_topn)
	del thesaurus

	end = time.clock()
	if record_log:
		logfile.writeLogfile('- Thesaurus sucessfully built!\nTime consuming: '+str(end - start)+' seconds\n\n')
	else:
		print '- Thesaurus sucessfully built!'

	del logfile

if __name__ == "__main__":
   main('SecondOrder', sys.argv[1:])

