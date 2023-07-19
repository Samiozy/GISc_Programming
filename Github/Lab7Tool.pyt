# -*- coding: utf-8 -*-

import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "My Second Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [RMITool_q1, RMI_Analysis]

#Question 1
        
class RMITool_q1(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Rank Mobility Index Tool"
        self.description = "The rank mobility index is a measure of an area's change in population rank among a group of areas"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = "Select a feature class", name = "inputfc", datatype = "DEFeatureClass", parameterType = "Required", direction = "Input")
        param1 = arcpy.Parameter(displayName = "Select the field to rank", name = "field", datatype = "Field", parameterType = "Required", direction = "Input")
        param1.parameterDependencies = [param0.name]
        param2 = arcpy.Parameter(displayName = "Specify Rank field name", name = "rankName", datatype = "GPString", parameterType = "Required", direction = "Input")
        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #create a new field for the ranking if not existing
        if not arcpy.ListFields(parameters[0].ValueAsText, parameters[2].ValueAsText):
            arcpy.AddField_management(parameters[0].ValueAsText, parameters[2].ValueAsText, "SHORT") # SHORT is for short interger

        #create a list of tuple containing the population values
        recList = []
        recNum = 0

        with arcpy.da.SearchCursor(parameters[0].ValueAsText, [parameters[1].ValueAsText]) as cursor:
            for row in cursor:
                recList.append([recNum, row[0], 0])
                recNum += 1
        sorted_recList = sorted(recList, key = lambda x:x[1], reverse = True) #sort the list based on the population values

        #add the rank value for each population
        rank = 1
        for aRec in sorted_recList:
            aRec[2] = rank
            rank += 1

        reg_recList = sorted(sorted_recList, key = lambda x:x[0]) #sort the list based on the index number

        #Use the update cursor to update the feature class with the rank values
        with arcpy.da.UpdateCursor(parameters[0].ValueAsText, [parameters[2].ValueAsText]) as rows:
            recNum = 0
            for row in rows:
                row[-1] = reg_recList[recNum][2]
                row[-1] = float(row[-1])
                recNum += 1
                rows.updateRow(row)
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
class RMI_Analysis(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "RMI Analysis Tool"
        self.description = "The rank mobility index is a measure of an area's change in population rank among a group of areas"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(displayName = "Select a feature class", name = "inputfc", datatype = "DEFeatureClass", parameterType = "Required", direction = "Input")
        param1 = arcpy.Parameter(displayName = "Select the 1st field to rank", name = "field1", datatype = "Field", parameterType = "Required", direction = "Input")
        param1.parameterDependencies = [param0.name]
        param2 = arcpy.Parameter(displayName = "Select the 2nd field to rank", name = "field2", datatype = "Field", parameterType = "Required", direction = "Input")
        param2.parameterDependencies = [param0.name]
        param3 = arcpy.Parameter(displayName = "Specify Rank field1 name", name = "rankName1", datatype = "GPString", parameterType = "Required", direction = "Input")
        param4 = arcpy.Parameter(displayName = "Specify Rank field2 name", name = "rankName2", datatype = "GPString", parameterType = "Required", direction = "Input")
        param5 = arcpy.Parameter(displayName = "RMI", name = "rank", datatype = "GPString", parameterType = "Required", direction = "Input")
        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        if not arcpy.ListFields(parameters[0].ValueAsText, parameters[3].ValueAsText):
            arcpy.AddField_management(parameters[0].ValueAsText, parameters[3].ValueAsText, "SHORT") # SHORT is for short interger
        if not arcpy.ListFields(parameters[0].ValueAsText, parameters[4].ValueAsText):
            arcpy.AddField_management(parameters[0].ValueAsText, parameters[4].ValueAsText, "SHORT") # SHORT is for short interger
        if not arcpy.ListFields(parameters[0].ValueAsText, parameters[5].ValueAsText):
            arcpy.AddField_management(parameters[0].ValueAsText, parameters[5].ValueAsText, "FLOAT","10","4") # SHORT is for short interger

        recList = []
        recNum = 0

        with arcpy.da.SearchCursor(parameters[0].ValueAsText, [parameters[1].ValueAsText, parameters[2].ValueAsText]) as cursor:
            for row in cursor:
                recList.append([recNum, row[0], row[1], 0, 0])
                recNum += 1
        sorted_recList = sorted(recList, key = lambda x:x[1], reverse = True)

        rank = 1
        for aRec in sorted_recList:
            aRec[3] = rank
            rank += 1

        #reg_recList = sorted(sorted_recList, key = lambda x:x[0])
        
        sorted_recList = sorted(sorted_recList, key = lambda x:x[2], reverse = True)

        rank = 1
        for aRec in sorted_recList:
            aRec[4] = rank
            rank += 1

        reg_recList = sorted(sorted_recList, key = lambda x:x[0])
        
        with arcpy.da.UpdateCursor(parameters[0].ValueAsText, [parameters[3].ValueAsText, parameters[4].ValueAsText, parameters[5].ValueAsText]) as rows:
            recNum = 0
            for row in rows:
                row[0] = reg_recList[recNum][3]
                row[1] = reg_recList[recNum][4]
                r1 = float(row[0])
                r2 = float(row[1])
                rmi = ((r1-r2)/(r1+r2))
                row[2] = rmi
                recNum += 1
                rows.updateRow(row)
        del row
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return