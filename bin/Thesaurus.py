#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, codecs, re, os
from Miscelaneous import Miscelaneous

class Thesaurus:
	def __init__(self, output_file, max_qty_terms):
		self.output_file = output_file
		self.max_qty_terms = max_qty_terms
		misc = Miscelaneous()
		self.thesaurus_file = misc.openFile(output_file, 'w')

	def __del__(self):
		pass

	def write(self, dic_terms):
		self.thesaurus_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<thesaurus>\n')
		for seed in dic_terms:
			qty_terms = 0
			self.thesaurus_file.write('\t<seed term="'+seed+'">\n')
			for index_related_term in dic_terms[seed]['terms']:
				if qty_terms < int(self.max_qty_terms):
					similarity = index_related_term[index_related_term.keys()[0]]
					if not '.' in similarity: similarity += '.'
					for i in range(len(similarity),18): similarity += '0'
					term = index_related_term.keys()[0]
					self.thesaurus_file.write('\t\t<related similarity="'+similarity+'">'+term+'</related>\n')
					qty_terms += 1
			self.thesaurus_file.write('\t</seed>\n')
		self.thesaurus_file.write('</thesaurus>')
		self.thesaurus_file.close()
