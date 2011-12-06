#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, codecs, re, os
from Miscelaneous import bcolors
from Accents import Accents

class Thesaurus:
	def __init__(self, output_file, window_size, max_qty_terms):
		self.output_file = output_file
		self.max_qty_terms = max_qty_terms
		try:
			self.thesaurus_file = codecs.open(output_file, 'w', 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the  file '+output_file+''+bcolors.ENDC
			sys.exit(2)

	def write(self, dic_terms):
		accents = Accents()
		self.thesaurus_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<thesaurus>\n')
		for seed in dic_terms:
			qty_terms = 0
			self.thesaurus_file.write('\t<seed term="'+accents.buildAccents(seed)+'">\n')
			for index_related_term in dic_terms[seed]['terms']:
				if qty_terms < int(self.max_qty_terms):
					similarity = index_related_term[index_related_term.keys()[0]]
					term = accents.buildAccents(index_related_term.keys()[0])
					self.thesaurus_file.write('\t\t<related similarity="'+similarity+'">'+term+'</term>\n')
					qty_terms += 1
			self.thesaurus_file.write('\t</seed>\n')
		self.thesaurus_file.write('</thesaurus>')
		self.thesaurus_file.close()
		print 'Thesaurus recorded in '+self.output_file
