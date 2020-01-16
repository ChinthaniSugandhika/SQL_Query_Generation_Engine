def reGenereateQuery(tableList, attributeList,joinList,conditionList,):
    whereClause=generateCondition(conditionList,joinList)
    sqlQuery = ''
    if (attributeList and tableList and conditionList):
        sqlQuery = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList) + " WHERE " + whereClause + ";"

    if (attributeList and tableList and not conditionList):
        sqlQuery = "SELECT " + ','.join(attributeList) + " FROM " + ','.join(tableList) + ";"

    if (not attributeList and tableList and conditionList):
        sqlQuery = "SELECT * FROM " + ', '.join(tableList) + " WHERE " + whereClause + ";"

    if (not attributeList and not conditionList):
        sqlQuery = "SELECT * FROM " + ','.join(tableList) + ";"
    print("\n\nFinal SQL Query :", sqlQuery)
    return sqlQuery

def generateCondition(conditionList,joinList):
    newCondition = ''
    length = len(conditionList)
    conCatLength = length - 1
    count = 0
    while (count < length):
        con = conditionList[count]
        if (not (conCatLength == count)):
            newCondition = newCondition + con + ' and '
        else:
            newCondition = newCondition + con
        count = count + 1
    print("new con :", newCondition)
    length = len(joinList)
    conCatLength = length - 1
    count = 0
    if joinList:
        if newCondition != '':
            newCondition = newCondition + ' and '
            while (count < length):
                join = joinList[count]
                if (not (conCatLength == count)):
                    newCondition = newCondition + join + ' and '
                else:
                    newCondition = newCondition + join
                count = count + 1
        else:
            while (count < length):
                join = joinList[count]
                if (not (conCatLength == count)):
                    newCondition = newCondition + join + ' and '
                else:
                    newCondition = newCondition + join
                count = count + 1

    print("new con :", newCondition)
    return newCondition
