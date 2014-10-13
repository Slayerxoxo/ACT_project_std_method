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

from functions import *

# #########################################################################################################
#                                          LANCEMENT DU SCRIPT                                           #
#                                                                                                        #
#															                                             #
# ./ACT_project.py arg1 arg2 arg3 arg4                                                                   #
#   arg1 => corpus français                                                                              #
#   arg2 => corpus anglais                                                                               #
#   arg3 => dictionnaire                                                                                 #
#   arg4 => liste de mots à traduire                                                                     #
#                                                                                                        #
##########################################################################################################
# ./ACT_project.py
#   Corpus/termer_source.lem
#   Corpus/termer_target.lem
#   Dictionary/dicfrenelda-utf8.txt
#   Other_src/test_list.txt #
##########################################################################################################


if __name__ == "__main__":
    if len(sys.argv) > 4:
        for arg in [1, 2, 3, 4]:
            if not os.path.isfile(sys.argv[arg]):
                raise SystemExit, "[ERROR] " + sys.argv[arg] + ": file not found !"
    else:
        raise SystemExit, "[ERROR] " + sys.argv[0] + " expected at least 4 arguments !"


    ###############################
    #         ALGORITHME          #
    ###############################

    #TODO Récupération de la liste de mots à traduire

    #TODO Construction du vecteur contexte pour ces mots (récupérer les 3 mots avants et les 3 mots après)
    # on compte combien de fois chaque mot apparait

    #TODO Traduction de chaque mot du vecteur de contexte
    # s'il n'y a qu'une traduction

    #TODO

    ###############################
    #   Variables de traitement   #
    ###############################
    # True = corpus déjà traité
    french_corpus_clean = True
    english_corpus_clean = False
    dictionary_clean = False
    list_clean = False


    ###############################
    #  Mise en place des sources  #
    ###############################

    if french_corpus_clean == False:
        file_corpus_source = codecs.open(sys.argv[1], "r", "utf-8")
        file_cleaning_french_corpus = codecs.open("Results/french_corpus", "w", "utf-8")
        corpus_source_txt = file_corpus_source.read()
        corpus_source_lst = corpus_source_txt.split(" ")
        file_corpus_source.close()
    else:
        file_cleaning_french_corpus = codecs.open("Results/french_corpus", "r", "utf-8")
        corpus_source_txt = file_cleaning_french_corpus.read()
        corpus_source_lst = corpus_source_txt.split(" ")

    if english_corpus_clean == False:
        file_corpus_target = codecs.open(sys.argv[2], "r", "utf-8")
        file_cleaning_english_corpus = codecs.open("Results/english_corpus", "w", "utf-8")
        corpus_target_txt = file_corpus_target.read()
        corpus_target_lst = corpus_target_txt.split(" ")
        file_corpus_target.close()
    else:
        file_cleaning_english_corpus = codecs.open("Results/english_corpus", "r", "utf-8")
        corpus_target_txt = file_cleaning_english_corpus.read()
        corpus_target_lst = corpus_target_txt.split(" ")



    # ouverture des fichiers sources

    file_dictionary = codecs.open(sys.argv[3], "r", "utf-8")
    file_word_list = codecs.open(sys.argv[4], "r", "utf-8")

    # ouverture des fichiers résultats

    file_cleaning_dictionnary = codecs.open("Results/dictionary", "w", "utf-8")
    file_cleaning_list = codecs.open("Results/list", "w", "utf-8")

    # lecture de l'intégralité des fichiers

    dictionary_txt = file_dictionary.read()
    word_list_txt = file_word_list.read()

    # construction des listes sources

    dictionary_lst = dictionary_txt.split(" ")
    word_list_lst = word_list_txt.split(" ")



    ###############################
    #    Nettoyage des sources    #
    ###############################

    # nettoyage du corpus français
    if french_corpus_clean == False:
        corpus_source_lst = cleaning_french_corpus(corpus_source_lst)
        for element in corpus_source_lst:
            file_cleaning_french_corpus.write(element + " \n")
    else:
        for element in corpus_source_lst:
            if isAWord(element) == 0:
                corpus_source_lst.remove(element)

    # nettoyage du corpus anglais
    # nettoyage du dictionnaire
    # nettoyage de la liste



    ###############################
    #   Conclusion et fermeture   #
    ###############################

    # fermeture des fichiers
    file_cleaning_french_corpus.close()
    file_cleaning_english_corpus.close()
    file_cleaning_dictionnary.close()
    file_cleaning_list.close()


    file_dictionary.close()
    file_word_list.close()

    print("fin du code")