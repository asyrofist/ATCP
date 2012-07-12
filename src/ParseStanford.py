#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, sys
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous

class ParseStanford:

	def __init__(self, filename):
		self.dic_t = {}
		self.dic_nt = {}
		self.dic_nts = {}
		self.dic_nouns = {}
		self.dic_verbs = {}
		
		self.buidStructure = True
		self.buidNouns = True
		self.buidVerbs = True

		self.__buildDics__(filename)

	def __buildDics__(self, filename):
		misc = Miscelaneous()
		txtfile = misc.openFile(filename, 'r')

		record_phrase = False
		for line in txtfile:
			line = re.sub('\n', '', line)
			if '(ROOT' in line:
				record_phrase = True
			elif line == '':
				record_phrase = False
			elif record_phrase:
				elements = line.split('(')
				for values in elements:
					if ')' in values:
						term = values.split(')')[0]
						print term


		"""

				self.dic_t[id_t] = {'word':word, 'lemma':lemma, 'pos':pos, 'morph':morph, 'sem':sem, 'extra':extra, 'headof':''}

				self.dic_nt[id_nt] = {'cat':cat, 'edge':array_edges}
			
					self.dic_t[idref]['headof'] = id_nt
					self.dic_nt[id_nt]['head'] = idref

				self.dic_nt[id_nt]['edge'] = array_edges
		"""
		txtfile.close()
	"""
	def __buildNonTerminalStructure__(self):
			self.dic_nts[id_nt] = {'structure': list_np}

			self.dic_nts[id_nts]['phrase'] = phrase.rstrip()


	def __buildDicNouns__(self):
				self.dic_nouns[id_t] = self.dic_t[id_t]['lemma']

	
	def __buildDicVerbs__(self):
				self.dic_verbs[id_t] = self.dic_t[id_t]['lemma']

	def getDicTerms(self):
		return self.dic_t

	def getTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print bcolors.FAIL+'ERROR: Term with ID '+id_t+' was not found'+bcolors.ENDC
			sys.exit()
		return term

	def getDicNonTerminals(self):
		return self.dic_nt

	def getNonTerminalsById(self, id_nt):
		try:
			nonterminal = self.dic_nt[id_nt]
		except:
			print bcolors.FAIL+'ERROR: Non terminal with ID '+id_nt+' was not found'+bcolors.ENDC
			sys.exit()
		return nonterminal

	def getDicNTStructure(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		return self.dic_nts

	def getDicNTStructureToNP(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		dic_nts_np = {}
		for id_nts in self.dic_nts:
			if self.dic_nt[id_nts]['cat'] == 'np':
				dic_nts_np[id_nts] = self.dic_nts[id_nts]
		return dic_nts_np

	def getNTStructureById(self, id_nts):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		try:
			nts = self.dic_nts[id_nts]
		except:
			print bcolors.FAIL+'ERROR: Non terminal structure with ID '+id_nts+' was not found'+bcolors.ENDC
			sys.exit()
		return nts

	def getNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		return self.dic_nouns

	def getListNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		list_nouns = {}
		for id_t in self.dic_nouns:
			list_nouns[self.dic_nouns[id_t]] = self.dic_nouns[id_t]
		return list_nouns

	def getVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		return self.dic_verbs

	def getListVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		list_verbs = {}
		for id_t in self.dic_verbs:
			list_verbs[self.dic_verbs[id_t]] = self.dic_verbs[id_t]
		return list_verbs
	
	def printDicTerms(self):
		for id_t in self.dic_t:
			print 'Key: '+id_t
			print self.dic_t[id_t]
			print '\n'

	def printTermsById(self, id_t):
		try:
			term = self.dic_t[id_t]
		except:
			print bcolors.FAIL+'ERROR: Term with ID '+id_t+' was not found'+bcolors.ENDC
			sys.exit()
		print term

	def printDicNonTerminals(self):
		for id_nt in self.dic_nt:
			print 'Key: '+id_nt
			print self.dic_nt[id_nt]

	def printNonTerminalsById(self, id_nt):
		try:
			nonterminal = self.dic_nt[id_nt]
		except:
			print bcolors.FAIL+'ERROR: Non terminal with ID '+id_nt+' was not found'+bcolors.ENDC
			sys.exit()
		print nonterminal

	def printDicNTStructure(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		for id_nts in self.dic_nts:
			print 'Key: '+id_nts
			print self.dic_nts[id_nts]

	def printDicNTStructureToNP(self):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		for id_nts in self.dic_nts:
			if self.dic_nt[id_nts]['cat'] == 'np':
				print self.dic_nts[id_nts]

	def printNTStructureById(self, id_nts):
		if self.buidStructure:
			self.__buildNonTerminalStructure__()
		try:
			nts = self.dic_nts[id_nts]
		except:
			print bcolors.FAIL+'ERROR: Non terminal structure with ID '+id_nts+' was not found'+bcolors.ENDC
			sys.exit()
		print nts

	def printNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		for id_noun in self.dic_nouns:
			print 'Key: '+id_noun
			print self.dic_nouns[id_noun]

	def printVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		for id_verb in self.dic_verbs:
			print 'Key: '+id_verb
			print self.dic_verbs[id_verb]

	def printListNouns(self):
		if self.buidNouns:
			self.__buildDicNouns__()
		list_nouns = {}
		for id_t in self.dic_nouns:
			list_nouns[self.dic_nouns[id_t]] = self.dic_nouns[id_t]
		for noun in list_nouns:
			print noun+', ',

	def printListVerbs(self):
		if self.buidVerbs:
			self.__buildDicVerbs__()
		list_verbs = {}
		for id_t in self.dic_verbs:
			list_verbs[self.dic_verbs[id_t]] = self.dic_verbs[id_t]
		for verb in list_verbs:
			print verb+', ',
	"""

if __name__ == '__main__':
	ParseStanford('/home/roger/Desktop/parsed.txt')
