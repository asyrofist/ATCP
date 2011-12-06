#!/usr/bin/python

import sys, codecs
from Miscelaneous import bcolors

class Seeds:
	def __init__(self, fileinput):
		self.list_seeds = []

		try:
			file_seeds = codecs.open(fileinput, 'r', 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the '+fileinput+' file'+bcolors.ENDC
			sys.exit()

		for line in file_seeds:
			if line != '':
				line = line.replace('\n','')
				self.list_seeds.append(line)
		file_seeds.close()

	def getQtySeeds(self):
		return len(self.list_seeds)

	def getSeeds(self):
		return sorted(self.list_seeds)

	def printSeeds(self):
		print self.list_seeds

	def printQtySeeds(self):
		print len(self.list_seeds)

