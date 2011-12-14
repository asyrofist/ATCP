#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, os, sys

from ParseStanfordXml import ParseStanfordXml
from Miscelaneous import Miscelaneous
from Miscelaneous import bcolors

class StanfordSyntacticContexts:

	def __init__(self, input_folder, temp_folder, min_word_size):	
		try:
			self.root, self.dirs, self.files = os.walk(input_folder).next()[:3]
		except IOError:
			print bcolors.FAIL+'ERROR: It was not possible to open the '+input_folder+' folder'+bcolors.ENDC
			sys.exit(2)

		self.min_word_size = int(min_word_size)
		self.temp_folder = temp_folder
		self.qty_documents = len(self.files)
		self.misc = Miscelaneous()

		self.dic_t = {}
		self.dic_nt = {}
		self.dic_an = {}
		self.dic_sv = {}
		self.dic_vo = {}

		i = 0
		for corpus_file in self.files:
			i += 1
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xml = ParseStanfordXml(self.root+''+corpus_file)
				self.dic_t = xml.getDicTerms()
				self.dic_nt = xml.getDicNonTerminals()
				self.__extractRelations__()
			self.misc.progress_bar(i, self.qty_documents, 100)

	def __del__(self):
		pass

	def __extractRelations__(self):
		i = 0

		for id_nt in self.dic_nt:
			if self.dic_nt[id_nt]['cat'] == 'nn':
				noun = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicAN__(context+'#'+noun)
					self.__addElementDicAN__(noun+'#'+context)

			elif self.dic_nt[id_nt]['cat'] == 'amod':
				noun = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicSV__(context+'#'+noun)

			elif self.dic_nt[id_nt]['cat'] == 'prep_for':
				noun = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicAN__('for_'+context+'#'+noun)
					self.__addElementDicAN__('for_'+noun+'#'+context)

			elif self.dic_nt[id_nt]['cat'] == 'prep_of':
				noun = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicAN__('of_'+context+'#'+noun)
					self.__addElementDicAN__('of_'+noun+'#'+context)

			elif re.match('^(nsubjpass|nsubj|xsubj|agent)$', self.dic_nt[id_nt]['cat']):
				noun = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicSV__(context+'#'+noun)
			
			elif re.match('^(dobj|iobj)$', self.dic_nt[id_nt]['cat']):
				noun = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicVO__(context+'#'+noun)

	def __addElementDicAN__(self, relation):
		if self.dic_an.has_key(relation):
			self.dic_an[relation] += 1
		else:
			self.dic_an[relation] = 1

	def __addElementDicSV__(self, relation):
		if self.dic_sv.has_key(relation):
			self.dic_sv[relation] += 1
		else:
			self.dic_sv[relation] = 1

	def __addElementDicVO__(self, relation):
		if self.dic_vo.has_key(relation):
			self.dic_vo[relation] += 1
		else:
			self.dic_vo[relation] = 1

	""" Get and Print methods """

	def getDic(self, type_relation):
		if type_relation == 'AN': return self.dic_an
		elif type_relation == 'SV': return self.dic_sv
		elif type_relation == 'VO': return self.dic_vo

	def printDic (self, type_relation):
		dic_relation = getDic(type_relation)
		for id_relation in self.dic_relation:
			print id_relation+' = '+str(self.dic_relation[id_relation])

	def writeDic (self, type_relation):
		misc = Miscelaneous()
		file_relation = misc.openFile(self.temp_folder+''+type_relation+'_Relations.txt', 'w')
		dic_relation = self.getDic(type_relation)
		for id_relation in dic_relation:
			file_relation.write(id_relation+'#'+str(dic_relation[id_relation])+'\n')
		file_relation.close()
