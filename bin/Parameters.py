#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, getopt, re, os
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous

class Parameters:

	def __init__(self, type_atc, argv):
		self.input_folder = '../Data/Corpus/'
		self.output_folder = '../Data/Output/'
		self.temp_folder = '../Data/Temp/'
		self.seeds_file = '../misc/seeds.txt'
		self.misc = Miscelaneous()
		file_parameters = self.misc.openFile('../misc/parameters.cfg', 'r')

		for line in file_parameters:
			if re.match('language', line):
				self.language = line.split('=')[1].replace('\n','')
			if re.match('max_qty_terms', line):
				self.max_qty_terms = line.split('=')[1].replace('\n','')
			if re.match('mi_precision', line):
				self.mi_precision = line.split('=')[1].replace('\n','')
			if re.match('min_word_size', line):
				self.min_word_size = line.split('=')[1].replace('\n','')
			if re.match('sim_measure', line):
				self.sim_measure = line.split('=')[1].replace('\n','')
			if re.match('svd_dimension', line):
				self.svd_dimension = line.split('=')[1].replace('\n','')
			if re.match('window_size', line):
				self.window_size = line.split('=')[1].replace('\n','')
			if re.match('record_log', line):
				record_log = line.split('=')[1].replace('\n','')
				if record_log == 'On': self.record_log = True
				else: self.record_log = False
		file_parameters.close()

		try:
			opts, args = getopt.getopt(argv,\
				"h:i:o:m:M:p:w:d:t:l:r:s:S:", \
				["help", "input=", "output=", "min_size=", "max_terms=", "mi_precision=", "window_size=", "svd_dimension=", "temp=", "language=", "record_log=", "seeds=", "sim_measure="])
		except getopt.GetoptError:
			self.usage(type_atc)
			sys.exit(2)
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				self.help()
				sys.exit(0)
			elif opt in ("-i", "--input"):
				if os.path.isdir(arg): self.input_folder = arg 
				else: print bcolors.WARNING+'WARNING: '+str(arg)+' is not a folder, setting '+self.input_folder+' as input folder'+bcolors.ENDC
			elif opt in ("-o", "--output"):
				if os.path.isdir(arg):  self.output_folder = arg
				else: print bcolors.WARNING+'WARNING: '+str(arg)+' is not a folder, setting '+self.output_folder+' as output folder'+bcolors.ENDC
			elif opt in ("-t", "--temp"): 
				if os.path.isdir(arg): self.temp_folder = arg 
				else: print bcolors.WARNING+'WARNING: '+str(arg)+' is not a folder, setting '+self.temp_folder+' as temporary folder'+bcolors.ENDC 
			elif opt in ("-m", "--min_size"):
				self.min_word_size = arg
			elif opt in ("-M", "--max_terms"):
				self.max_qty_terms = arg
			elif opt in ("-l", "--language"):
				if arg == 'en' or arg == 'pt': self.language = arg
				else: print bcolors.WARNING+'WARNING: "'+str(arg)+'" is not a supported language, setting to "'+self.language+'" as language'+bcolors.ENDC 
			elif opt in ("-r", "--record_log"):
				if arg == 'On': self.record_log = True
				elif arg == 'Off': self.record_log = False
				else: print bcolors.WARNING+'WARNING: "'+str(arg)+'" is not a supported option to log recording, setting to "'+record_log+'" as default option'+bcolors.ENDC 
			elif opt in ("-s", "--seeds"):
				if os.path.isfile(arg): self.seeds_file = arg 
				else: print bcolors.WARNING+'WARNING: '+str(arg)+' is not a file, setting '+self.seeds+' as seeds file'+bcolors.ENDC
			elif opt in ("-S", "--sim_measure"):
				if arg == 'mutual_information' \
					or arg == 'baseline' \
					or arg == 'dicebin' \
					or arg == 'dicemin' \
					or arg == 'jaccard' \
					or arg == 'cosinebin' \
					or arg == 'cosine' \
					or arg == 'city' \
					or arg == 'euclidean' \
					or arg == 'js' \
					or arg == 'lin' \
					or arg == 'jaccardmax': 
					self.sim_measure = arg
				else: 
					print bcolors.WARNING+'WARNING: "'+str(arg)+'" is not a supported similarity measure, setting to "'+self.sim_measure+'" as default similarity measure. 						\nSimilarity measures supported by the system:\n - mutual_information [used only in First Order construction]\n - baseline\n - dicebin\n - dicemin\n - jaccard\n - cosinebin\n - cosine\n - city\n - euclidean\n - js\n - lin\n - jaccardmax'+bcolors.ENDC 

			if type_atc == 'FirstOrder':
				if opt in ("-p", "--mi_precision"):
					self.mi_precision = arg
				elif opt in ("-w", "--window_size"):
					self.window_size = arg

			elif type_atc == 'HigherOrder':
				if opt in ("-d", "--svd_dimension"):
					self.svd_dimension = arg

	def __del__(self):
		pass

	def getInputFolder(self):
		return self.input_folder

	def getLanguage(self):
		return self.language

	def getMinWordSize(self):
		return self.min_word_size

	def getMaxQtyTerms(self):
		return self.max_qty_terms

	def getMIPrecision(self):
		return self.mi_precision

	def getOutputFolder(self):
		return self.output_folder

	def getRecordLog(self):
		return self.record_log

	def getSeedsFile(self):
		return self.seeds_file

	def getSimilarityMeasure(self):
		return self.sim_measure

	def getSvdDimension(self):
		return self.svd_dimension

	def getWindowSize(self):
		return self.window_size

	def getTempFolder(self):
		return self.temp_folder

	def usage(self, type_atc):
		if type_atc == 'FirstOrder':
			usage = """
   Usage: python main_FirstOrder.py [OPTION] [FOLDER]... [OPTION] [PARAMETER]...\n
   -i  --input=               Input folder containing the corpus
   -l  --language=            Language of the corpus data
   -m  --min_size=            Minimum size of a word to be computed
   -M  --max_terms=           Max number of similar terms recorded in the XML file
   -o  --output=              Output folder to receive the data
   -p  --mi_precision=        Precision of the Mutual Information result
   -r  --record_log=          Enable/Disable log file recording
   -s  --seeds=               File containing seeds to the thesaurus
	-S  --sim_measure=         Metric to compute the similarity between seed and related terms
   -w  --window_size=         Size of the window to compute the correlation analysis
   -t  --temp=                Temp folder to receive temporary data
   -h  --help                 Display this help and exit
   """
		elif type_atc == 'HigherOrder':
			usage = """
   Usage: python main_HigherOrder.py [OPTION] [FOLDER]... [OPTION] [PARAMETER]...\n
   -d  --svd_dimension=       Number of dimensions to reduce the SVD
   -i  --input=               Input folder containing the corpus
   -l  --language=            Language of the corpus data
   -m  --min_size=            Minimum size of a word to be computed
   -M  --max_terms=           Max number of similar terms recorded in the XML file
   -o  --output=              Output folder to receive the corpus
   -r  --record_log=          Enable/Disable log file recording
   -s  --seeds=               File containing seeds to the thesaurus
   -S  --sim_measure=         Metric to compute the similarity between seed and related terms
   -t  --temp=                Temp folder to receive temporary data
   -h  --help                 Display this help and exit
   """
		else:
			usage = """
   Usage: python main_SecondOrder.py [OPTION] [FOLDER]... [OPTION] [PARAMETER]...\n
   -i  --input=               Input folder containing the corpus
   -l  --language=            Language of the corpus data
   -m  --min_size=            Minimum size of a word to be computed
   -M  --max_terms=           Max number of similar terms recorded in the XML file
   -o  --output=              Output folder to receive the corpus
   -r  --record_log=          Enable/Disable log file recording
   -s  --seeds=               File containing seeds to the thesaurus
   -S  --sim_measure=         Metric to compute the similarity between seed and related terms
   -t  --temp=                Temp folder to receive temporary data
   -h  --help                 Display this help and exit
   """
		print usage

	def help(self):
		help = """
   HELP FILE:
   -----------------------------------------------------------------------------------------------\n
   [COMMAND] $python ['main' program].py [OPTION] [FOLDER]... [OPTION] [PARAMETER]...\n
   [OPTION] [FOLDER] ... [OPTION] [PARAMETER]
   -d  --svd_dimension= Number of dimensions to reduce the SVD [Used only in main_HigherOrder.py]\n
   -i  --input=         Input folder containing the corpus
                        Default folder: '../Data/Corpus/'\n
   -l  --language=      Language of the corpus data
                        Default language: 'en'
                        Supported languages: 'en' [English] and 'pt' [Portuguese]\n
   -m  --min_size=      Minimum size of a word to be computed
                        Default size: '3' letters\n
   -M  --max_terms=     Max number of similar terms recorded in the XML file
                        Default max: '10' related terms\n
   -o  --output=        Output folder to receive the data
                        Default output: '../Data/Output/'\n
   -p  --mi_precision=  Precision of the Mutual Information result [Used only in main_FirstOrder.py with --sim_measure=mi_information]
                        Default precision: 10\n
   -r  --record_log=    Enable/Disable log file recording
                        Default option: 'Off' [Log file is recorded in ../misc/application.log]
                        Supported options: 'On' and 'Off'
   -s  --seeds=         File containing seeds to the thesaurus
                        Default file: '../misc/seeds.txt'\n
   -S  --sim_measure=   Metric to compute the similarity between seed and related terms
                        Default measure: 'jaccardmax'
                        Supported measures: 'mutual_information', 'baseline', 'dicebin'
                                            'dicemin', 'jaccard', 'cosinebin', 'cosine'
                                            'city', 'euclidean', 'js', 'lin', 'jaccardmax'\n
   -w  --window_size=   Size of the window to compute the correlation analysis [Used only in main_FirstOrder.py]
                        Default size: '20'\n
   -t  --temp=          Temp folder to receive temporary data
                        Default folder: '../Data/Temp/'\n
   -h  --help           Display this help and exit\n
   """
		print help
