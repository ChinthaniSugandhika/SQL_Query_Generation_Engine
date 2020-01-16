import  nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
import re

#create kKowledge Base which contains synonyms for table names and attribute names
def createKnowledgeBase(listType, list):
    knowledgeBase = []
    if listType == 'table':
        table_list = list
        for table in table_list:
            kbFile = open("table_knowledgebase_file", "w+")
            syns = wordnet.synsets(table, pos='n')[0]
            #lemmas = syns.lemmas()
            #print(len(lemmas))
            #print([lemma.name() for lemma in syns.lemmas()])
            kbFile.write(str([table, syns]))
            kbFile.write("\n")
            knowledgeBase.append([table, syns])
    if listType == 'attribute':
        attributeList = list
        for attribute in attributeList:
            if(re.search(r'\_', attribute)):
                knowledgeBase.append(attribute)
            else:
                kbFile = open("table_knowledgebase_file", "w+")
                syns = wordnet.synsets(attribute, pos='n')[0]
                #print([lemma.name() for lemma in syns.lemmas()])
                kbFile.write(str([attribute, syns]))
                kbFile.write("\n")
                knowledgeBase.append([attribute, syns])
    return knowledgeBase

def operatorKnowledgeBase(nouns,adverbs):
    symbolList = []
    symbol = ''
    greaterThanList=['greater', 'bigger', 'higher', 'great', 'more']
    lesserThanList = ['lesser', 'smaller', 'lower', 'less']
    equalList=['equal', 'equals', 'same']
    for noun in nouns:
        if(noun in equalList):
            if(len(adverbs)>0):
                for adverb in adverbs:
                    if(adverb=='not'):
                        symbol = '<>'
                        symbolList.append(symbol)
            else:
                symbol='='
                symbolList.append(symbol)
        else:
            if(noun in greaterThanList):
                symbol='>'
                symbolList.append(symbol)
            if (noun in lesserThanList):
                symbol = '<'
                symbolList.append(symbol)
            if (noun in equalList and noun in lesserThanList):
                symbol = '<='
                symbolList.append(symbol)
            if (noun in equalList and noun in greaterThanList):
                symbol = '>='
                symbolList.append(symbol)
    return symbolList

def attributeValueKnowledgeBase(adjectivesList):
    dic={'female':'gender','male':'gender','HR':'name'}
    conditionList=[]
    for key,value in dic.items():
        if key in adjectivesList:
            conditionList.append(value+'='+'"'+key+'"')

    length = len(conditionList)
    count = 0
    c=1
    condition = ''
    while (count < length):
        con = conditionList[count]
        symbol = 'and'
        if (not (len(conditionList) == c)):
            #concatenatingOperator = concatenatingOperatorList[count]
            condition = condition+ con + ' and '
        else:
            condition = condition+con
        count += 1
        c+=1
    #print("attributeValueCondition :")
    return condition

#ss=attributeValueKnowledgeBase(['first_name', 'female', 'higher','HR'],['female','HR'])
#print('attKB :',ss)




#knowledgebase1=createKnowledgeBase('attribute',['department_num', 'location'])
#'number', 'name', 'relationship', 'first_name', 'gender', 'date_of_birth', 'employee_number', 'dependent_number', 'employee_number', 'number', 'name', 'start_date', 'location', 'department_number', 'employee_number', 'project_number', 'hours_per_week', 'supervisor', 'gender', 'number', 'first_name', 'middle_name', 'date_of_birth', 'address', 'salary', 'departmnet_number', 'last_name'])
#print(knowledgebase1)


#createKnowledgeBase('att',['name','id'])
#print(knowledgebase1)

"""

syns = wordnet.synsets("program")
print(syns[0].name())
print(syns[0].lemmas()[0].name())
print(syns[0].definition())
print(syns[0].examples())

"""