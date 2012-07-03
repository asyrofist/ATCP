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
	def __init__(self, input_file, temp_folder, svd_dimension):
		self.misc = Miscelaneous()
		self.temp_folder = temp_folder
		self.svd_dimension = svd_dimension
		self.dic_column = OrderedDict()
		self.dic_column_index = {}
		self.dic_row = OrderedDict()
		self.dic_row_index = {}
		self.array_row = []
		self.array_col = []
		self.array_data = []
		self.dic_matrix = {}

		string_files_matrix = ''

		self.buildMatrixFromFile(input_file)
		self.applySvd()

	def __del__(self):
		pass

	def buildMatrixFromFile(self, input_file):
		index_row = 0
		index_column = 0
		line_row = ''
		line_column = ''
		line_data = ''

		file_input = self.misc.openFile(input_file, 'r')
		file_row = self.misc.openFile(self.temp_folder+'Matrix_row.txt', 'w')
		file_column = self.misc.openFile(self.temp_folder+'Matrix_column.txt', 'w')
		file_data = self.misc.openFile(self.temp_folder+'Matrix_data.txt', 'w')

		for line in file_input:
			line = re.sub('\n', '', line)
			row, column, frequency = line.split('#')
		
			if self.dic_row.has_key(row):
				index_m = self.dic_row[row]
			else:
				self.dic_row[row] = index_row
				self.dic_row_index[index_row] = row
				index_m = index_row
				index_row = index_row + 1

			if self.dic_column.has_key(column):
				index_n = self.dic_column[column]
			else:
				self.dic_column[column] = index_column
				self.dic_column_index[index_column] = column
				index_n = index_column
				index_column = index_column + 1

			self.array_row.append(int(index_n))
			self.array_col.append(int(index_m))
			log_frequency = math.log(float(frequency)+1, e)
			self.array_data.append(float(frequency))

			line_row += str(index_n)+' '
			line_column += str(index_m)+' '
			line_data += str(frequency)+' '
		
		file_input.close()

		for row in self.dic_row:
			file_row.write(str(self.dic_row[row])+' : '+row+'\n')
		for column in self.dic_column:
			file_column.write(str(self.dic_column[column])+' : '+column+'\n')

		file_data.write('<row>\n')
		file_data.write(line_row[0:-1]+'\n')
		file_data.write('<column>\n')
		file_data.write(line_column[0:-1]+'\n')
		file_data.write('<data>\n')
		file_data.write(line_data[0:-1]+'\n')

		file_row.close()
		file_column.close()
		file_data.close()

	def applySvd(self):
		len_row = max(self.array_row)+1
		len_col = max(self.array_col)+1
		print 'Applying SVD with ROW: '+str(len_row)+' and COL: '+str(len_col)
		sparse_matrix = scipy.sparse.csc_matrix( (self.array_data,(self.array_row,self.array_col)), shape=(len_row,len_col) )
		print 'sparsed matrix'
		Ut, Sigma, Vt = sparsesvd(sparse_matrix, self.svd_dimension)
		print 'U Sigma Vt done!'
		sparse_matrix = array(0)
		print 'Mounting Matrix SVD'
		self.svd_matrix = numpy.dot(Ut.T, numpy.dot(numpy.diag(Sigma), Vt))
		print 'Done!'
		print Ut.T
		print '\n'
		print Sigma
		print '\n'
		print Vt
		print '\n'
		print self.svd_matrix.T
		print '\n'
		Ut = None
		Sigma = None
		Vt = None
		#Ut = array(0)
		#Sigma = array(0)
		#Vt = array(0)
