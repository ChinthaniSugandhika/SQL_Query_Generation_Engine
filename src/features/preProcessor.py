import xml.etree.ElementTree as ET
from builtins import print

tree = ET.parse('D:\\Degree@Mora\\Level4\\FYP\\Newfolder\\flaskApp\\src\\features\\dataNew.xml')
root = tree.getroot()


# def joining(tableList):
#     if len(tableList) > 1:
#         table1Pk = ''
#         table2Pk = ''
#         join = ''
#         table1 = tableList[0]
#         table2 = tableList[1]
#
#         for table in root.findall('table'):
#             tableName = table.get('name')
#             if tableName == table1:
#                 for column in table.findall('column'):
#                     value1 = column.get('value1')
#                     value2 = column.get('value2')
#                     if value1:
#                         table1Pk = table1Pk + column.get('name')
#                     if value2 and column.get('ref') == table2:
#                         table2Pk = table2Pk + column.get('name')
#                         join = join + table1Pk + ' = ' + table2Pk
#         if table2Pk == '':
#             for tab in root.findall('table'):
#                 tabName = tab.get('name')
#                 if tabName == table2:
#                     for col in tab.findall('column'):
#                         colValue2 = col.get('value2')
#                         if colValue2:
#                             table2Pk = table2Pk + col.get('name')
#                             join = join + table1Pk + ' = ' + table2Pk
#     else:
#         join = ""
#     return join

def joining(tableList):
   if (len(tableList)==2):
       return join2(tableList)
   #if (len(tableList) == 3):
       #return join3(tableList)

def join2(tableList):
    table1Pk = ''
    table2Pk = ''
    join = ''
    table1 = tableList[0]
    table2 = tableList[1]

    for table in root.findall('table'):
        tableName = table.get('name')
        if tableName == table1:
            for column in table.findall('column'):
                value1 = column.get('value1')
                value2 = column.get('value2')
                if value1:
                    table1Pk = table1Pk + column.get('name')
                if value2:
                    if column.get('ref') == table2:
                        table1Pk = ''
                        table1Pk = table1Pk + column.get('name')
                        for tab in root.findall('table'):
                            tabName = tab.get('name')
                            if tabName == table2:
                                for col in tab.findall('column'):
                                    if col.get('value1'):
                                        table2Pk = table2Pk + col.get('name')
                                        join = join + table1Pk + ' = ' + table2Pk
    if table2Pk == '':
        for tab in root.findall('table'):
            tabName = tab.get('name')
            if tabName == table2:
                for col in tab.findall('column'):
                    if col.get('ref') == table1:
                        table2Pk = col.get('name')
                        join = join + table1Pk + ' = ' + table2Pk
    return join





# print("join1 :", join2)

def join3(tableList):
    table1Pk = ''
    table2Pk = ''
    table3Pk = ''
    join = []
    joinString=''
    table1 = tableList[0]
    table2 = tableList[1]
    table3 = tableList[2]

    for table in root.findall('table'):
        tableName = table.get('name')
        if tableName == table1:
            for column in table.findall('column'):
                value1 = column.get('value1')
                value2 = column.get('value2')
                if value1:
                    table1Pk = table1Pk + column.get('name')
                if value2:
                    if column.get('ref') == table2:
                        table1Pk = ''
                        table1Pk = table1Pk + column.get('name')
                        for tab in root.findall('table'):
                            tabName = tab.get('name')
                            if tabName == table2:
                                for col in tab.findall('column'):
                                    if col.get('value1'):
                                        table2Pk = table2Pk + col.get('name')
                                        joinString = joinString + table1 + '.' + table1Pk + ' = ' + table2 + '.' + table2Pk
                                        join.append(joinString)

                    elif column.get('ref') == table3:
                        joinString=''
                        table1Pk = ''
                        table1Pk = table1Pk + column.get('name')
                        for tab in root.findall('table'):
                            tabName = tab.get('name')
                            if tabName == table3:
                                for col in tab.findall('column'):
                                    if col.get('value1'):
                                        table3Pk = table3Pk + col.get('name')
                                        joinString =joinString + table1 + '.' + table1Pk + ' = ' + table3 + '.' + table3Pk
                                        join.append(joinString)

    table1Pkv = ''
    table2Pkv = ''
    table3Pkv = ''
    joinString = ''
    table1v = tableList[0]
    table2v = tableList[1]
    table3v = tableList[2]
    for table in root.findall('table'):
        tableName = table.get('name')
        if tableName == table2v:
            for column in table.findall('column'):
                value1 = column.get('value1')
                value2 = column.get('value2')
                if value1:
                    table2Pkv = table2Pkv + column.get('name')
                if value2:
                    if column.get('ref') == table1v:
                        table2Pkv = ''
                        table2Pkv = table2Pkv + column.get('name')
                        for tab in root.findall('table'):
                            tabName = tab.get('name')
                            if tabName == table1v:
                                for col in tab.findall('column'):
                                    if col.get('value1'):
                                        table1Pkv = table1Pkv + col.get('name')
                                        joinString =joinString + table2v + '.' + table2Pkv + ' = ' + table1v + '.' + table1Pkv
                                        join.append(joinString)
                    elif column.get('ref') == table3v:
                        joinString=''
                        table2Pkv = ''
                        table2Pkv = table2Pkv + column.get('name')
                        for tab in root.findall('table'):
                            tabName = tab.get('name')
                            if tabName == table3v:
                                for col in tab.findall('column'):
                                    if col.get('value1'):
                                        table3Pkv = table3Pkv + col.get('name')
                                        joinString = joinString + table2v + '.' + table2Pkv + ' = ' + table3v + '.' + table3Pkv
                                        join.append(joinString)
    finalJoin=''
    finalJoin=finalJoin+join[0]+' AND '+join[1]
    return finalJoin


#y = joining(["location","department","project"])
#print("join 3 :", y)


def conditionConcatenator(conditionAttributeList, operatorSymbolList, conditionValueList, concatenatingOperatorList,
                          join):
    length = len(conditionValueList)
    count = 0
    condition = ''
    while count < length:
        attribute = conditionAttributeList[count]
        symbol = operatorSymbolList[count]
        value = conditionValueList[count]
        if not (len(concatenatingOperatorList) == count):
            concatenatingOperator = concatenatingOperatorList[count]
            condition = condition + attribute+' ' + symbol +' '+ value + ' ' + concatenatingOperator + ' '
        else:
            condition = condition + attribute+' ' + symbol +' '+ value
        count += 1
    if join:
        if condition == '':
            condition = condition + join
        else:
            condition = condition + ' and ' + join
        print("condition :", condition)
    return condition


def generateSqlQuery(attributeList, tableList, condition):
    sqlQuery = ''
    if attributeList and tableList and condition:
        sqlQuery = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList) + " WHERE " + condition + ";"

    if attributeList and tableList and not condition:
        sqlQuery = "SELECT " + ','.join(attributeList) + " FROM " + ','.join(tableList) + ";"

    if not attributeList and tableList and condition:
        sqlQuery = "SELECT * FROM " + ', '.join(tableList) + " WHERE " + condition + ";"

    if not attributeList and not condition:
        sqlQuery = "SELECT * FROM " + ','.join(tableList) + ";"
    return sqlQuery
