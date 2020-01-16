from src.features import mainCordinator
from src.features import reGenerateQuery

def generateSqlQuery(naturalQuery):
    mainCordinator.intermediateLayer(naturalQuery)
    try:
        finalSqlQuery=mainCordinator.intermediateLayer(naturalQuery)
    except BaseException as e:
        print("xxxxxxxxxxxxxxxxxxxx", e)
        return e
    print("inside",finalSqlQuery)
    return finalSqlQuery

def regenarteSqlQuery(table_List, attribute_List, join_List, condition_List):
    tableList=[]
    attributeList=[]
    joinList=[]
    conditionList=[]
    if table_List:
        tableList.append(table_List)
    if attribute_List:
        attributeList.append(attribute_List)
    if join_List:
        joinList.append(join_List)
    if condition_List:
        conditionList.append(condition_List)
    try:
        sqlQuery_new = reGenerateQuery.reGenereateQuery(tableList, attributeList, joinList, conditionList)
    except BaseException as e:
        print("yyyyyyyyyyyyyyyy", e)
        return e
    return sqlQuery_new

#i want in number , first name , address of the employee whose department is HR
