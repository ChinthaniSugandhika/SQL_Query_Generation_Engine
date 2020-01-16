import nltk

from nltk.corpus import wordnet
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

from src.features import preProcessor
from src.features import knowledgebase
from src.features import XmlExtractor
from src.features import queryGenerator
#from src.features import
#import queryGenerator
#import GUIQueryGeneration

#create Knowledge Base
#tableSynset=knowledgebase.createKnowledgeBase('table', XmlExtractor.readTableNames())
#attributeSynset=knowledgebase.createKnowledgeBase('attribute', XmlExtractor.readAttributeNames())
#print("TableSynset: ",tableSynset)
#print("AttributeSynset", attributeSynset)

def getTableNames(nouns, tables):
    tableList=[]
    duplicateTableList=[]
    for noun in nouns:
        for table in tables:
            if(noun==table):
                tableList.append(table)
                #nouns.remove(noun)
            else:
                s1Lemmas = set(wordnet.all_lemma_names())
                if (table in s1Lemmas and noun in s1Lemmas):
                    #print("true")
                    s1 = wn.synsets(table)[0]
                    s2 = wn.synsets(noun)[0]
                    sim = s1.wup_similarity(s2)
                    if sim >= 0.8:
                        tableList.append(table)
                        #nouns.remove(noun)

    for x in tableList:
        if x not in duplicateTableList:
            duplicateTableList.append(x)
    return duplicateTableList

def getAttributeNames(nouns,attributes,tabs, taggedList,tables): #tables
    """
    attributeList=[]
    pdt=''
    #duplicateTableList=[]
    duplicateAttributeList=[]
    keyWords=['of','from']
    #attributeList=[]
    wordList=[]
    for word,tag in taggedList:
        if(tag=='PDT'):
            pdt=word
        wordList.append(word)
    #if()
    for word in wordList:
        #if(word==pdt and pdt=='all'):
            #return duplicateAttributeList
        if(word in tables):
            index=wordList.index(word)
            if(wordList[index-1] in keyWords):
                #if word==pdt and pdt=='all':
                    #return
                for i in range(0,index-1):
                    #n=nouns[i]
                    for attribute in attributes:
                        if(nouns[i]==attribute):
                            attributeList.append(nouns[i])
                        #else:
                            #s1Lemmas = set(wordnet.all_lemma_names())
                            #if(n in s1Lemmas and attribute in s1Lemmas):
                                    #print("true")
                                #s1 = wn.synsets(n)[0]
                                #s2 = wn.synsets(attribute)[0]
                                #sim = s1.wup_similarity(s2)
                                #if sim >= 0.8:
                                 #   attributeList.append(attribute)
    for x in attributeList:
        if x not in duplicateAttributeList:
            duplicateAttributeList.append(x)
    return duplicateAttributeList
    #for noun in nouns:
       # for attribute in attributes:
            #if(noun==attribute):
                #if (noun in attributeList):
                    #continue
                #attributeList.append(attribute)
    #return attributeList

"""
    duplicateAttributeList=[]
    attributeList=[]
    keyWords=['of','from']
    pdt=''
    wordList=[]
    for word,tag in taggedList:
        lemtedWord=preProcessor.lemmatizeSingleWord(word)
        tName=getTableName(lemtedWord,tables) #tables
        if tName:
            wordList.append(tName)
        elif(tag=='PDT' and word=='all'):
            return
        else:
            wordList.append(word)
    for word in wordList:
        if(word in tabs): #tables
            keyWordIndex=0
            index=wordList.index(word)
            index1=wordList[index-1]
            index2=wordList[index-2]
            index3=wordList[index-3]
            if index1 in keyWords:
                keyWordIndex=wordList.index(index1)
            if index2 in keyWords:
                keyWordIndex=wordList.index(index2)
            if index3 in keyWords:
                keyWordIndex=wordList.index(index3)
            #if(index1 in keyWords or index2 in keyWords or index3 in keyWords):
            for i in range(0,keyWordIndex-1):
                n=nouns[i]
                lemmedn=preProcessor.lemmatizeSingleWord(n)
                        #for attribute in attributes:
                if(nouns[i] in attributes):
                    attributeList.append(nouns[i])
                else:
                    for att in attributes:
                        s1Lemmas = set(wordnet.all_lemma_names())
                        if(att in s1Lemmas and lemmedn in s1Lemmas):
                            print("true")
                            s1 = wn.synsets(lemmedn)[0]
                            s2 = wn.synsets(att)[0]
                            sim = s1.wup_similarity(s2)
                            if sim >= 0.8:
                                attributeList.append(att)
    for x in attributeList:
        if x not in duplicateAttributeList:
            duplicateAttributeList.append(x)
    return duplicateAttributeList

def getTableName(word,tables):
    tableList=''
    for table in tables:
        if (word == table):
            tableList=table
                # nouns.remove(noun)
        else:
            s1Lemmas = set(wordnet.all_lemma_names())
            if (table in s1Lemmas and word in s1Lemmas):
                # print("true")
                s1 = wn.synsets(table)[0]
                s2 = wn.synsets(word)[0]
                sim = s1.wup_similarity(s2)
                if sim==None:
                    return
                elif sim>=0.8:
                    tableList = table
                else:
                    return
                        # nouns.remove(noun)

    return tableList

#userInput=("i want in number , first name , address of the employee whose department is HR")


#can you give me employee names who earn salary more than 40000
#"i'm interested in number , first name , address of the employee whose department is HR"


def intermediateLayer(userInput):
    """
        filterdText=preProcessor.removeStopWords(taggedWordList)
        print('filterdText :',filterdText)
        lemmedText=preProcessor.lemmatizing(filterdText)
        print('lemmedText :',lemmedText)

        attValues = preProcessor.extractIntegerValues(taggedWordList)
        print("att value: ", attValues)

        adjectivesNouns = preProcessor.extractAdjectivesAndNouns(taggedWordList)  # filterdSentence
        print("adjectives ", adjectivesNouns)

        adverbs = preProcessor.extractAdverbs(taggedWordList)
        print("adverbs ", adverbs)

        adjectives = preProcessor.extractAdjectives(taggedWordList)
        print("adjectives ", adjectives)

        symbol = knowledgebase.operatorKnowledgeBase(adjectivesNouns, adverbs)
        print("Symbols :", symbol)

        tables = XmlExtractor.readTableNames()
        print("tables :", tables)

        attributes = XmlExtractor.readAttributeNames()

        tableNames = getTableNames(lemmedText, tables)
        print("table names :", tableNames)

        join = queryGenerator.joining(tableNames)

        attributeNames = getAttributeNames(adjectivesNouns, attributes, tableNames, taggedWordList, lemmedText,tables)
        print("attribute Names :", attributeNames)

        conditionAttributeName = preProcessor.extractConditionAttribute(adjectivesNouns, attributes, taggedWordList)
        print("condition Att :", conditionAttributeName)
"""
    outputDic={}
    taggedWordList = preProcessor.tockenize(userInput)
    filterdSentence = preProcessor.removeStopWords(taggedWordList)
    print("filtered :", filterdSentence)

    lemmedText = preProcessor.lemmatizing2(filterdSentence) #
    print('lemmedText :', lemmedText)

    nounList = preProcessor.extractNouns(taggedWordList)  # filterdSentence
    print("nouns :", nounList)

    attributeValues = preProcessor.extractIntegerValues(taggedWordList)
    print("att value: ", attributeValues)

    adjectivesNouns = preProcessor.extractAdjectivesAndNouns(taggedWordList)  # filterdSentence
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

    concatenatingOperator = preProcessor.extractConditionConcatenatingOperator(nounList, attributeValues,
                                                                               taggedWordList)
    print("concat", concatenatingOperator)
    # process natural language query

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

    intermediateStatement= "SELECT " + ','.join(attributeNames) + " FROM " + ','.join(tableNames) + ' WHERE ' + finalCondition +";"
    print("intermediateStatement",intermediateStatement)

    finalQuery=queryGenerator.generateSqlQuery(attributeNames, tableNames, finalCondition)
    outputDic['query']=finalQuery
    outputDic['tables'] =tableNames
    outputDic['attributes'] = attributeNames
    outputDic['conditions'] = finalCondition

    print(outputDic)
    return outputDic



#x=intermediateLayer(userInput)



