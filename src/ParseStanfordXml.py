#!/usr/bin/python
#-*- coding: utf-8 -*-

import re, sys
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous
from collections import defaultdict

class ParseStanfordXml:

	def __init__(self, filename):
		self.dic_t = {}
		self.dic_nt = {}
		self.stoplist = []

		self.__buildDics__(filename)

	def __buildDics__(self, filename):
		misc = Miscelaneous()
		xmlfile = misc.openFile(filename, 'r')
		self.stoplist = misc.getStoplist('../misc/stoplist.txt')

		record_dependencies = False
		record_collapsed = False
		for line in xmlfile:
			line = re.sub('\n', '', line)
			if '<sentence ' in line:
				id_s = (line.split('id=\"')[1]).split('\"')[0]	
				array_rec_dep = []
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
				self.dic_t[id_t] = {'word':word, 'lemma':lemma, 'pos':pos, 'ner':ner, 'nps':[]}
				if re.match('NN|NNP', pos):
					array_nps = [lemma.lower()]
					self.dic_t[id_t]['nps'] = array_nps

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
				elif (record_dependencies or record_collapsed) and '</dep>' in line:
					if cat+'#'+id_t_gov+'#'+id_t_dep not in array_rec_dep:
						array_rec_dep.append(cat+'#'+id_t_gov+'#'+id_t_dep)	
						self.dic_nt['s'+id_s+'_'+str(index_nt)] = {'cat':cat, 'gov':id_t_gov, 'dep':id_t_dep}
						index_nt += 1
		xmlfile.close()

		for id_nt in self.dic_nt:
			if re.match("(nn|amod)", self.dic_nt[id_nt]['cat']):
				array_nps = self.dic_t[self.dic_nt[id_nt]['gov']]['nps']
				string = ''
				id_gov = self.dic_nt[id_nt]['gov'].split('_')[1]
				id_dep = self.dic_nt[id_nt]['dep'].split('_')[1]
				id_s = self.dic_nt[id_nt]['dep'].split('_')[0]
				for i in range(int(id_dep), int(id_gov)):
					id_next = id_s+'_'+str(i)
					if re.match("(NN|JJ)", self.dic_t[id_next]['pos']) and self.dic_t[id_next]['lemma'] not in self.stoplist:
						string += self.dic_t[id_next]['lemma']+'_'
				string += self.dic_t[id_s+'_'+id_gov]['lemma']
				if len(string.split('_')) > 1 and string.lower() not in array_nps:
					array_nps.append(string.lower())
				self.dic_t[self.dic_nt[id_nt]['gov']]['nps'] = array_nps

			elif re.match("prep_of", self.dic_nt[id_nt]['cat']):
				id_gov = self.dic_nt[id_nt]['gov']
				id_dep = self.dic_nt[id_nt]['dep']
				
				if re.match("NN", self.dic_t[id_dep]['pos']) and re.match("NN", self.dic_t[id_gov]['pos']):
					array_nps = self.dic_t[id_dep]['nps']
					string = self.dic_t[id_gov]['lemma']+'_of_'+self.dic_t[id_dep]['lemma']
					array_nps.append(string.lower())
					self.dic_t[self.dic_nt[id_nt]['dep']]['nps'] = array_nps

					array_nps = self.dic_t[id_gov]['nps']
					string = self.dic_t[id_gov]['lemma']+'_of_'+self.dic_t[id_dep]['lemma']
					array_nps.append(string.lower())
					self.dic_t[self.dic_nt[id_nt]['gov']]['nps'] = array_nps				

	def getDicTerms(self):
		return self.dic_t

	def getDicNonTerminals(self):
		return self.dic_nt

if __name__ == '__main__':
	ps = ParseXmlStanford('/home/roger/Desktop/corpus.xml')
