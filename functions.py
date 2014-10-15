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


# ##############################
#    Nettoyage des sources    #
###############################


###    removeAccent    ###
    #    enlève les accents d'une chaîne
def removeAccent(string):
    string = re.sub(u"[éèëê]", u"e", string)
    string = re.sub(u"[ïî]", u"i", string)
    string = re.sub(u"[àâä]", u"a", string)
    string = re.sub(u"[ôö]", u"o", string)
    string = re.sub(u"[ç]", u"c", string)
    string = re.sub(u"[ûùü]", u"u", string)
    string = re.sub(u"[œ]", u"oe", string)
    return string


###    isAWord    ###
    #    test si une chaine est un mot syntaxiquement français
def isAWord(string):
    ponctuation_lst = [u",", u"?", u";", u":", u"!", u"<", u">", u"\"", u"-", u"\'", u"«", u"»"]
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
    #    récupération du mot seul
    #    suppression des accents
    #    suppression des mots syntaxiquement inintéressant
    #    comptage des mots gardés
    #    suppression des happax


def cleaning_french_corpus(corpus_lst):
    new_lst = []
    tmp_lst = []
    tmp_dict = {}
    for element in corpus_lst:
        element = element.split("/")[-1].split(":")[0]
        element = removeAccent(element)
        element = element.lower()
        if isAWord(element) == 1:
            tmp_lst.append(element)
            if not element in tmp_dict.keys():
                tmp_dict[element] = 1
            else:
                tmp_dict[element] += 1
    for element in tmp_lst:
        if tmp_dict[element] >= 2:
            new_lst.append(element)
    return new_lst


###    cleaning_english_corpus    ###
    #    récupération du mot seul
    #    suppression des mots syntaxiquement inintéressant
def cleaning_english_corpus(corpus_lst):
    new_lst = []
    tmp_lst = []
    tmp_dict = {}
    for element in corpus_lst:
        element = element.split("/")[-2]
        element = element.lower()
        if isAWord(element) == 1:
            tmp_lst.append(element)
            if not element in tmp_dict.keys():
                tmp_dict[element] = 1
            else:
                tmp_dict[element] += 1
    for element in tmp_lst:
        if tmp_dict[element] >= 2:
            new_lst.append(element)
    return new_lst


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