import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import math
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import os
import re
from itertools import chain

lem = WordNetLemmatizer()

toRemove = stopwords.words('english')

term_context_temp = []
term_context_list = []
term_context = []
unique_term_context = []
term_context_dict = {}
TFs = []
tf_idf_dict = {}
arr = os.listdir('corpus')
def parse_txt(listDocs, flag):
    global term_context_temp, term_context_list, term_context, unique_term_context, term_context_dict, TFs, tf_idf_dict
    i = 0
    for doc in listDocs:
        print(doc, "This is my documentssssss")
        if doc.endswith(".txt"):
            f = open(doc, "r")
            text = f.read()
            text_list = re.split("\s|(?<!\d)[,.](?!\d)", text)
            for elem in text_list:
                if elem == "":
                    text_list.remove(elem)
            print(text_list, "This is my text list")
            for word in text_list:
                if lem.lemmatize(word.lower()) not in toRemove:
                    word_temp = word
                    word = lem.lemmatize(word.lower(), pos="v")
                    if word_temp is not word:
                        word = lem.lemmatize(word.lower(), pos="n")
                        word_temp = word
                    if word_temp is not word:
                        word = lem.lemmatize(word.lower(), pos="a")

                    term_context_temp.append(word)
                    if (word, str(i)) not in term_context_dict:
                        term_context_dict[word, str(i)] = 1
                    else:
                        term_context_dict[word, str(i)] = term_context_dict[word, str(i)] + 1

        elif doc.endswith(".xml"):
            tree = ET.parse(doc)
            root = tree.getroot()
            if root.text is not None:
                tokenized = str(root.text).split(" ")
                for word in tokenized:
                    if lem.lemmatize(word.lower()) not in toRemove:
                        word_temp = word
                        word = lem.lemmatize(word.lower(), pos="v")
                        if word_temp is not word:
                            word = lem.lemmatize(word.lower(), pos="n")
                            word_temp = word
                        if word_temp is not word:
                            word = lem.lemmatize(word.lower(), pos="a")

                        term_context_temp.append(word)
                        if (word, str(i)) not in term_context_dict:
                            term_context_dict[word, str(i)] = 1
                        else:
                            term_context_dict[word, str(i)] = term_context_dict[word, str(i)] + 1
            createList(root, i)
        term_context_list.append(term_context_temp)
        term_context_temp = []
        TFs.append(compute_TF(term_context_list[i], term_context_dict, i))
        i = i + 1
    extract_TermContext(term_context_list)
    print("Term context: ", term_context)
    print("Term context lists: ", term_context_list)
    print("Term context dict: ", term_context_dict)
    df_tf = pd.DataFrame(TFs)
    df_tf = df_tf.replace(np.nan, 0.0)
    idfs = compute_IDF(term_context_list, list(set(term_context)))
    df_idfs = pd.DataFrame([idfs])
    df_idfs = df_idfs.replace(np.nan, 0.0)
    df_tf_idfs = pd.DataFrame(TFs)
    for term in list(set(term_context)):
        df_tf_idfs[term] = df_tf_idfs[term] * df_idfs.loc[0].at[term]
    df_tf_idfs = df_tf_idfs.replace(np.nan, 0.0)
    # if flag is True:
    #     cos_sim, dice_sim, jacc_sim = sim_measures_TF_IDF(df_tf_idfs)
    # else:
    #     cos_sim, dice_sim, jacc_sim = sim_measures_TF_IDF(df_tf)
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        print(df_tf)
        print(df_idfs)
        print(df_tf_idfs)

    if flag is True:
        cos_sim, dice_sim, jacc_sim = sim_measures_TF_IDF(df_tf_idfs)
    else:
        cos_sim, dice_sim, jacc_sim = sim_measures_TF_IDF(df_tf)
    term_context_temp = []
    term_context_list = []
    term_context = []
    unique_term_context = []
    term_context_dict = {}
    TFs = []
    tf_idf_dict = {}
    return cos_sim, dice_sim, jacc_sim

def extract_TermContext(list_termContext):
    for element in list_termContext:
        if isinstance(element, list):
            extract_TermContext(element)
        else:
            term_context.append(element)

def createList(root, i):
    for child in root:
        if child.text is not None:
            tokenized = str(child.text).split(" ")

            for word in tokenized:
                if lem.lemmatize(word.lower()) not in toRemove:
                    word_temp = word
                    word = lem.lemmatize(word.lower(), pos="v")
                    if word_temp is not word:
                        word = lem.lemmatize(word.lower(), pos="n")
                        word_temp = word
                    if word_temp is not word:
                        word = lem.lemmatize(word.lower(), pos="a")

                    term_context_temp.append(word)
                    if (word, str(i)) not in term_context_dict:
                        term_context_dict[word,  str(i)] = 1
                    else:
                        term_context_dict[word, str(i)] = term_context_dict[word, str(i)] + 1
        createList(child, i)

def compute_TF(list1, dict1, num):
    tfDict = {}
    for item in list1:
        tuple_new = (item, str(num))
        if tuple_new in dict1.keys():
            tfDict[item] = dict1[tuple_new]
    return tfDict

def compute_IDF(list_of_lists, unique_words):
    N = len(arr)
    print(N, "This is N")
    idfDict = dict.fromkeys(unique_words, 0)
    for word in unique_words:
        for list_1 in list_of_lists[1:]:
            if word in list_1:
                idfDict[word] += 1
                continue
    print(idfDict, "This is the dictionary")
    for word, val in idfDict.items():
        if val == 0.0:
            idfDict[word] = 0.0
        else:
            idfDict[word] = math.log10(N/float(val))

    return idfDict

def sim_measures_TF_IDF(dataframe):
    cos_sim_dict = {}
    dice_sim_dict = {}
    jacc_sim_dict = {}
    for_calc = list(dataframe)
    for i in range(1, len(term_context_list)):
        numer = 0
        for term in for_calc:
            numer = numer + (dataframe.loc[0].at[term] * dataframe.loc[i].at[term] )
        dotProd = calculate_mag(dataframe.loc[0]) * calculate_mag(dataframe.loc[i])
        dotProd2 = math.pow(calculate_mag(dataframe.loc[0]), 2) + math.pow(calculate_mag(dataframe.loc[i]), 2)
        if dotProd == 0.0:
            cos_sim_dict[i] = 0.0
        else:
            cos_sim_dict[i] = numer / dotProd
        if dotProd2 == 0.0:
            dice_sim_dict[i] = 0.0
        else:
            dice_sim_dict[i] = (2*numer)/dotProd2
        if (dotProd2 - numer) == 0.0:
            jacc_sim_dict[i] = 0.0
        else:
            jacc_sim_dict[i] = numer /(dotProd2 - numer)
    return cos_sim_dict, dice_sim_dict, jacc_sim_dict

def calculate_mag(row):
    z = math.sqrt(sum(pow(element, 2) for element in row))
    return z


