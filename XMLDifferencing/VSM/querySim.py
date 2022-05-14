import xml.etree.ElementTree as ET
import os
from simProcessing_XML import parse
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from simProcessing_TXT import parse_txt
import re

lem = WordNetLemmatizer()
toRemove = stopwords.words('english')
indexDict = {}
ranking = {}
filtered_nestedDocs = []
filtered_Docs = []
arr = os.listdir("corpus")
for i in range(len(arr)):
    arr[i] = "corpus/" + arr[i]

def filter(query):
    filteredDocs = filteringDocs(query)
    return filteredDocs



def rank_no_filter(query, flag):
    cos_sim = {}
    dice_sim = {}
    jacc_sim = {}
    if query[0] == "<":
        with open("query.xml", "w") as f:
            f.write(query)
        arr.insert(0, "query.xml")
        cos_sim, dice_sim, jacc_sim = parse(arr, flag)
    elif os.path.isfile(query):
        if query.endswith('.xml'):
            arr.insert(0, query)
            cos_sim, dice_sim, jacc_sim = parse(arr, flag)
        elif query.endswith('.txt'):
            arr.insert(0, query)
            cos_sim, dice_sim, jacc_sim = parse_txt(arr, flag)
    else:
        with open("query.txt", "w") as f:
            f.write(query)
        arr.insert(0, "query.txt")
        cos_sim, dice_sim, jacc_sim = parse_txt(arr, flag)
    for i in range(1, len(arr)):
        cos_sim[arr[i]] = cos_sim.pop(i)
        dice_sim[arr[i]] = dice_sim.pop(i)
        jacc_sim[arr[i]] = jacc_sim.pop(i)
    arr.pop(0)
    return cos_sim, dice_sim, jacc_sim

def rank_filter(query, flag):
    cos_sim = {}
    dice_sim = {}
    jacc_sim = {}
    if query[0] == "<":
        with open("query.xml", "w") as f:
            f.write(query)
        filteredDocs = filter("query.xml")
        filteredDocs.sort()
        filteredDocs.insert(0, "query.xml")
        cos_sim, dice_sim, jacc_sim = parse(filteredDocs, flag)
    elif os.path.isfile(query):
        if query.endswith('.xml'):
            filteredDocs = filter(query)
            filteredDocs.sort()

            filteredDocs.insert(0, query)
            cos_sim, dice_sim, jacc_sim = parse(filteredDocs, flag)
        elif query.endswith('.txt'):
            filteredDocs = filter(query)
            filteredDocs.sort()
            filteredDocs.insert(0, query)
            cos_sim, dice_sim, jacc_sim = parse_txt(filteredDocs, flag)
    else:
        with open("query1.txt", "w") as f:
            f.write(query)
        filteredDocs = filter("query1.txt")
        filteredDocs.sort()
        filteredDocs.insert(0, "query1.txt")
        cos_sim, dice_sim, jacc_sim = parse_txt(filteredDocs, flag)
    for i in range(1, len(filteredDocs)):
        cos_sim[filteredDocs[i]] = cos_sim.pop(i)
        dice_sim[filteredDocs[i]] = dice_sim.pop(i)
        jacc_sim[filteredDocs[i]] = jacc_sim.pop(i)
    filteredDocs.pop(0)
    return cos_sim, dice_sim, jacc_sim



def indexing(listOfDocs):
    for doc in listOfDocs:
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
                    if word in indexDict.keys():
                        listA = indexDict[word]
                        if doc not in listA:
                            listA.append(doc)
                        indexDict[word] = listA
                    else:
                        indexDict[word] = [doc]
        indexingChild(root, doc)


def indexingChild(root, document):
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
                    if word in indexDict.keys():
                        listA = indexDict[word]
                        if document not in listA:
                            listA.append(document)
                        indexDict[word] = listA
                    else:
                        indexDict[word] = [document]
        indexingChild(child, document)


def filteringDocs(queryFile):
    global filtered_Docs
    global filtered_nestedDocs
    if queryFile.endswith(".xml"):
        tree = ET.parse(queryFile)
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
                    if word in indexDict.keys():
                        filtered_nestedDocs.append(indexDict[word])
        filteringChild(root)
    elif queryFile.endswith(".txt"):
        f = open(queryFile, "r")
        text = f.read()
        text_list = re.split("\s|(?<!\d)[,.](?!\d)", text)
        for elem in text_list:
            if elem == "":
                text_list.remove(elem)

        for word in text_list:
            if lem.lemmatize(word.lower()) not in toRemove:
                word_temp = word
                word = lem.lemmatize(word.lower(), pos="v")
                if word_temp is not word:
                    word = lem.lemmatize(word.lower(), pos="n")
                    word_temp = word
                if word_temp is not word:
                    word = lem.lemmatize(word.lower(), pos="a")
                if word in indexDict.keys():
                    filtered_nestedDocs.append(indexDict[word])
    extract_nested_lists(filtered_nestedDocs)
    filtered_Docs = list(set(filtered_Docs))
    return filtered_Docs
def filteringChild(root):
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
                    if word in indexDict.keys():
                        filtered_nestedDocs.append(indexDict[word])
        filteringChild(child)

def extract_nested_lists(nested_list):
    for element in nested_list:
        if isinstance(element, list):
            extract_nested_lists(element)
        else:
            filtered_Docs.append(element)

indexing(arr)
print(indexDict)

