import xml.etree.ElementTree as ET

tree = ET.parse('D:\\Degree@Mora\\Level4\\FYP\\Newfolder\\flaskApp\\src\\features\\dataNew.xml')
root = tree.getroot()


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
                    if value2 and column.get('ref') == table2:
                        table2Pk = table2Pk + column.get('name')
                        join = join + table1Pk + ' = ' + table2Pk
        if table2Pk == '':
            for tab in root.findall('table'):
                tabName = tab.get('name')
                if tabName == table2:
                    for col in tab.findall('column'):
                        colValue2 = col.get('value2')
                        if colValue2:
                            table2Pk = table2Pk + col.get('name')
                            join = join + table1Pk + ' = ' + table2Pk
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
                value2 = column.get('value2')
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


join2 = join1(['employee', 'employee'])
print("join1 :", join2)


def conditionConcatenator(conditionAttributeList, operatorSymbolList, conditionValueList, concatenatingOperatorList,
                          join):
    length = len(conditionValueList)
    count = 0
    condition = ''
    if (not (
            not conditionAttributeList and not operatorSymbolList and conditionValueList and not concatenatingOperatorList and join)):
        while count < length:
            attribute = conditionAttributeList[count]
            symbol = operatorSymbolList[count]
            value = conditionValueList[count]
            if not (len(concatenatingOperatorList) == count):
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