# -*- coding: utf-8 -*-
# 指定源代码文件的编码格式
# 为图层生成唯一id，如果没有字段则自动生成
# 如果字段有值则跳过，填充没有值的字段

import arcpy
import sys
import os
import traceback
from extends import SnowFlake
from extends import tableFieldOp


# Script arguments
Input_table = arcpy.GetParameterAsText(0)  # 输入图层
# Input_table = r'D:\arcgis_pro_projects\yingzi\publicdata.gdb\public_basicdata\building_public'

Target_field = arcpy.GetParameterAsText(1)  # 关联图层对应存储的字段
# Target_field = 'entity_id'

if Target_field == '':
    Target_field = 'ID'



def createEntityId(tableName, fieldName, whereClause=''):
    worker = SnowFlake.IdWorker(0, 0)

    # worker.get_id()
    # Execute CalculateField
    with arcpy.da.UpdateCursor(tableName, fieldName, where_clause=whereClause) as cursor:
        for row in cursor:
            row[0] = str(worker.get_id())
            cursor.updateRow(row)

try:
    inputTableOp = tableFieldOp.FieldOp(Input_table)
    if inputTableOp.hasField(Target_field) is not True:
        inputTableOp.add(Target_field, 'TEXT')
    createEntityId(Input_table, Target_field, "{} IS NULL or {} = ''".format(Target_field, Target_field))

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + \
        tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    # Return python error messages for use in script tool or Python window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    # Print Python error messages for use in Python / Python window
    print(pymsg)
    print(msgs)
