import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from src.features import preProcessor
from src.features import knowledgebase
from src.features import XmlExtractor
from src.features import queryGenerator


def getTableNames(nouns, tables):
    tableList = []
    duplicateTableList = []
    for noun in nouns:
        for table in tables:
            if noun == table:
                tableList.append(table)
            else:
                s1Lemmas = set(wordnet.all_lemma_names())
                if table in s1Lemmas and noun in s1Lemmas:
                    s1 = wn.synsets(table)[0]
                    s2 = wn.synsets(noun)[0]
                    sim = s1.wup_similarity(s2)
                    if sim >= 0.8:
                        tableList.append(table)
    for x in tableList:
        if x not in duplicateTableList:
            duplicateTableList.append(x)
    return duplicateTableList


def getAttributeNames(nouns, attributes, tabs, taggedList, tables):
    duplicateAttributeList = []
    attributeList = []
    keyWords = ['of', 'from']
    wordList = []
    for word, tag in taggedList:
        lemtedWord = preProcessor.lemmatizeSingleWord(word)
        tName = getTableName(lemtedWord, tables)
        if tName:
            wordList.append(tName)
        elif tag == 'PDT' and word == 'all':
            return
        else:
            wordList.append(word)
    for word in wordList:
        if word in tabs:
            keyWordIndex = 0
            index = wordList.index(word)
            index1 = wordList[index - 1]
            index2 = wordList[index - 2]
            index3 = wordList[index - 3]
            if index1 in keyWords:
                keyWordIndex = wordList.index(index1)
            if index2 in keyWords:
                keyWordIndex = wordList.index(index2)
            if index3 in keyWords:
                keyWordIndex = wordList.index(index3)
            for i in range(0, keyWordIndex - 1):      #issue in attribues identification
                n = nouns[i]
                lemmedn = preProcessor.lemmatizeSingleWord(n)
                if nouns[i] in attributes:
                    attributeList.append(nouns[i])
                else:
                    for att in attributes:
                        s1Lemmas = set(wordnet.all_lemma_names())
                        if att in s1Lemmas and lemmedn in s1Lemmas:
                            s1 = wn.synsets(lemmedn)[0]
                            s2 = wn.synsets(att)[0]
                            sim = s1.wup_similarity(s2)
                            if sim >= 0.8:
                                attributeList.append(att)
    for x in attributeList:
        if x not in duplicateAttributeList:
            duplicateAttributeList.append(x)
    return duplicateAttributeList


def getTableName(word, tables):
    tableList = ''
    for table in tables:
        if word == table:
            tableList = table
        else:
            s1Lemmas = set(wordnet.all_lemma_names())
            if table in s1Lemmas and word in s1Lemmas:
                s1 = wn.synsets(table)[0]
                s2 = wn.synsets(word)[0]
                sim = s1.wup_similarity(s2)
                if sim is None:
                    return
                elif sim >= 0.8:
                    tableList = table
                else:
                    return

    return tableList


def intermediateLayer(userInput):
    outputDic = {}
    taggedWordList = preProcessor.tockenize(userInput)
    filterdSentence = preProcessor.removeStopWords(taggedWordList)
    print("filtered :", filterdSentence)
    lemmedText = preProcessor.lemmatizing2(filterdSentence)
    print('lemmedText :', lemmedText)
    nounList = preProcessor.extractNouns(taggedWordList)
    print("nouns :", nounList)
    attributeValues = preProcessor.extractIntegerValues(taggedWordList)
    print("att value: ", attributeValues)
    adjectivesNouns = preProcessor.extractAdjectivesAndNouns(taggedWordList)
    print("adjectives ", adjectivesNouns)
    adverbs = preProcessor.extractAdverbs(taggedWordList)
    print("adverbs ", adverbs)
    adjectives = preProcessor.extractAdjectives(taggedWordList)
    print("adjectives ", adjectives)
    lemmatizedWords = preProcessor.lemmatizing(nounList)
    print("lemmatized Words :", lemmatizedWords)
    symbol = knowledgebase.operatorKnowledgeBase(adjectivesNouns, adverbs)
    print("Symbols :", symbol)
    tables = XmlExtractor.readTableNames()
    print("tables :", tables)
    attributes = XmlExtractor.readAttributeNames()
    tableNames = getTableNames(lemmatizedWords, tables)
    print("table names :", tableNames)
    join = queryGenerator.joining(tableNames)
    attributeNames = getAttributeNames(adjectivesNouns, attributes, tableNames, lemmedText, tables)
    print("attribute Names :", attributeNames)
    conditionAttributeName = preProcessor.extractConditionAttribute(adjectivesNouns, attributes, taggedWordList)
    print("condition Att :", conditionAttributeName)
    concatenatingOperator = preProcessor.extractConditionConcatenatingOperator(attributeValues,
                                                                               taggedWordList)
    print("concat", concatenatingOperator)
    adjectiveAttributeValueCondition = knowledgebase.attributeValueKnowledgeBase(adjectives)
    print("adjectiveAttributeValueCondition : ", adjectiveAttributeValueCondition)
    condition = queryGenerator.conditionConcatenator(conditionAttributeName, symbol, attributeValues,
                                                     concatenatingOperator, join)
    print("concat condition :", condition)
    finalCondition = ''
    if condition and adjectiveAttributeValueCondition:
        finalCondition = finalCondition + condition + ' and ' + adjectiveAttributeValueCondition
    if not condition and adjectiveAttributeValueCondition:
        finalCondition = finalCondition + adjectiveAttributeValueCondition
    if condition and not finalCondition:
        finalCondition = finalCondition + condition
    intermediateStatement = "SELECT " + ','.join(attributeNames) + " FROM " + ','.join(
        tableNames) + ' WHERE ' + finalCondition + ";"
    print("intermediateStatement", intermediateStatement)
    finalQuery = queryGenerator.generateSqlQuery(attributeNames, tableNames, finalCondition)
    outputDic['query'] = finalQuery
    outputDic['tables'] = tableNames
    outputDic['attributes'] = attributeNames
    outputDic['conditions'] = finalCondition
    return outputDic