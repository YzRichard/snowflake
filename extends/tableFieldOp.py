# coding: utf-8
# 字段处理：添加、删除
import arcpy
import datetime


def FieldExists(TableName, FieldName):
    desc = arcpy.Describe(TableName)
    FieldName = FieldName.upper()
    for field in desc.fields:
        if field.Name.upper() == FieldName:
            return True
            break
    return False


class FieldOp(object):

    def __init__(self, input_table):
        self.input_table = input_table
        self._descTable()

    def add(self, fieldName, fieldType):
        return arcpy.AddField_management(self.input_table, fieldName, fieldType,
                                         "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    def delete(self, fieldName):
        return arcpy.DeleteField_management(self.input_table, [fieldName])

    def hasField(self, fieldName):
        fieldName = fieldName.upper()
        for field in self.tableDesc.fields:
            if field.Name.upper() == fieldName:
                return True
                break
        return False

    def assignDefault(self, fieldName, fieldType, defaultValue):
        code_block = ''
        # defaultValue type is string
        if fieldType.upper() == 'DATE':
            # 20210501
            expression = "datetime.datetime.strptime('{}', '%Y%m%d')".format(defaultValue)
            code_block = "import time"
            pass
        elif fieldType.upper() == 'DOUBLE':
            expression = "float({})".format(defaultValue)
            pass
        elif fieldType.upper() == 'LONG':
            expression = "int({})".format(defaultValue)
            pass
        elif fieldType.upper() == 'TEXT':
            expression = "str('{}')".format(defaultValue)

        if fieldType.upper() == 'ENTITY_ID':
            fieldType = 'TEXT'

        arcpy.AddMessage(self.input_table + " , " + fieldName + " , " + expression + " , " + code_block)
        arcpy.CalculateField_management(
            self.input_table, fieldName, expression, "PYTHON3",code_block)

    def getFieldType(self, fieldName):
        self._descTable()
        fieldName = fieldName.upper()
        for field in self.tableDesc.fields:
            if field.Name.upper() == fieldName:
                type = field.type
                if type == 'String':
                    type = 'text'
                elif type == 'Integer':
                    type = 'long'
                elif type == 'SmallInteger':
                    type = 'short'
                return type.upper()
                break
        return None

    def _descTable(self):
        self.tableDesc = arcpy.Describe(self.input_table)


if __name__ == '__main__':
    arcpy.env.workspace = r'D:\arcgis_pro_projects\yingzi\scratch.gdb'
    fileOp = FieldOp(
        'province')
    type = fileOp.assignDefault('tenant_id', 'DATE', '20210501')
    print(type)
