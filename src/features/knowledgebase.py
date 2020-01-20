import nltk

nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
from src.features import preProcessor
import re


def createKnowledgeBase(listType, itemsList):
    knowledgeBase = []
    if listType == 'table':
        table_list = itemsList
        for table in table_list:
            kbFile = open("table_knowledgebase_file", "w+")
            syns = wordnet.synsets(table, pos='n')[0]
            kbFile.write(str([table, syns]))
            kbFile.write("\n")
            knowledgeBase.append([table, syns])
    if listType == 'attribute':
        attributeList = itemsList
        for attribute in attributeList:
            if re.search(r'_', attribute):
                knowledgeBase.append(attribute)
            else:
                kbFile = open("table_knowledgebase_file", "w+")
                syns = wordnet.synsets(attribute, pos='n')[0]
                kbFile.write(str([attribute, syns]))
                kbFile.write("\n")
                knowledgeBase.append([attribute, syns])
    return knowledgeBase


def operatorKnowledgeBase(nouns, adverbs):
    symbolList = []
    greaterThanList = ['greater', 'bigger', 'higher', 'great', 'more','above', 'over']
    lesserThanList = ['lesser', 'smaller', 'lower', 'less']
    equalList = ['equal', 'equals', 'same','is', 'in']
    for noun in nouns:
        if noun in equalList:
            if len(adverbs) > 0:
                for adverb in adverbs:
                    if adverb == 'not':
                        symbol = '<>'
                        symbolList.append(symbol)
            else:
                symbol = '='
                symbolList.append(symbol)
        else:
            if noun in greaterThanList:
                symbol = '>'
                symbolList.append(symbol)
            if noun in lesserThanList:
                symbol = '<'
                symbolList.append(symbol)
            if noun in equalList and noun in lesserThanList:
                symbol = '<='
                symbolList.append(symbol)
            if noun in equalList and noun in greaterThanList:
                symbol = '>='
                symbolList.append(symbol)
    return symbolList


def attributeValueKnowledgeBase(tockens):
    dic = {'female': 'gender', 'male': 'gender', 'HR': 'name'}
    femaleList=['woman', 'women']
    maleList=['men','man']
    conditionList = []
    for key, value in dic.items():
        for tocken in tockens:
            s1Lemmas = set(wordnet.all_lemma_names())
            lemmatizedTocken=preProcessor.lemmatizeSingleWord(tocken)
            if key in s1Lemmas and lemmatizedTocken in s1Lemmas:
                s1 = wn.synsets(lemmatizedTocken)[0]
                s2 = wn.synsets(key)[0]
                sim = s1.wup_similarity(s2)
                if sim is None:
                    continue
                elif sim >= 0.9:
                    conditionList.append(value + '=' + '"' + key + '"')
                elif lemmatizedTocken in femaleList and key=='female':
                    conditionList.append(value + '=' + '"' + key + '"')
                elif lemmatizedTocken in maleList and key=='male':
                    conditionList.append(value + '=' + '"' + key + '"')
                else:
                    continue

    length = len(conditionList)
    count = 0
    c = 1
    condition = ''
    while count < length:
        con = conditionList[count]
        if not (len(conditionList) == c):
            condition = condition + con + ' and '
        else:
            condition = condition + con
        count += 1
        c += 1
    return condition

attributeValueKnowledgeBase(['men','male','woman','female'])