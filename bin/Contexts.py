#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, os, sys

from collections import defaultdict
from ParseStanfordXml import ParseStanfordXml
from Miscelaneous import Miscelaneous
from Miscelaneous import bcolors

class Contexts:

	def __init__(self, temp_folder):
		self.temp_folder = temp_folder
		self.misc = Miscelaneous()
		self.dic_an = {}
		self.dic_sv = {}
		self.dic_vo = {}
		self.matrix_relations = ['AN', 'SV', 'VO']

		for type_relation in self.matrix_relations:
			self.__loadTerms__(type_relation)
		self.__writeDic__()

	def __del__(self):
		pass

	def __loadTerms__(self, type_relation):
		try:
			root, dirs, files = os.walk(self.temp_folder+''+type_relation+'/').next()[:3]
		except IOError:
			print bcolors.FAIL+'ERROR: It was not possible to open the '+self.temp_folder+' folder'+bcolors.ENDC
			sys.exit(2)

		qty_documents = len(files)

		i = 0
		for corpus_file in files:
			i += 1
			if re.match('.*txt$', corpus_file):
				relation_file = self.misc.openFile(root+''+corpus_file, 'r')
				for line in relation_file:
					line = re.sub('\n', '', line)
					relation, noun, frequency = line.split('#')
					if type_relation == 'AN':
						self.__addElementDicAN__(relation+'#'+noun, frequency)
					elif type_relation == 'SV':
						self.__addElementDicSV__(relation+'#'+noun, frequency)
					elif type_relation == 'VO':
						self.__addElementDicVO__(relation+'#'+noun, frequency)
			self.misc.progress_bar(i, qty_documents, 100)

	def __addElementDicAN__(self, relation, frequency):
		if self.dic_an.has_key(relation):
			self.dic_an[relation] += int(frequency)
		else:
			self.dic_an[relation] = int(frequency)

	def __addElementDicSV__(self, relation, frequency):
		if self.dic_sv.has_key(relation):
			self.dic_sv[relation] += int(frequency)
		else:
			self.dic_sv[relation] = int(frequency)

	def __addElementDicVO__(self, relation, frequency):
		if self.dic_vo.has_key(relation):
			self.dic_vo[relation] += int(frequency)
		else:
			self.dic_vo[relation] = int(frequency)

	def __writeDic__(self):
		for type_relation in self.matrix_relations:
			file_relation = self.misc.openFile(self.temp_folder+''+type_relation+'_Relations.txt', 'w')
			dic_relation = self.getDic(type_relation)
			for id_relation in dic_relation:
				file_relation.write(id_relation+'#'+str(dic_relation[id_relation])+'\n')
			file_relation.close()

	""" Get and Print methods """

	def getDic(self, type_relation):
		if type_relation == 'AN': return self.dic_an
		elif type_relation == 'SV': return self.dic_sv
		elif type_relation == 'VO': return self.dic_vo

	def printDic (self, type_relation):
		dic_relation = getDic(type_relation)
		for id_relation in self.dic_relation:
			print id_relation+' = '+str(self.dic_relation[id_relation])
