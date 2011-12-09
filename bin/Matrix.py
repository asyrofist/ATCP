#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, re, codecs, numpy, scipy.sparse

from sparsesvd import sparsesvd
from math import *
from numpy import *
from numpy.linalg import svd
from collections import OrderedDict
from Miscelaneous import bcolors

class Matrix:
	def __init__(self, temp_folder, svd_dimension, type_relation):
		self.temp_folder = temp_folder
		self.svd_dimension = svd_dimension
		self.type_relation = type_relation
		self.dic_noun = OrderedDict()
		self.dic_noun_index = {}
		self.dic_modifier = OrderedDict()
		self.dic_modifier_index = {}
		self.row = []
		self.col = []
		self.data = []
		#self.line_data = ''

	def __del__(self):
		print "Removing Object from memory..."

	def buildMatrixFromFile(self):
		index_modifier = 0
		index_noun = 0
		line_row = ''
		line_column = ''

		file_relations = self.__openFile__(self.temp_folder+''+self.type_relation+'_Relations.txt', 'r')
		file_row = self.__openFile__(self.temp_folder+''+self.type_relation+'_Matrix_row.txt', 'w')
		file_column = self.__openFile__(self.temp_folder+''+self.type_relation+'_Matrix_column.txt', 'w')
		#file_data = self.__openFile__(temp_folder+'matrix_data.txt', 'w')

		for line in file_relations:
			line = re.sub('\n', '', line)
			modifier, noun, frequency = line.split('#')
		
			if self.dic_modifier.has_key(modifier):
				index_m = self.dic_modifier[modifier]
			else:
				self.dic_modifier[modifier] = index_modifier
				self.dic_modifier_index[index_modifier] = modifier
				index_m = index_modifier
				index_modifier = index_modifier + 1

			if self.dic_noun.has_key(noun):
				index_n = self.dic_noun[noun]
			else:
				self.dic_noun[noun] = index_noun
				self.dic_noun_index[index_noun] = noun
				index_n = index_noun
				index_noun = index_noun + 1

			self.row.append(int(index_n))
			self.col.append(int(index_m))
			self.data.append(math.log(int(frequency)+1, 10))

			line_row += str(index_n)+' '
			line_column += str(index_m)+' '
			#self.line_data += str(frequency)+' '
		
		file_relations.close()

		for modifier in self.dic_modifier:
			file_column.write(str(self.dic_modifier[modifier])+' : '+modifier+'\n')
		for noun in self.dic_noun:
			file_row.write(str(self.dic_noun[noun])+' : '+noun+'\n')

		#file_data.write('<row>\n')
		#file_data.write(self.line_row[0:-1]+'\n')
		#file_data.write('<column>\n')
		#file_data.write(self.line_column[0:-1]+'\n')
		#file_data.write('<data>\n')
		#file_data.write(self.line_data[0:-1]+'\n')

		file_row.close()
		file_column.close()
		#file_data.close()

	def applySvd(self):
		file_matrix_svd = self.__openFile__(self.temp_folder+''+self.type_relation+'_Matrix_SVD.txt', 'w')
		len_row = max(self.row)+1
		len_col = max(self.col)+1
		print 'Computing SVD to '+self.temp_folder+''+self.type_relation+'_Matrix_SVD.txt...'

		sparse_matrix = scipy.sparse.csc_matrix( (self.data,(self.row,self.col)), shape=(len_row,len_col) )
		Ut, Sigma, Vt = sparsesvd(sparse_matrix, self.svd_dimension)
		sparse_matrix = array(0)
		self.svd_matrix = numpy.dot(Ut.T, numpy.dot(numpy.diag(Sigma), Vt))
		Ut = array(0)
		Sigma = array(0)
		Vt = array(0)

		for row_data in self.svd_matrix:
			for value in row_data:
				file_matrix_svd.write(str(value)+' ')
			file_matrix_svd.write('\n');

		file_matrix_svd.close()

	def buildRelationsSvd(self):
		file_relations_svd = self.__openFile__(self.temp_folder+''+self.type_relation+'_Relations_SVD.txt', 'w')
		index_noun = 0

		for row_data in self.svd_matrix:
			index_modifier = 0
			for value in row_data:
				file_relations_svd.write(self.dic_modifier_index[index_modifier]+'#'+self.dic_noun_index[index_noun]+'#'+str(value)+'\n')
				index_modifier += 1
			index_noun += 1

		file_relations_svd.close()

	def __openFile__(self, fileinput, mode):
		try:
			opened_file = codecs.open(fileinput, mode, 'utf-8')
		except IOError:
			print bcolors.FAIL+'ERROR: System cannot open the '+fileinput+' file'+bcolors.ENDC
			sys.exit(2)
		return opened_file
