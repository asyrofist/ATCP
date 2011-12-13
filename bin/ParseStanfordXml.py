#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, sys
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous

class ParseStanfordXml:

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
		xmlfile = misc.openFile(filename, 'r')

		record_dependencies = False
		record_collapsed = False
		for line in xmlfile:
			line = re.sub('\n', '', line)
			if '<sentence ' in line:
				id_s = (line.split('id=\"')[1]).split('\"')[0]
			elif '<token ' in line:
				id_t = 's'+id_s+'_'+(line.split('id=\"')[1]).split('\"')[0]
			elif '<word>' in line:
				word = (line.split('<word>')[1]).split('</word>')[0]
			elif '<lemma>' in line:
				lemma = (line.split('<lemma>')[1]).split('</lemma>')[0]
			elif '<POS>' in line:
				pos = (line.split('<POS>')[1]).split('</POS>')[0]
			elif '<NER>' in line:
				ner = (line.split('<NER>')[1]).split('</NER>')[0]
			elif '</token>' in line:
				array_heads = []
				self.dic_t[id_t] = {'word':word, 'lemma':lemma, 'pos':pos, 'ner':ner, 'headof':array_heads}

			elif '<basic-dependencies>' in line:
				record_dependencies = True
				index_nt = 500
			elif '</basic-dependencies>' in line:
				record_dependencies = False
			elif '<collapsed-ccprocessed-dependencies>' in line:
				record_collapsed = True
			elif '</collapsed-ccprocessed-dependencies>' in line:
				record_collapsed = False

			if record_dependencies or record_collapsed:
				if '<dep type=' in line:
					cat = (line.split('type=\"')[1]).split('\"')[0]
				elif '<governor ' in line:
					idx_gov = (line.split('idx=\"')[1]).split('\"')[0]
					id_t_gov = 's'+id_s+'_'+idx_gov
				elif '<dependent ' in line:
					idx_dep = (line.split('idx=\"')[1]).split('\"')[0]
					id_t_dep = 's'+id_s+'_'+idx_dep
				elif record_dependencies and '</dep>' in line:
					array_edges = []
					array_heads_t = []
					array_ends_t = []
					string_relation = ''
					id_nt = 's'+id_s+'_'+str(index_nt) # s1_500

					array_heads_t = self.dic_t[id_t_gov]['headof']
					array_heads_t.append(id_nt)
					self.dic_t[id_t_gov]['headof'] = array_heads_t

					if int(idx_dep) < int(idx_gov):
						index = int(idx_dep)
						while index <= int(idx_gov):
							id_t = 's'+id_s+'_'+str(index)
							string_relation += self.dic_t[id_t]['lemma']+'_'
							array_edges.append(id_t)
							index += 1
					else:
						index = int(idx_gov)
						while index <= int(idx_dep):
							id_t = 's'+id_s+'_'+str(index)
							string_relation += self.dic_t[id_t]['lemma']+'_'
							array_edges.append(id_t)
							index += 1
					self.dic_nt[id_nt] = {'cat':cat, 'phrase':string_relation[:-1], 'head':id_t_gov, 'dep':id_t_dep, 'edge':array_edges}
					index_nt += 1

				elif record_collapsed and '</dep>' in line:
					new_relation = True
					last_index = index_nt-1
					for value_id in range(500, last_index, 1):
						if self.dic_nt['s'+str(id_s)+'_'+str(value_id)]['head'] == id_t_gov and self.dic_nt['s'+str(id_s)+'_'+str(value_id)]['dep'] == id_t_dep:
							new_relation = False

					if new_relation:
						array_edges = []
						array_heads_t = []
						array_ends_t = []
						string_relation = ''
						id_nt = 's'+id_s+'_'+str(index_nt) # s1_500

						array_heads_t = self.dic_t[id_t_gov]['headof']
						array_heads_t.append(id_nt)
						self.dic_t[id_t_gov]['headof'] = array_heads_t

						if int(idx_dep) < int(idx_gov):
							index = int(idx_dep)
							while index <= int(idx_gov):
								id_t = 's'+id_s+'_'+str(index)
								string_relation += self.dic_t[id_t]['lemma']+'_'
								array_edges.append(id_t)
								index += 1
						else:
							index = int(idx_gov)
							while index <= int(idx_dep):
								id_t = 's'+id_s+'_'+str(index)
								string_relation += self.dic_t[id_t]['lemma']+'_'
								array_edges.append(id_t)
								index += 1
					
						self.dic_nt[id_nt] = {'cat':cat, 'phrase':string_relation[:-1], 'head':id_t_gov, 'dep':id_t_dep, 'edge':array_edges}
						index_nt += 1

		xmlfile.close()

	def __buildNonTerminalStructure__(self):
		for index in self.dic_nt:
			if self.dic_nt[index]['cat'] == 'nn':
				self.dic_nts[index] = self.dic_nt[index]
		self.buidStructure = False

	def __buildDicNouns__(self):
		for id_t in self.dic_t:
			if re.match('^NN', self.dic_t[id_t]['pos']):
				self.dic_nouns[id_t] = self.dic_t[id_t]['lemma']
		self.buidNouns = False

	def __buildDicVerbs__(self):
		for id_t in self.dic_t:
			if re.match('^VB', self.dic_t[id_t]['pos']):
				self.dic_verbs[id_t] = self.dic_t[id_t]['lemma']
		self.buidVerbs = False

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
		for id_nt in self.dic_nts:
			dic_nts_np[id_nts] = self.dic_nt[id_nt]['phrase']
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
			if self.dic_nt[id_nts]['cat'] == 'nn':
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

#if __name__ == '__main__':
#	ps = ParseStanfordXml('/home/roger/Desktop/Temp/corpus.xml')
#	ps.printDicNonTerminals()
