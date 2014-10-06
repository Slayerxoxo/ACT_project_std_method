#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Authors:
	Coraline MARIE

:Date:
	2014/10/6
"""

import sys
import os
import codecs

##############################################################################################################################
# 						    LANCEMENT DU SCRIPT							     #
#															     #
#															     #
# ./ACT_project.py arg1 arg2 arg3 arg4											     #
# 	arg1 => corpus français												     #
# 	arg2 => corpus anglais												     #
# 	arg3 => dictionnaire												     #
# 	arg4 => liste de mots à traduire										     #
#															     #
##############################################################################################################################
# ./ACT_project.py Corpus/termer_source.lem Corpus/termer_target.lem Dictionary/dicfrenelda-utf8.txt Other_src/test_list.txt #
##############################################################################################################################


if __name__ == "__main__":
	if len(sys.argv) > 4:
		for arg in [1, 2, 3, 4]:
			if not os.path.isfile(sys.argv[arg]):
				raise SystemExit, "[ERROR] " + sys.argv[arg] + ": file not found !"
	else:
		raise SystemExit, "[ERROR] "+sys.argv[0]+" expected at least 4 arguments !"


	###############################
	#         ALGORITHME          #
	###############################

	#TODO Récupération de la liste de mots à traduire

	#TODO Construction du vecteur contexte pour ces mots (récupérer les 3 mots avants et les 3 mots après)
		# on compte combien de fois chaque mot apparait

	#TODO Traduction de chaque mot du vecteur de contexte
		# s'il n'y a qu'une traduction

	#TODO 
