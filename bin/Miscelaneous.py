#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, codecs

class Miscelaneous:
	def __init__(self):
		pass

	def __del__(self):
		pass

	def progress_bar(self, value, max, barsize):
		chars = int(value * barsize / float(max))
		percent = int((value / float(max)) * 100)
		sys.stdout.write("#" * chars)
		sys.stdout.write(" " * (barsize - chars + 2))
		if value >= max:
			sys.stdout.write("Done. \n\n")
		else:
			sys.stdout.write("[%3i%%]\r" % (percent))
			sys.stdout.flush()

	def openFile(self, fileinput, mode):
		try:
			opened_file = codecs.open(fileinput, mode, 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the '+fileinput+' file'+bcolors.ENDC
			sys.exit(2)
		return opened_file


class LogFile:
	def __init__(self, dt_now, d, i, l, m, M, p, o, w, t, s, S):
		misc = Miscelaneous()
		self.logfile = misc.openFile('../misc/application.log', 'a')
		self.logfile.write('\nBeginning the process at: '+dt_now+' using the parameters below as configuration:\n')
		self.logfile.write('---------------------------------------------------------------------------------\n')
		self.logfile.write('Svd_dimension : '+str(d)+'\n')
		self.logfile.write('Input folder  : '+i+'\n')
		self.logfile.write('Language      : '+l+'\n')
		self.logfile.write('Min_word_size : '+str(m)+'\n')
		self.logfile.write('Max_qty_terms : '+str(M)+'\n')
		self.logfile.write('Mi_precision  : '+str(p)+'\n')
		self.logfile.write('Output_folder : '+o+'\n')
		self.logfile.write('Window_size   : '+str(w)+'\n')
		self.logfile.write('Temp_folder   : '+t+'\n')
		self.logfile.write('Seeds_file    : '+s+'\n')
		self.logfile.write('Sim_measure   : '+S+'\n')
		self.logfile.write('---------------------------------------------------------------------------------\n')

	def __del__(self):
		self.logfile.close()

	def writeLogfile(self, message):
		self.logfile.write(message)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = "\033[1m"
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
