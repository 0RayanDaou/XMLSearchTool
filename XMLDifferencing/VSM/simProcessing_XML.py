import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import math
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import os
from itertools import chain

lem = WordNetLemmatizer()

toRemove = stopwords.words('english')

labelA = []
term_context_temp = []
term_context_list = []
term_context = []
unique_term_context = []
term_context_dict = {}
TFs = []
tf_idf_dict = {}
arr = os.listdir('corpus2')
def parse(listDocs, flag):
    global labelA, term_context_temp, term_context_list, term_context, unique_term_context, term_context_dict, TFs, tf_idf_dict
    i = 0
    for doc in listDocs:
        tree = ET.parse(doc)
        root = tree.getroot()
        labelA.append(root.tag)
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

                    term_context_temp.append((word, labelA[len(labelA) - 1]))
                    if (word, labelA[len(labelA) - 1] + str(i)) not in term_context_dict:
                        term_context_dict[word, labelA[len(labelA) - 1] + str(i)] = 1
                    else:
                        term_context_dict[word, labelA[len(labelA) - 1] + str(i)] = term_context_dict[word, labelA[
                            len(labelA) - 1] + str(i)] + 1
        createList(root, i)
        term_context_list.append(term_context_temp)
        term_context_temp = []
        labelA = []
        TFs.append(compute_TF(term_context_list[i], term_context_dict, i))
        i = i + 1
    extract_TermContext(term_context_list)
    unique_term_context = list(set(term_context))
    idfs = compute_IDF(term_context_list, unique_term_context)
    df_tf = pd.DataFrame(TFs)
    df_tf = df_tf.replace(np.nan, 0.0)
    df_idfs = pd.DataFrame([idfs])
    df_idfs = df_idfs.replace(np.nan, 0.0)
    df_tf_idfs = pd.DataFrame(TFs)
    for term in unique_term_context:
        df_tf_idfs[term] = df_tf_idfs[term] * df_idfs.loc[0].at[term]
    df_tf_idfs = df_tf_idfs.replace(np.nan, 0.0)
    if flag is True:
        cos_sim, dice_sim, jacc_sim = sim_measures_TF_IDF(df_tf_idfs)
    else:
        cos_sim, dice_sim, jacc_sim = sim_measures_TF_IDF(df_tf)
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        print(df_tf)
        print(df_idfs)
        print(df_tf_idfs)
    # print( cos_sim, dice_sim, jacc_sim, sep="\n")
    labelA = []
    term_context_temp = []
    term_context_list = []
    term_context = []
    unique_term_context = []
    term_context_dict = {}
    TFs = []
    idfs = {}
    tf_idf_dict = {}
    print(cos_sim, dice_sim, jacc_sim, sep="\n")
    return cos_sim, dice_sim, jacc_sim
def createList(root, i):
    lastLabelA = labelA[len(labelA) - 1]
    for child in root:
        labelA.append(lastLabelA + "/" + child.tag)
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

                    term_context_temp.append((word, labelA[len(labelA) - 1]))
                    if (word, labelA[len(labelA) - 1] + str(i)) not in term_context_dict:
                        term_context_dict[word, labelA[len(labelA) - 1] + str(i)] = 1
                    else:
                        term_context_dict[word, labelA[len(labelA) - 1] + str(i)] = term_context_dict[word, labelA[
                            len(labelA) - 1] + str(i)] + 1
        createList(child, i)


def compute_TF(list1, dict1, num):
    tfDict = {}
    for term in list1:
        temp = list(term)
        temp[1] = temp[1] + str(num)
        term = tuple(temp)
        if term in dict1.keys():
            temp2 = term
            temp = list(term)
            temp[1] = temp[1].replace(temp[1][-1], "")
            term = tuple(temp)
            tfDict[term] = dict1[temp2]
    return tfDict

def extract_TermContext(list_termContext):
    for element in list_termContext:
        if isinstance(element, list):
            extract_TermContext(element)
        else:
            term_context.append(element)
#zabto haydi corpus kilo length
def compute_IDF(list_of_lists, uniqueTermList):
    #number of documents
    N = len(arr)
    idfDict = dict.fromkeys(uniqueTermList, 0)
    for tuple1 in uniqueTermList:
        for temp in list_of_lists:
            if tuple1 in temp:
                idfDict[tuple1] += 1
    for word, val in idfDict.items():
        if val == 0.0:
            idfDict[word] = 0.0
        else:
            idfDict[word] = math.log10(N / float(val))
    return idfDict


def sim_measures_TF_IDF(dataframe):
    cos_sim_dict = {}
    dice_sim_dict = {}
    jacc_sim_dict = {}
    for_calc = list(dataframe)
    checkList = []
    for i in range(1, len(term_context_list)):
        temp = list(set(term_context_list[0]))
        for temp in for_calc:
            output = list(filter(lambda x: temp[0] in x, for_calc))
            temp2 = permutation(output)
            if temp2 not in checkList:
                checkList.append(temp2)
    perm_list = list(chain(*checkList))
    for i in range(1, len(term_context_list)):
        numer = 0
        for temp in perm_list:
            for elem in temp:
                numer = numer + (dataframe.loc[0].at[temp[0]] * dataframe.loc[i].at[elem] * (1 / (1 + Wagner_Fisher(temp[0][1], elem[1]))))
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

def Wagner_Fisher(contextA, contextB):
    tokenA = contextA.split("/")
    tokenB = contextB.split("/")
    M = len(tokenA)
    N = len(tokenB)

    Distance = [[None for i in range(N)] for i in range(M)]
    Distance[0][0] = costUpdWord(tokenA[0], tokenB[0])

    for i in range(1, M):
        Distance[i][0] = Distance[i - 1][0] + 1
    for j in range(1, N):
        Distance[0][j] = Distance[0][j - 1] + 1

    for i in range(1, M):
        for j in range(1, N):
            Distance[i][j] = min(
                Distance[i - 1][j - 1]
                + costUpdWord(tokenA[i], tokenB[j]),
                Distance[i - 1][j] + 1,
                Distance[i][j - 1] + 1,
            )
    return Distance[M - 1][N - 1]


def costUpdWord(A, B):
    if A == B:
        return 0
    else:
        return 1

def permutation(lst):

    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]

    l = []
    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1:]
        for p in permutation(remLst):
            l.append([m] + p)
    return l

