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
import re

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
# ./ACT_project.py                                                                                       #
#   Corpus/termer_source.lem                                                                             #
#   Corpus/termer_target.lem                                                                             #
#   Dictionary/dicfrenelda-utf8.txt                                                                      #
#   Other_src/test_list.txt                                                                              #
##########################################################################################################
# resultat top 10  40%

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
    # True = document déjà traité
    french_corpus_clean = True
    english_corpus_clean = True
    dictionary_clean = True
    en_vector_context_clean = False
    english_corpus_count = True


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
        corpus_source_lst = []

    if english_corpus_clean == False:
        file_corpus_target = codecs.open(sys.argv[2], "r", "utf-8")
        file_cleaning_english_corpus = codecs.open("Results/english_corpus", "w", "utf-8")
        corpus_target_txt = file_corpus_target.read()
        corpus_target_lst = corpus_target_txt.split(" ")
        file_corpus_target.close()
    else:
        file_cleaning_english_corpus = codecs.open("Results/english_corpus", "r", "utf-8")
        corpus_target_lst = []

    if dictionary_clean == False:
        file_dictionary = codecs.open(sys.argv[3], "r", "utf-8")
        file_cleaning_dictionnary = codecs.open("Results/dictionary", "w", "utf-8")
        dictionary_txt = []
        for lines in file_dictionary.readlines():
            dictionary_txt.append(lines)
        file_dictionary.close()
    else:
        file_cleaning_dictionnary = codecs.open("Results/dictionary", "r", "utf-8")
        dictionary_lst = []

    file_words_list = codecs.open(sys.argv[4], "r", "utf-8")
    word_list_txt = []
    for lines in file_words_list.readlines():
            word_list_txt.append(lines)
    file_words_list.close()

    file_french_stopwords = codecs.open("Other_src/french_stopwords.lst", "r", "utf-8")
    french_stopwords_lst = file_french_stopwords.read()
    file_french_stopwords.close()

    file_english_stopwords = codecs.open("Other_src/english_stopwords.lst", "r", "utf-8")
    english_stopwords_lst = file_english_stopwords.read()
    file_english_stopwords.close()

    if english_corpus_count == False:
        file_english_corpus_count = codecs.open("Results/en_corpus_count", "w", "utf-8")
    else:
        file_english_corpus_count = codecs.open("Results/en_corpus_count", "r", "utf-8")

    file_fr_vector_context = codecs.open("Results/fr_context_vector", "w", "utf-8")

    if en_vector_context_clean == False:
        file_en_vector_context = codecs.open("Results/en_context_vector", "w", "utf-8")
    else:
        file_en_vector_context = codecs.open("Results/en_context_vector", "r", "utf-8")


    ###############################
    #    Nettoyage des sources    #
    ###############################

    # nettoyage du corpus français
    if french_corpus_clean == False:
        affichage(1)
        corpus_source_lst = cleaning_french_corpus(corpus_source_lst, french_stopwords_lst)
        for element in corpus_source_lst:
            file_cleaning_french_corpus.write(element + "\n")
    else:
        affichage(2)
        for lines in file_cleaning_french_corpus.readlines():
            corpus_source_lst.append(lines.rstrip("\n"))
    affichage(0)

    # nettoyage du corpus anglais
    if english_corpus_clean == False:
        affichage(3)
        corpus_target_lst = cleaning_english_corpus(corpus_target_lst, english_stopwords_lst)
        for element in corpus_target_lst:
            file_cleaning_english_corpus.write(element + "\n")
    else:
        affichage(4)
        for lines in file_cleaning_english_corpus.readlines():
            corpus_target_lst.append(lines.rstrip("\n"))
    affichage(0)

    english_counter_dico = {}
    if english_corpus_count == False:
        english_counter_dico = counting_word(corpus_target_lst)
        for element in english_counter_dico.keys():
            file_english_corpus_count.write(element + ";" + str(english_counter_dico[element]) + "\n")
    else:
        for line in file_english_corpus_count.readlines():
            english_counter_dico[line.split(";")[0]] = line.split(";")[-1]


    # nettoyage du dictionnaire
    if dictionary_clean == False:
        affichage(5)
        dictionary_lst = []
        for lines in dictionary_txt:
            dictionary_lst.append(cleaning_dictionnary(lines))
        for (element1,element2) in dictionary_lst:
            file_cleaning_dictionnary.write(element1 + ";" + element2 + "\n")
    else:
        affichage(6)
        for lines in file_cleaning_dictionnary.readlines():
            lines = lines.rstrip("\n")
            dictionary_lst.append((lines.split(";")[0],lines.split(";")[-1]))
    affichage(0)

    # nettoyage de la liste
    affichage(7)
    word_list_lst = cleaning_word_list(word_list_txt)
    affichage(0)


    ###############################
    #    Vecteurs de contextes    #
    ###############################

    # construction de la liste des mots à traduire
    affichage(8)
    lst_to_trad = []
    for (element,list) in word_list_lst:
        lst_to_trad.append(element)
    affichage(0)

    # construction du vecteur de contexte français
    # TODO supprimer les mots absents du corpus
    affichage(9)
    fr_context_vector_lst = []
    tmp_dico = {}
    for element in lst_to_trad:
        tmp_dico = context_vector_construction(element, corpus_source_lst)
        if len(tmp_dico) >= 1:
            fr_context_vector_lst.append((element,tmp_dico))
        else:
            lst_to_trad.remove(element)
    for (element,element_dico) in fr_context_vector_lst:
        file_fr_vector_context.write(element + ":")
        file_fr_vector_context.write(str(element_dico) + "\n")
    affichage(0)

    # traduction du vecteur de contexte en anglais
    affichage(10)

    # pour chaque vecteur
        # pour chaque mot du vecteur
        #     on récupere le mot et sa valeur
        #     on récupère la ou les traductions du mot
        #         s il y a une seule traduction
        #             si cette trad et absente du dico on l ajoute avec la meme valeur dans le nouveau dico
        #             sinon on additionne sa valeur à la précédente
        #         si il y a plusieurs traduction
        #             pour chaque trad on compte le nombre d apparition de cette trad dans le corpus ang
        #             puis on ajoute chaque trad avec pour valeur nb base * nb app / nb trad


    mot_a_traduire = fr_context_vector_lst[0][0]
    vecteur_fr_de_context = fr_context_vector_lst[0][1]
    vecteur_en_de_context = {}

    for element in vecteur_fr_de_context.keys():
        nb_app_fr = vecteur_fr_de_context[element]
        nb_de_trad_diff = 0
        liste_des_tradutions = []
        for (fr_element, en_element) in dictionary_lst:
            if element == fr_element:
                liste_des_tradutions.append(en_element)
                nb_de_trad_diff += 1
        for traduction in liste_des_tradutions:
            if traduction in english_counter_dico.keys():
                if not traduction in vecteur_en_de_context.keys():
                    vecteur_en_de_context[traduction] = (int(nb_app_fr)*int(english_counter_dico[traduction]))/nb_de_trad_diff
                else:
                    vecteur_en_de_context[traduction] += (int(nb_app_fr)*int(english_counter_dico[traduction]))/nb_de_trad_diff

    print mot_a_traduire
    for element in vecteur_en_de_context.keys():
        print (element + ":" + str(vecteur_en_de_context[element]))

    affichage(0)



    ###############################
    #   Conclusion et fermeture   #
    ###############################

    # fermeture des fichiers
    file_cleaning_french_corpus.close()
    file_cleaning_english_corpus.close()
    file_cleaning_dictionnary.close()
    file_english_corpus_count.close()
    file_fr_vector_context.close()
    file_en_vector_context.close()

    print(color.BLUE + "\n\n\nfin du programme\n\n\n" + color.END)