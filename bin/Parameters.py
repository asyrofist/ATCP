#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, getopt, codecs, re, os
from Miscelaneous import bcolors

class Parameters:

	def __init__(self, type_atc, argv):
		self.input_folder = '../../Data/Corpus/'
		self.output_folder = '../../Data/Output/'
		self.temp_folder = '../../Data/Temp/'
		self.seeds_file = '../misc/seeds.txt'

		try:
			file_parameters = codecs.open('../misc/parameters.cfg', 'r', 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the parameters.cfg file to get default configuration'+bcolors.ENDC
			sys.exit(2)

		for line in file_parameters:
			if re.match('language', line):
				self.language = line.split('=')[1].replace('\n','')
			if re.match('max_qty_terms', line):
				self.max_qty_terms = line.split('=')[1].replace('\n','')
			if re.match('mi_precision', line):
				self.mi_precision = line.split('=')[1].replace('\n','')
			if re.match('min_word_size', line):
				self.min_word_size = line.split('=')[1].replace('\n','')
			if re.match('svd_dimension', line):
				self.svd_dimension = line.split('=')[1].replace('\n','')
			if re.match('window_size', line):
				self.window_size = line.split('=')[1].replace('\n','')

		file_parameters.close()

		try:
			opts, args = getopt.getopt(argv,\
				"h:i:o:m:M:p:w:d:t:l:s:", \
				["help", "input=", "output=", "min_size=", "max_terms=", "mi_precision=", "window_size=", "svd_dimension=", "temp=", "language=", "seeds="])
		except getopt.GetoptError:
			self.usage(type_atc)
			sys.exit(2)
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				self.usage(type_atc)
				sys.exit(0)
			elif opt in ("-i", "--input"):
				if os.path.isdir(arg): self.input_folder = arg 
				else: print bcolors.WARNING+'WARNING: '+arg+' is not a folder, setting '+self.input_folder+' as input folder'+bcolors.ENDC
			elif opt in ("-o", "--output"):
				if os.path.isdir(arg): self.output_folder = arg 
				else: print bcolors.WARNING+'WARNING: '+arg+' is not a folder, setting '+self.output_folder+' as output folder'+bcolors.ENDC
			elif opt in ("-t", "--temp"): 
				if os.path.isdir(arg): self.temp_folder = arg 
				else: print bcolors.WARNING+'WARNING: '+arg+' is not a folder, setting '+self.temp_folder+' as temporary folder'+bcolors.ENDC 
			elif opt in ("-m", "--min_size"):
				self.min_word_size = arg
			elif opt in ("-M", "--max_terms"):
				self.max_qty_terms = arg
			elif opt in ("-l", "--language"):
				if arg == 'en' or arg == 'pt': self.language = arg
				else: print bcolors.WARNING+'WARNING: "'+arg+'" is not a supported language, setting to "'+self.language+'" as language'+bcolors.ENDC 
			elif opt in ("-s", "--seeds"):
				if os.path.isfile(arg): self.seeds_file = arg 
				else: print bcolors.WARNING+'WARNING: '+arg+' is not a file, setting '+self.seeds+' as seeds file'+bcolors.ENDC

			if type_atc == 'FirstOrder':
				if opt in ("-p", "--mi_precision"):
					self.mi_precision = arg
				elif opt in ("-w", "--window_size"):
					self.window_size = arg

			elif type_atc == 'HigherOrder':
				if opt in ("-d", "--svd_dimension"):
					self.svd_dimension = arg

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

	def getSeedsFile(self):
		return self.seeds_file

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
   -s  --seeds=               File containing seeds to the thesaurus
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
   -s  --seeds=               File containing seeds to the thesaurus
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
   -s  --seeds=               File containing seeds to the thesaurus
   -t  --temp=                Temp folder to receive temporary data
   -h  --help                 Display this help and exit
   """
		print usage
