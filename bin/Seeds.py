#!/usr/bin/python

from Miscelaneous import Miscelaneous

class Seeds:
	def __init__(self, fileinput):
		self.list_seeds = []
		misc = Miscelaneous()
		file_seeds = misc.openFile(fileinput, 'r')

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

