import xml.etree.ElementTree as ET
import src.features

tree = ET.parse('D:\\Degree@Mora\\Level4\\FYP\\Newfolder\\flaskApp\\src\\features\\dataNew.xml')
root = tree.getroot()

"""
def joining(tableList):
    #valDic={}
    global table1Pk
    join=''
    table1=tableList[0]
    table2=tableList[1]

    for table in root.findall('table'):
        tableName=table.get('name')
        table1Pk=''
        if tableName==table1:
            #valueDic = {}
            for column in table.findall('column'):
                #name=column.get('name')
                val1=column.get('value1')
                val2=column.get('value2')
                val='None'
                name1=''
                name1=column.get('name')
                if not val2: #if val 2:
                    continue
                else:
                    #val=val2
                    name2=column.get('name')
                    ref=column.get('ref')
                    if ref==table2:
                        for table in root.findall('table'):
                            tName=table.get('name')
                            if tName==table1:
                                for column in table.findall('column'):
                                    v1=column.get('value1')
                                    v2=column.get('value2')
                                    if v1 and not v2:
                                        table1Pk=column.get('name')

                        join=join+table1Pk+' = '+name2
                        print("join :",join)
    return join
                #valDic.update({name:value})

        #joinDic[tableName]=valDic
"""


def joining(tableList):
    if len(tableList) > 1:
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
                            table2Pk = table2Pk + column.get('name')
                            join = join + table1Pk + ' = ' + table2Pk
        if table2Pk == '':
            for tab in root.findall('table'):
                tabName = tab.get('name')
                if tabName == table2:
                    for col in tab.findall('column'):
                        colValue1 = col.get('value1')
                        colValue2 = col.get('value2')
                        if colValue2:
                            table2Pk = table2Pk + col.get('name')
                            join = join + table1Pk + ' = ' + table2Pk
    # print(join)
    else:
        join = ""
    return join


def join1(tableList):
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
                # if value1 and not value2:
                # table1Pk=table1Pk+column.get('name')
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
                    if col.get('ref'):
                        table2Pk = col.get('name')
                        join = join + table1Pk + ' = ' + table2Pk
    return join


# join1=join1(['department', 'employee'])
join2 = join1(['employee', 'employee'])
print("join1 :", join2)


# join2=joining(['location','department'])
# print("join :",join2)
# joining(['project','department'])

def conditionConcatenator(conditionAttributeList, operatorSymbolList, conditionValueList, concatenatingOperatorList,
                          join):
    length = len(conditionValueList)
    count = 0
    condition = ''
    if (not (
            not conditionAttributeList and not operatorSymbolList and conditionValueList and not concatenatingOperatorList and join)):
        while (count < length):
            attribute = conditionAttributeList[count]
            symbol = operatorSymbolList[count]
            value = conditionValueList[count]
            if (not (len(concatenatingOperatorList) == count)):
                concatenatingOperator = concatenatingOperatorList[count]
                condition = condition + attribute + symbol + value + ' ' + concatenatingOperator + ' '
            else:
                condition = condition + attribute + symbol + value
        count += 1
    if join:
        if condition == '':
            condition = condition + join
        else:
            condition = condition + ' and ' + join
        print("condition :", condition)
    return condition


def generateSqlQuery(attributeList, tableList, condition):
    sqlQuery=''
    if (attributeList and tableList and condition):
        # att_for_value = prv_attribute
        # sqlQuery = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList)+ " WHERE " + att_for_value[0] + symbol + value[0] + ";"
        sqlQuery = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList) + " WHERE " + condition + ";"
        #print("\n\nFinal SQL Query :", sqlQuery)

    if (attributeList and tableList and not condition):
        sqlQuery = "SELECT " + ','.join(attributeList) + " FROM " + ','.join(tableList) + ";"
        #print("\n\nFinal SQL Query :", sqlQuery)

    if (not attributeList and tableList and condition):
        # att_for_value = prv_attribute
        # sqlQuery = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList)+ " WHERE " + att_for_value[0] + symbol + value[0] + ";"
        sqlQuery = "SELECT * FROM " + ', '.join(tableList) + " WHERE " + condition + ";"
        #print("\n\nFinal SQL Query :", sqlQuery)

    if (not attributeList and not condition):
        sqlQuery = "SELECT * FROM " + ','.join(tableList) + ";"
        #print("\n\nFinal SQL Query :", sqlQuery)
    # print("basic sql",sqlQuery)
    return sqlQuery

    """

        if value and attributeList:
       # att_for_value = prv_attribute
       #att_for_value=condition_list
       basciSQL = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList) + " WHERE " + condition_list[0][0] + symbol[0][0] + value[0][0] + operator[0][0]+ " "+ condition_list[1] + symbol[1] + value[1] + ";"
    print("basic sql", basciSQL)
    return basciSQL

    if value and attributeList:
        att_for_value = prv_attribute
        basciSQL = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList)+ " WHERE " + att_for_value[0] + symbol[0] + value[0] + operator[0] +att_for_value[1] + symbol[1] + value[1]+ ";"
    print("basic sql",basciSQL)
    return sqlQuery;

    if value and len(condition_list) >= 2:
        basciSQL = "SELECT " + ', '.join(attributeList) + " FROM " + ', '.join(tableList)+ " WHERE " + condition_list[0][0] + condition_list[0][1] + value[0] + operator[0].upper() + " " +condition_list[1][0] + condition_list[1][1] + value[1] + ";"
        print(basciSQL)


    for a in condition_list and b in symbol and c in value:
        st="statement" + condition_list[a] + " " + symbol[b] + " " + value[c] + " "
        print(st)
"""
# generateSqlQuery(attributeList,tableList, condition_list, symbol, value,operator)