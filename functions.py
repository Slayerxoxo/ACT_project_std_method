#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Authors:
    Coraline MARIE

:Date:
    2014/10/12
"""
import re
import sys
import os
import codecs
import math


# ##############################
# Nettoyage des sources    #
###############################


###    removeAccent    ###
def removeAccent(string):
    '''
    enlève les accents d'une chaîne

    :param string:
    :return:
    '''
    string = string.replace(u"é", "e")
    string = string.replace(u"è", "e")
    string = string.replace(u"ê", "e")
    string = string.replace(u"ë", "e")
    string = string.replace(u"à", "a")
    string = string.replace(u"â", "a")
    string = string.replace(u"ä", "a")
    string = string.replace(u"î", "i")
    string = string.replace(u"ï", "i")
    string = string.replace(u"ô", "o")
    string = string.replace(u"ö", "o")
    string = string.replace(u"ù", "u")
    string = string.replace(u"û", "u")
    string = string.replace(u"ü", "u")
    string = string.replace(u"ç", "c")
    string = string.replace(u"œ", "oe")
    return string



###    replaceSpace    ###
def replaceSpace(string):
    '''
    remplace les espaces par des _

    :param string:
    :return:
    '''
    string = string.replace(u" ", "_")
    return string



###    isAWord    ###
def isAWord(string):
    '''
    test si une chaine est un mot syntaxiquement français

    :param string:
    :return:
    '''
    ponctuation_lst = [u".", u",", u"?", u";", u":", u"!", u"<", u">", u"\"", u"-", u"\'", u"«", u"»"]
    symbol_lst = [u"#", u"%", u"+", u"=", u"/", u"(", u")", u"[", u"]"]
    number_lst = [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0"]
    badWord_lst = [u"__endfile", u"__ENDFILE", u"__file"]
    empty_lst = [u"\r\n", u"\n", u" "]

    for element in ponctuation_lst:
        if element in string:
            return 0
    for element in symbol_lst:
        if element in string:
            return 0
    for element in number_lst:
        if element in string:
            return 0
    for element in badWord_lst:
        if element in string:
            return 0

    if string in empty_lst:
        return 0
    else:
        return 1



###    cleaning_french_corpus    ###
def cleaning_french_corpus(corpus_lst, stopwords_lst):
    '''
    récupération du mot seul
    suppression des accents et majuscules
    suppression des mots syntaxiquement inintéressant
    suppression des happax

    :param corpus_lst:
    :param stopwords_lst:
    :return:
    '''
    new_lst = []
    tmp_lst = []
    tmp_dict = {}
    for element in corpus_lst:
        element = element.split("/")[-1].split(":")[0]
        element = removeAccent(element)
        element = element.lower()
        if isAWord(element) == 1 and not element in stopwords_lst:
            tmp_lst.append(element)
            if not element in tmp_dict.keys():
                tmp_dict[element] = 1
            else:
                tmp_dict[element] += 1
    for element in tmp_lst:
        if tmp_dict[element] >= 2:
            new_lst.append(element)
    return new_lst



#virer la traduction qui n'est pas présente dans le corpus  ET aussi les couple qui n'aparaisent qu'une seule fois


###    cleaning_english_corpus    ###
def cleaning_english_corpus(corpus_lst, stopwords_lst):
    '''
    récupération du mot seul
    suppression des majuscules
    suppression des mots syntaxiquement inintéressant
    suppression des happax

    :param corpus_lst:
    :param stopwords_lst:
    :return:
    '''
    new_lst = []
    tmp_lst = []
    tmp_dict = {}
    for element in corpus_lst:
        element = element.split("/")[-2]
        element = element.lower()
        if isAWord(element) == 1 and not element in stopwords_lst:
            tmp_lst.append(element)
            if not element in tmp_dict.keys():
                tmp_dict[element] = 1
            else:
                tmp_dict[element] += 1
    for element in tmp_lst:
        if tmp_dict[element] >= 2:
            new_lst.append(element)
    return new_lst



###    cleaning_dictionnary    ###
def cleaning_dictionnary(line):
    '''
    récupération des deux mots
    suppression des majuscules
    remplacement des espaces par _

    :param line:
    :return:
    '''
    line = line.rstrip(";\n")
    line = line.lower()
    line = replaceSpace(line)
    line = removeAccent(line)
    new_couple = (line.split(";")[0] , line.split(";")[-2])
    return new_couple

###    cleaning_word_list    ###
def cleaning_word_list(corpus_lst):
    '''
    test si la comparaison est bonne
    récupération des mots comparable
    suppression des accents et majuscules

    :param corpus_lst:
    :return:
    '''
    new_lst = []
    french = ""
    eng_lst = []
    trad_var = False
    first_word = False

    for line in corpus_lst:
        line = line.strip()
        line = line.rstrip("\n")
        if line.split(" ")[0] == "<TRAD" and line.split(" ")[-1] == "valid=\"yes\">":
            trad_var = True
            first_word = True
        elif line == "</TRAD>" and trad_var == True:
            trad_var = False
            new_lst.append((french,eng_lst))
        elif line.split(">")[0] == "<BASE" and trad_var == True:
            if first_word == True:
                french = line.split(">")[1].split("<")[-2]
                french = french.lower()
                french = removeAccent(french)
                french = replaceSpace(french)
                first_word = False
                eng_lst = []
            else:
                eng_lst.append(line.split(">")[1].split("<")[-2])
    return new_lst



###############################
#    Vecteurs de contextes    #
###############################

###    context_vector_construction    ###
def context_vector_construction (word, corpus_lst):
    '''
    construction d'un vecteur de contexte

    :param word:
    :param corpus_lst:
    :return:
    '''
    new_lst = []
    new_dico = {}
    for i , element in enumerate(corpus_lst):
        if element == word:
            new_lst.extend([corpus_lst[i-3], corpus_lst[i-2],corpus_lst[i-1]])
            new_lst.extend([corpus_lst[i+1], corpus_lst[i+2],corpus_lst[i+3]])
    for element in new_lst:
        if not element in new_dico.keys():
            new_dico[element] = 1
        else:
            new_dico[element] += 1
    return new_dico




###    context_vector_traduction    ###
def context_vector_traduction (context_word_lst, dictionary_lst):
    '''
    traduction d'un vecteur de contexte

    :param word:
    :param corpus_lst:
    :return:
    '''
    new_lst = []
    new_dico = {}
    for element in context_word_lst.keys():

        # récupérer toute les traduc
        # s'il y a plusieurs traduc on fait pour chaque traduc (nombre d'apparition de la traduction)*((nombre d'apparition du mot dans le vecteur)/(nombre de trad))
        # ne pas ajouter les mots sans trad

        nb_of_traduction = 0    # nombre de traduction en disponible pour le mot fr
        nb_p_fr = 0 #nombre d'apparition du mot fr dans le vecteur
        for (fr_word,en_word) in dictionary_lst:
            nb_ap_traduction = 0    # nombre de fois ou la traduction apparait dans le corpus en

            if element == fr_word :
                new_lst.append(fr_word)
                nb_of_traduction += 1
                
        # print element
        # print context_word_lst[element]
    return new_dico

# def context_vector_construction (french_word, dictionnary_lst):
#     new_lst = []
#     for sub_lst in dictionnary_lst:
#         if sub_lst[0] == french_word:
#             new_lst = sub_lst
#             new_lst.remove[0]
#             print(french_word + " -> " + new_lst)
#     return new_lst


###############################
#           Calculs           #
###############################

###    cosine    ###
#    calcul le cosinus entre deux dictionnaires
#    v1 et v2 sont les deux vecteurs de contextes liste('mot':frequence)
def cosine(v1, v2):
    if len(v2.keys()) == 0:
        return 0.0

    v1v2 = 0
    v1v1 = 0
    v2v2 = 0
    for attr in set(v1.keys() + v2.keys()):
        if attr in v1:
            attr1 = v1[attr]
        else:
            attr1 = 0

        if attr in v2:
            attr2 = v2[attr]
        else:
            attr2 = 0

        v1v2 += (attr1 * attr2)
        v1v1 += (attr1 * attr1)
        v2v2 += (attr2 * attr2)
    return v1v2 / (math.sqrt(v1v1) * math.sqrt(v2v2))


###############################
# Afficher le top 10          #
###############################
# traductionsCandidates = sorted(traductionsCandidates.items(), key=lambda x: (-x[1], x[0]))
#
#     cleanedTraductionsCandidates = {}
#     counter = 0
#     for el in traductionsCandidates:
#         if counter > 9:
#             break
#         else:
#             cleanedTraductionsCandidates[el[0]] = el[1]
#             counter = counter+1



###############################
#     Organistion du code     #
###############################


###    color    ###
#    mise en forme du texte
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


###    affichage    ###
#    affiche dans la console des textes sur l'exécution du programme
def affichage(num):
    if num == 444:
        print(color.RED + "\nERREUR" + color.END)
    elif num == 0:
        print("                                 " + color.GREEN + " > done" + color.END)
    elif num == 1:
        print(color.BOLD + "\n\nNETTOYAGE DU CORPUS FRANCAIS :" + color.END)
    elif num == 2:
        print(color.BOLD + "\n\nRECUPERATION DU CORPUS FRANCAIS :" + color.END)
    elif num == 3:
        print(color.BOLD + "\n\nNETTOYAGE DU CORPUS ANGLAIS :" + color.END)
    elif num == 4:
        print(color.BOLD + "\n\nRECUPERATION DU CORPUS ANGLAIS :" + color.END)
    elif num == 5:
        print(color.BOLD + "\n\nNETTOYAGE DU DICTIONNAIRE :" + color.END)
    elif num == 6:
        print(color.BOLD + "\n\nRECUPERATION DU DICTIONNAIRE :" + color.END)
    elif num == 7:
        print(color.BOLD + "\n\nNETTOYAGE DE LA LISTE DE MOTS A TRADUIRE :" + color.END)
    elif num == 8:
        print(color.BOLD + "\n\nRECUPERATION DE LA LISTE DE TEST :" + color.END)
    elif num == 9:
        print(color.BOLD + "\n\nCONSTRUCTION DES VECTEURS DE CONTEXTES :" + color.END)