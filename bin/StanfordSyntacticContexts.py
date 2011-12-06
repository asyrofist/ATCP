#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, codecs, os, sys

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

		os.system('rm '+self.temp_folder+'SyntacticRelations.txt')
		try:
			self.temp_file = codecs.open(self.temp_folder+'SyntacticRelations.txt', 'a', 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the '+self.temp_folder+'SyntacticRelations.txt file'+bcolors.ENDC
			sys.exit(2)

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

	def __extractRelations__(self):
		i = 0
		#id_sentence = 1
		#id_relation = 500
		#id_nt = 's'+str(id_sentence)+'_'+str(id_relation)
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
				#print id_nt
				noun = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['head']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicVO__(context+'#'+noun)
				#print id_nt +' -> '+self.dic_nt[id_nt]['cat']

			#	id_relation += 1
			#	id_nt = 's'+str(id_sentence)+'_'+str(id_relation)
			#id_relation = 500
			#id_sentence += 1
			#id_nt = 's'+str(id_sentence)+'_'+str(id_relation)

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

	"""
	 Get and Print methods
	"""

	def getDicAN(self):
		return self.dic_an

	def printDicAN(self):
		for id_an in self.dic_an:
			print id_an+' = '+str(self.dic_an[id_an])

	def writeDicAN(self, filename):
		try:
			output_an = codecs.open(filename+'.txt', 'w', 'utf-8')
			for id_an in self.dic_an:
				output_an.write(id_an+'#'+str(self.dic_an[id_an])+'\n')
			output_an.close() 
		except IOError:
			print 'The system could not open the file '+filename+' to write'
			sys.exit(2)

	def getDicSV(self):
		return self.dic_sv

	def printDicSV(self):
		for id_sv in self.dic_sv:
			print id_sv+' = '+str(self.dic_sv[id_sv])

	def writeDicSV(self, filename):
		try:
			output_sv = codecs.open(filename+'.txt', 'w', 'utf-8')
			for id_sv in self.dic_sv:
				output_sv.write(id_sv+'#'+str(self.dic_sv[id_sv])+'\n')
			output_sv.close() 
		except IOError:
			print 'The system could not open the file '+filename+' to write'
			sys.exit(2)

	def getDicVO(self):
		return self.dic_vo

	def printDicVO(self):
		for id_vo in self.dic_vo:
			print id_vo+' = '+str(self.dic_vo[id_vo])

	def writeDicVO(self, filename):
		try:
			output_vo = codecs.open(filename+'.txt', 'w', 'utf-8')
			for id_vo in self.dic_vo:
				output_vo.write(id_vo+'#'+str(self.dic_vo[id_vo])+'\n')
			output_vo.close() 
		except IOError:
			print 'The system could not open the file '+filename+' to write'
			sys.exit(2)
