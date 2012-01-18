#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, os, sys

from collections import defaultdict
from ParseStanfordXml import ParseStanfordXml
from Miscelaneous import Miscelaneous
from Miscelaneous import bcolors

class StanfordSyntacticContexts:

	def __init__(self, input_folder, temp_folder, stoplist_file, min_word_size, record_intermediate):	
		try:
			self.root, self.dirs, self.files = os.walk(input_folder).next()[:3]
		except IOError:
			print bcolors.FAIL+'ERROR: It was not possible to open the '+input_folder+' folder'+bcolors.ENDC
			sys.exit(2)

		self.min_word_size = int(min_word_size)
		self.temp_folder = temp_folder
		self.qty_documents = len(self.files)
		self.misc = Miscelaneous()
		self.stoplist = self.misc.getStoplist(stoplist_file)

		self.dic_t = {}
		self.dic_nt = {}
		self.dic_an = {}
		self.dic_sv = {}
		self.dic_vo = {}

		i = 0
		for corpus_file in self.files:
			print corpus_file
			i += 1
			if re.match('.*xml$', corpus_file):
				corpus_filename = corpus_file.split('.')[0]
				xml = ParseStanfordXml(self.root+''+corpus_file)
				self.dic_t = xml.getDicTerms()
				self.dic_nt = xml.getDicNonTerminals()
				self.__extractRelations__()
				if record_intermediate:
					self.__writeDicRelations__(corpus_filename)
					self.dic_t = {}
					self.dic_nt = {}
					self.dic_an = {}
					self.dic_sv = {}
					self.dic_vo = {}
			#self.misc.progress_bar(i, self.qty_documents, 100)

		if not record_intermediate:
			self.__writeDic__('AN')
			self.__writeDic__('SV')
			self.__writeDic__('VO')

	def __del__(self):
		pass

	def __extractRelations__(self):
		i = 0
		#print self.dic_t
		for id_nt in self.dic_nt:
			if self.dic_nt[id_nt]['cat'] == 'nn':
				noun = self.dic_t[self.dic_nt[id_nt]['gov']]['lemma'].lower()
				#noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicAN__(context+'#'+noun)
					self.__addElementDicAN__(noun+'#'+context)

			elif self.dic_nt[id_nt]['cat'] == 'amod':
				noun = self.dic_t[self.dic_nt[id_nt]['gov']]['lemma'].lower()
				#noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size and context not in self.stoplist:
					self.__addElementDicAN__(context+'#'+noun)
				
			if re.match('prep_', self.dic_nt[id_nt]['cat']) \
				and re.match('^NN', self.dic_t[self.dic_nt[id_nt]['dep']]['pos'])  \
				and re.match('^NN', self.dic_t[self.dic_nt[id_nt]['gov']]['pos']):
				noun = self.dic_t[self.dic_nt[id_nt]['gov']]['lemma'].lower()
				#noun = re.sub('-', '_', noun)
				context = self.dic_t[self.dic_nt[id_nt]['dep']]['lemma'].lower()
				context = re.sub('-', '_', context)
				prep = self.dic_nt[id_nt]['cat'].split('_')[1]
				if len(noun) >= self.min_word_size and len(context) >= self.min_word_size:
					self.__addElementDicAN__(prep+'_'+context+'#'+noun)
					self.__addElementDicAN__(prep+'_'+noun+'#'+context)

			elif re.match('^(nsubjpass|nsubj|xsubj|agent)$', self.dic_nt[id_nt]['cat']): #gov = verb
				if re.match('V', self.dic_t[self.dic_nt[id_nt]['gov']]['pos']):
					verb = self.dic_t[self.dic_nt[id_nt]['gov']]['lemma'].lower()
					#verb = re.sub('-', '_', verb)
					contexts = self.dic_t[self.dic_nt[id_nt]['dep']]['nps']
					for context in contexts:
						if len(verb) >= self.min_word_size and len(context) >= self.min_word_size:
							self.__addElementDicSV__('sub_'+verb+'#'+context)
			
			elif re.match('^(dobj|iobj)$', self.dic_nt[id_nt]['cat']):
				if re.match('V', self.dic_t[self.dic_nt[id_nt]['gov']]['pos']):
					verb = self.dic_t[self.dic_nt[id_nt]['gov']]['lemma'].lower()
					#verb = re.sub('-', '_', verb)
					contexts = self.dic_t[self.dic_nt[id_nt]['dep']]['nps']
					for context in contexts:
						if len(verb) >= self.min_word_size and len(context) >= self.min_word_size:
							self.__addElementDicVO__('obj_'+verb+'#'+context)

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

	def __writeDicRelations__(self, corpus_filename):
		file_relation_an = self.misc.openFile(self.temp_folder+'AN/AN_'+corpus_filename+'.txt', 'w')
		for id_relation in self.dic_an:
			file_relation_an.write(id_relation+'#'+str(self.dic_an[id_relation])+'\n')
		file_relation_an.close()

		file_relation_sv = self.misc.openFile(self.temp_folder+'SV/SV_'+corpus_filename+'.txt', 'w')
		for id_relation in self.dic_sv:
			file_relation_sv.write(id_relation+'#'+str(self.dic_sv[id_relation])+'\n')
		file_relation_sv.close()

		file_relation_vo = self.misc.openFile(self.temp_folder+'VO/VO_'+corpus_filename+'.txt', 'w')
		for id_relation in self.dic_vo:
			file_relation_vo.write(id_relation+'#'+str(self.dic_vo[id_relation])+'\n')
		file_relation_vo.close()

	def __writeDic__(self, type_relation):
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

#if __name__ == '__main__':
#	ps = StanfordSyntacticContexts('/home/roger/Desktop/exe1/', '/home/roger/Desktop/exe2/', 3, False)
