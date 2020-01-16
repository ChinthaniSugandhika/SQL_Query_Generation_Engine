import xml
import xml.etree.ElementTree as ET


tree = ET.parse('D:\\Degree@Mora\\Level4\\FYP\\Newfolder\\flaskApp\\src\\features\\dataNew.xml')
root = tree.getroot()

tableInfoDic={}



#Reads the xml file and stores table names, attribute names and attribute values in a dictionary
for table in root.findall('table'):
    tableName=table.get('name')
    #tableList.append(tableName)
    valueDic = {}
    for column in table.findall('column'):
        name=column.get('name')
        value1=column.get('value1')
        value2=column.get('value2')
        value='None'
        if value1:
            value=value1
        if value2:
            value=value2
            reference=column.get('ref')
        valueDic.update({name:value})

    tableInfoDic[tableName]=valueDic



#Reads the keys(table names) from a dictinary and stores in a list
def readTableNames():
    tableList = []
    for key,value in tableInfoDic.items():
        tempKey = key
        tableList.append(tempKey)
    print("tables :",tableList)
    return tableList

#def createAttributeListsForTables():
   # numberOfTables=tableList.count()
   # for table in tableList:
       # tempDic={}
       # tempDic[table]=

#Reads the keys(attribute names) in dictionary inside another dictionary and converts it into a list
def readAttributeNames():
    attributeList = []
    duplicateAttributeList = []
    for key, value in tableInfoDic.items():
        #tempKey= key
        tempValue = value
        tempDic=tempValue
        for key1 in tempDic.keys():
            attributeList.append(key1)
    #print("attributes", attributeList)
    for x in attributeList:
        if x not in duplicateAttributeList:
            duplicateAttributeList.append(x)
    return duplicateAttributeList

print("table names :", readTableNames())
print("attribute names :",readAttributeNames())