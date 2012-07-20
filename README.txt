NAME
    README Introduction to Automatic Thesaurus Construction Package (ATCP)

SYNOPSIS
    This document provides a general introduction to the Automatic Thesaurus
    Construction Package.

DESCRIPTION
  1. Introduction
    The Automatic Thesaurus Construction Package (ATCP) is a suite of 
    programs that aids in generating Thesauri from text files. We define a
    thesaurus as a structure composed by seeds and their semantic related
    terms, as follow:
       seed: car
       related: auto, automobile, machine, motorcar etc.

    ATCP consists of three core programs and three utilities:

    Program main_sta.py

    Program main_lin.py
		
    Program main_lsa.py takes plain text files and seeds as input and generates a list of
    related terms to each seed, using the Latentic Semantic Analysis (LSA) algorithm.


  2. Types of construction
    The Automatic Thesaurus Construction Package (ATCP) in its version (v0.1)
    supports three types of automatic construction.  

COPYRIGHT
    Copyright (C) 2011, Roger Granada.

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License, or (at your
    option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
    Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to

        The Free Software Foundation, Inc.,
        59 Temple Place - Suite 330,
        Boston, MA  02111-1307, USA.

    Note: a copy of the GNU General Public License is available on the web
    at <http://www.gnu.org/licenses/gpl.txt> and is included in this
    distribution as GPL.txt.

