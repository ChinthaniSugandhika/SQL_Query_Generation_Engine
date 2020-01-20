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


def getAttributeNames(attributes, tabs, taggedList, tables):
    duplicateAttributeList = []
    attributeList = []
    keyWords = ['of', 'from']
    wordList = []
    words = []

    for word, tag in taggedList:
        words.append(word)
    count = 1
    tableIndex = 0
    while count < len(words):
        if words[count] in keyWords:
            tableIndex = tableIndex + count + 1
        count += 1
    count = 0
    while count < len(words):
        if words[count] in tabs and not (count == tableIndex):
            words.remove(words[count])
        count += 1
    posTaggedNounlist = nltk.pos_tag(words)
    nouns = preProcessor.extractAdjectivesAndNouns(posTaggedNounlist)

    if tableIndex==0:
        nounList=preProcessor.extractAdjectivesAndNouns(taggedList)
        attributeList=identifyAttributesOfReleventaTable(tabs,nounList)

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
            elif index2 in keyWords:
                keyWordIndex = wordList.index(index2)
            elif index3 in keyWords:
                keyWordIndex = wordList.index(index3)
            else:
                wordList.remove(word)
            for i in range(0, keyWordIndex - 1):  # issue in attribues identification keyWordIndex-1
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
    for noun in nouns:
        if noun == 'name':
            attributeList.append('first_name')
            attributeList.append('middle_name')
            attributeList.append('last_name')

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


tableList = []
attributeList = []


def identifyAttributesOfReleventaTable(identifiedTableNames, identifiedAttributeNames):
    employeeTable = ["number", "first_name", "middle_name", "last_name", "salary", "address", "gender", "date_of_birth",
                     "department_number", "supervisor"]
    projectTable = ["number", "name", "location", "department_number"]
    departmentTable = ["number", "name", "employee_number", "start_date"]
    dependentTable = ["dependent_number", "first_name", "gender", "date_of_birth", "relationship", "employee_number"]
    workTable = ["employee_number", "project_number", "hours_per_week"]
    locationTable = ["location", "department_number"]

    for attribute in identifiedAttributeNames:
        if attribute in employeeTable:
            tableName = "employee"
            if tableName in identifiedTableNames:
                tableList.append(tableName)
                attributeName = attribute
                attributeList.append(attributeName)
        if attribute in projectTable:
            tableName = "project"
            if tableName in identifiedTableNames:
                tableList.append(tableName)
                attributeName = attribute
                attributeList.append(attributeName)
        if attribute in departmentTable:
            tableName = "department"
            if tableName in identifiedTableNames:
                tableList.append(tableName)
                attributeName = attribute
                attributeList.append(attributeName)
        if attribute in dependentTable:
            tableName = "dependent"
            if tableName in identifiedTableNames:
                tableList.append(tableName)
                attributeName = attribute
                attributeList.append(attributeName)
        if attribute in workTable:
            tableName = "work"
            if tableName in identifiedTableNames:
                tableList.append("work")
                attributeName = attribute
                attributeList.append(attributeName)
        if attribute in locationTable:
            tableName = "location"
            if tableName in identifiedTableNames:
                tableList.append(tableName)
                attributeName = attribute
                attributeList.append(attributeName)
    print("tName :", tableList)
    print("attList :", attributeList)
    return attributeList

def identifyTablesOfTheRelevantAttribute(identifiedAttributeNames):
    employeeTable = ["number", "first_name", "middle_name", "last_name", "salary", "address", "gender", "date_of_birth",
                     "department_number", "supervisor"]
    projectTable = ["number", "name", "location", "department_number"]
    departmentTable = ["number", "name", "employee_number", "start_date"]
    dependentTable = ["dependent_number", "first_name", "gender", "date_of_birth", "relationship", "employee_number"]
    workTable = ["employee_number", "project_number", "hours_per_week"]
    locationTable = ["location", "department_number"]

    for attribute in identifiedAttributeNames:
        if attribute in employeeTable:
            tableName = "employee"
            tableList.append(tableName)
            attributeName = attribute
            attributeList.append(attributeName)
        if attribute in projectTable:
            tableName = "project"
            tableList.append(tableName)
            attributeName = attribute
            attributeList.append(attributeName)
        if attribute in departmentTable:
            tableName = "department"
            tableList.append(tableName)
            attributeName = attribute
            attributeList.append(attributeName)
        if attribute in dependentTable:
            tableName = "dependent"
            tableList.append(tableName)
            attributeName = attribute
            attributeList.append(attributeName)
        if attribute in workTable:
            tableName = "work"
            tableList.append(tableName)
            attributeName = attribute
            attributeList.append(attributeName)
        if attribute in locationTable:
            tableName = "location"
            tableList.append(tableName)
            attributeName = attribute
            attributeList.append(attributeName)
    print("tName :", tableList)
    print("attList :", attributeList)
    return tableList


def intermediateLayer(userInput):
    outputDic = {}
    tockens = preProcessor.tockenize(userInput)
    taggedWordList = preProcessor.posTagger(userInput)
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
    adjectiveAdverbNouns = preProcessor.extractAdjectivesAdverbsdNouns(taggedWordList)
    adverbs = preProcessor.extractAdverbs(taggedWordList)
    print("adverbs ", adverbs)
    adjectives = preProcessor.extractAdjectives(taggedWordList)
    print("adjectives ", adjectives)
    lemmatizedWords = preProcessor.lemmatizing(nounList)
    print("lemmatized Words :", lemmatizedWords)
    symbol = knowledgebase.operatorKnowledgeBase(adjectiveAdverbNouns, adverbs)
    print("Symbols :", symbol)
    tables = XmlExtractor.readTableNames()
    print("tables :", tables)
    attributes = XmlExtractor.readAttributeNames()
    tableNames = getTableNames(lemmatizedWords, tables)
    print("table names :", tableNames)
    join = queryGenerator.joining(tableNames)
    attributeNames = getAttributeNames(attributes, tableNames, lemmedText, tables)
    print("attribute Names :", attributeNames)
    identifyAttributesOfReleventaTable(tableNames, attributeNames)
    conditionAttributeName = preProcessor.extractConditionAttribute(adjectivesNouns, attributes, taggedWordList,
                                                                    attributeValues)
    if conditionAttributeName and not tableNames and not attributeNames:
        for conditionAttribute in conditionAttributeName:
            conditionAttributeNamesList = []
            conditionAttributeNamesList.append(conditionAttribute)
            tableNames = identifyTablesOfTheRelevantAttribute(conditionAttributeNamesList)
            # tableNames.append(tableName)
    if attributeNames and not tableNames:
        for attribute in attributeNames:
            attList = []
            attList.append(attribute)
            tableNames = identifyTablesOfTheRelevantAttribute(attList)

    print("condition Att :", conditionAttributeName)
    concatenatingOperator = preProcessor.extractConditionConcatenatingOperator(attributeValues,
                                                                               taggedWordList)
    print("concat", concatenatingOperator)
    adjectiveAttributeValueCondition = knowledgebase.attributeValueKnowledgeBase(adjectiveAdverbNouns)
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
