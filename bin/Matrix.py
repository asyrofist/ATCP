#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, re, numpy, scipy.sparse, time, os

from sparsesvd import sparsesvd
from math import *
from numpy import *
from numpy.linalg import svd
from collections import OrderedDict
from Miscelaneous import bcolors
from Miscelaneous import Miscelaneous

class Matrix:
	def __init__(self, temp_folder, svd_dimension, record_intermediate):
		self.misc = Miscelaneous()
		self.temp_folder = temp_folder
		self.svd_dimension = svd_dimension
		self.dic_noun = OrderedDict()
		self.dic_noun_index = {}
		self.dic_modifier = OrderedDict()
		self.dic_modifier_index = {}
		self.row = []
		self.col = []
		self.data = []
		self.dic_matrix = {}
		#self.line_data = ''
		list_relations = ['AN', 'SV', 'VO']

		string_files_matrix = ''
		for relation in list_relations:
			self.type_relation = relation
			#self.buildMatrixFromFile()
			#self.applySvd()
			#if record_intermediate:
			#	logfile.writeLogfile('- Recording SVD matrix to '+relation+' in a file...')
			#	self.writeSvd()
			#self.buildRelationsSvd()

			string_files_matrix += self.temp_folder+''+relation+'/Matrix_row.txt '+self.temp_folder+''+relation+'/Matrix_column.txt '
			file_matrix = self.misc.openFile(self.temp_folder+''+relation+'/Matrix_row.txt', 'r')
			for line in file_matrix:
				self.__loadDicMatrix__(line, relation)
			file_matrix.close()

		file_doc_matrix = self.misc.openFile(self.temp_folder+'/Matrix_nouns.txt', 'w')
		number_document = 0
		for noun in self.dic_matrix:
			file_doc_matrix.write(str(number_document)+' : '+noun+'\n')
			command = 'cat'+self.dic_matrix[noun]+' > '+self.temp_folder+'Matrix/'+str(number_document)+'.txt'
			os.system(command)
			if not record_intermediate:
				command = 'rm -Rf'+self.dic_matrix[noun]+' '+string_files_matrix
				os.system(command)
			number_document += 1
		file_doc_matrix.close()

	def __del__(self):
		pass

	def __loadDicMatrix__(self, line, relation):
		line = re.sub('\n', '', line)
		row, noun = line.split(' : ')
		if self.dic_matrix.has_key(noun):
			self.dic_matrix[noun] = self.dic_matrix[noun]+' '+self.temp_folder+''+relation+'/3Order/'+row+'.txt'
		else:
			self.dic_matrix[noun] = ' '+self.temp_folder+''+relation+'/3Order/'+row+'.txt'

	def buildMatrixFromFile(self):
		index_modifier = 0
		index_noun = 0
		line_row = ''
		line_column = ''

		file_relations = self.misc.openFile(self.temp_folder+''+self.type_relation+'/Relations.txt', 'r')
		file_row = self.misc.openFile(self.temp_folder+''+self.type_relation+'/Matrix_row.txt', 'w')
		file_column = self.misc.openFile(self.temp_folder+''+self.type_relation+'/Matrix_column.txt', 'w')
		#file_data = self.misc.openFile(self.temp_folder+''+self.type_relation+'/Matrix_data.txt', 'w')

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
			self.data.append(math.log(float(frequency)+1, e))

			line_row += str(index_n)+' '
			line_column += str(index_m)+' '
			#self.line_data += str(frequency)+' '
		
		file_relations.close()

		for modifier in self.dic_modifier:
			file_column.write(str(self.dic_modifier[modifier])+' : '+modifier+'\n')
		for noun in self.dic_noun:
			file_row.write(str(self.dic_noun[noun])+' : '+noun+'\n')

		#file_data.write('<row>\n')
		#file_data.write(line_row[0:-1]+'\n')
		#file_data.write('<column>\n')
		#file_data.write(line_column[0:-1]+'\n')
		#file_data.write('<data>\n')
		#file_data.write(self.line_data[0:-1]+'\n')

		file_row.close()
		file_column.close()
		#file_data.close()

	def applySvd(self):
		len_row = max(self.row)+1
		len_col = max(self.col)+1
		print 'Applying SVD with ROW: '+str(len_row)+' and COL: '+str(len_col)
		sparse_matrix = scipy.sparse.csc_matrix( (self.data,(self.row,self.col)), shape=(len_row,len_col) )
		print 'sparsed matrix'
		Ut, Sigma, Vt = sparsesvd(sparse_matrix, self.svd_dimension)
		print 'Ut Sigma Vt done!'
		sparse_matrix = array(0)
		print 'Mounting Matrix SVD'
		self.svd_matrix = numpy.dot(Ut.T, numpy.dot(numpy.diag(Sigma), Vt))
		print 'Done!'
		print Ut
		print '\n'
		print Sigma
		print '\n'
		print Vt
		Ut = None
		Sigma = None
		Vt = None
		#Ut = array(0)
		#Sigma = array(0)
		#Vt = array(0)

	def buildRelationsSvd(self):
		index_noun = 0
		for row_data in self.svd_matrix:
			index_modifier = 0
			file_relations_svd = self.misc.openFile(self.temp_folder+''+self.type_relation+'/3Order/'+str(index_noun)+'.txt', 'w')
			for value in row_data:
				file_relations_svd.write(self.dic_modifier_index[index_modifier]+'#'+self.dic_noun_index[index_noun]+'#'+str(value)+'\n')
				index_modifier += 1
			index_noun += 1
			file_relations_svd.close()
		self.svd_matrix = array(0)

	def writeSvd(self):
		file_matrix_svd = self.misc.openFile(self.temp_folder+''+self.type_relation+'/MatrixDataSvd.txt', 'w')
		for row_data in self.svd_matrix:
			for value in row_data:
				file_matrix_svd.write(str(value)+' ')
			file_matrix_svd.write('\n');
		file_matrix_svd.close()
