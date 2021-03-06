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
    symbol_lst = [u"#", u"%", u"+", u"=", u"/", u"(", u")", u"[", u"]", u"{", u"}"]
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


def counting_word(corpus_lst):
    new_dico = {}
    for element in corpus_lst:
        if not element in new_dico.keys():
            new_dico[element] = 1
        else:
            new_dico[element] += 1
    return new_dico




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
            if i <= 220246:
                new_lst.extend([corpus_lst[i+1], corpus_lst[i+2],corpus_lst[i+3]])
            elif i == 220247:
                new_lst.extend([corpus_lst[i+1], corpus_lst[i+2]])
            elif i == 220248:
                new_lst.extend([corpus_lst[i+1]])
            if i >= 3:
                new_lst.extend([corpus_lst[i-3], corpus_lst[i-2],corpus_lst[i-1]])
            elif i == 2:
                new_lst.extend([corpus_lst[i-2],corpus_lst[i-1]])
            elif i == 1:
                new_lst.extend([corpus_lst[i-1]])
    for element in new_lst:
        if not element in new_dico.keys():
            new_dico[element] = 1
        else:
            new_dico[element] += 1
    return new_dico


def find_the_trad(elt_key_dico, dictionary_lst):
    already_find = False
    new_lst = []
    new_lst.append(0)
    for (fr_word,en_word) in dictionary_lst:
        if fr_word == elt_key_dico:
            already_find = True
            new_lst[0] += 1
            new_lst.append(en_word)
        elif fr_word != elt_key_dico and already_find == True:
            break
    return new_lst


def add_trad(tmp_dico,tmp_trad_lst, nb_base, en_corpus):
    new_dico = tmp_dico
    if tmp_trad_lst[0] == 1:
        if not tmp_trad_lst[1] in new_dico.keys():
            new_dico[tmp_trad_lst[1]] = nb_base
        else:
            new_dico[tmp_trad_lst[1]] += nb_base
    else:
        tmp_lst = tmp_trad_lst[1:]
        for element in tmp_lst:
            nb_app = 0
            for en_element in en_corpus:
                if element == en_element :
                    nb_app +=1
            if not element in new_dico.keys():
                new_dico[element] = (nb_base*nb_app)/tmp_trad_lst[0]
            else:
                new_dico[tmp_trad_lst[1]] += (nb_base*nb_app)/tmp_trad_lst[0]
    return new_dico




def context_vector_traduction(vecteur_fr_dico, english_corpus_count, dictionary_lst, cognat_lst):
    final_dico = {}
    for element in vecteur_fr_dico.keys():
        trad = False
        somme_trad_total = 0
        nb_app_fr = vecteur_fr_dico[element]
        dico_tmp = {}
        dico_tmp.clear()
        for (fr_word,en_word) in dictionary_lst:
            if element == fr_word and en_word in english_corpus_count.keys():
                trad = True
                dico_tmp[en_word] = float (english_corpus_count[en_word])
                somme_trad_total += float(english_corpus_count[en_word])
        if trad == False:
            for (fr_word,en_word) in cognat_lst:
                if element == fr_word and en_word in english_corpus_count.keys():
                    dico_tmp[en_word] = float (english_corpus_count[en_word])
                    somme_trad_total += float(english_corpus_count[en_word])
        for en_word in dico_tmp.keys():
            if not en_word in final_dico.keys():
                final_dico[en_word] = (float(nb_app_fr)*float(dico_tmp[en_word]))/somme_trad_total
            else:
                final_dico[en_word] += (float(nb_app_fr)*float(dico_tmp[en_word]))/somme_trad_total
    return (final_dico)



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
    elif num == 10:
        print(color.BOLD + "\n\nTRADUCTION DES VECTEURS DE CONTEXTES :" + color.END)
    elif num == 11:
        print(color.BOLD + "\n\nCONSTRUCTION DE TOUS LES VECTEURS DE CONTEXTES ANGLAIS :" + color.END)
    elif num == 12:
        print(color.BOLD + "\n\nCALCULS DES COSINUS :" + color.END)
    elif num == 13:
        print(color.BOLD + "\n\nRESULTATS :" + color.END)
    elif num == 14:
        print(color.BOLD + "\n\nCREATION DES COGNATS :" + color.END)