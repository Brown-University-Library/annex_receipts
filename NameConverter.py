# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Convert names.
"""



import FileHandler



class NameConverter:



	def makeTrueOrigToArchiveOrigDictionary(self, inputList, timeStamp):

		builtDict = {}
		for fileName in inputList:
			key = fileName
			import string
			underscorePosition = string.find(fileName, "_")
			rootSlice = fileName[:underscorePosition]
			value = "ORIG_" + rootSlice + "_" + timeStamp + ".dat"
			builtDict[key] = value

		return builtDict



	def makeArchiveOrigToArchiveParsedDictionary(self, inputDictionary, timeStamp):

		builtDict = {}
		for fileName in inputDictionary.values(): # the value in the incoming dictionary becomes the key in this built dictionary
			key = fileName
			rootSlice = fileName[5:10]
			value = "PARSED_" + rootSlice + "_" + timeStamp + ".dat"
			builtDict[key] = value

		return builtDict



#	def makeArchiveOrigToArchiveParsedDictionary(self, inputDictionary, timeStamp, archiveOrigDirectory):
#
#		builtDict = {}
#
#		for fileName in inputDictionary.values(): # inputDictionary is like {"QHACS_0615.txt":"ORIG_QHACS_2005-06-15T13-41-39.dat"}
#			# check to see if file is empty. if so, don't include it in output dictionary.
#			fullFilePath = archiveOrigDirectory + fileName
#			fileReference = open(fullFilePath, "r")
#			firstLine = fileReference.readline()
#			if( len(firstLine) > 0 ):
#				key = fileName
#				rootSlice = fileName[5:10]
#				value = "PARSED_" + rootSlice + "_" + timeStamp + ".dat"
#				builtDict[key] = value
#
#		return builtDict



	def convertInputToOriginal(self, inputFileName):

		if(inputFileName[:4] == "ORIG"):
			root = inputFileName[5:10]
			month = inputFileName[16:18]
			day = inputFileName[19:21]
			returnValue = root + "_" + month + day + ".txt"
		elif(inputFileName[:4] == "PARS"):
			root = inputFileName[7:12]
			month = inputFileName[18:20]
			day = inputFileName[21:23]
			returnValue = root + "_" + month + day + ".txt"
		else:
			returnValue = inputFileName

		return returnValue



	def makeSameNameDictionary(self, inputList):

		builtDict = {}
		for fileName in inputList:
			key = fileName
			value = fileName
			builtDict[key] = value

		return builtDict



#	def prepareFinalDestinationDictionary(self, archiveOriginalToArchiveParsedDictionary):
#
#		builtDict = {}
#		for parsedFileName in archiveOriginalToArchiveParsedDictionary.values():
#			key = parsedFileName
#
#			root = parsedFileName[7:12]
#			month = parsedFileName[18:20]
#			day = parsedFileName[21:23]
#
#			value = root + "_" + month + day + ".txt"
#			builtDict[key] = value
#
#		return builtDict



#	def prepareFinalDestinationDictionary(self, archiveOriginalToArchiveParsedDictionary):
#
#		builtDict = {}
#		for parsedFileName in archiveOriginalToArchiveParsedDictionary.values():
#			key = parsedFileName
#
#			root = parsedFileName[7:12]
#			import string
#			root = string.lower(root)
#
#			month = parsedFileName[18:20]
#			day = parsedFileName[21:23]
#
#			value = root + month + day + ".txt"
#			builtDict[key] = value
#
#		return builtDict




	def prepareFinalDestinationDictionary(self, archiveOriginalToArchiveParsedDictionary, destinationDirectory):
		'''
		- Takes the most recently used dictionary (with references to empty files removed) and creates the new dictionary for
		copying the parsed files to their final destination.
		- Also checks for pre-existing files, and if found, appends a suffix to the file name to prevent overwriting.
		'''
		builtDict = {}
		for parsedFileName in archiveOriginalToArchiveParsedDictionary.values():

			key = parsedFileName # destinationFileName in inputDictionary becomes sourceFileName in outputDictionary

			root = parsedFileName[7:12]
			import string
			root = string.lower(root)

			month = parsedFileName[18:20]
			day = parsedFileName[21:23]

			basicCreatedName = root + month + day + ".txt" # this will be the destinationFileName *if* the file doesn't already exist.

			# check for existence of pre-existing files with same root name.
#				Remember, I'm iterating through a list now.
#				The logic is that I start a loop, take my basicCreatedName and look for a match anywhere in the destinationDirectory.
#				If no match, I'm golden (add to new dict), but if there is a match, add a suffix_number to the basicCreatedName and
#				check again for a match in the destinationDirectory.

			fileHandlerInstance = FileHandler.FileHandler()
			destinationFileList = fileHandlerInstance.scanDirectory(destinationDirectory)

			hopefulFinalName = basicCreatedName
			suffixNumeral = 1
			flag = "continue"
			sanityCheck = 0
			while ( (flag == "continue") & (sanityCheck < 1000) ):
				sanityCheck = sanityCheck + 1 # no endless loops while developing

				comparisonResult = "initialize"
				for existingFileName in destinationFileList:
					if (existingFileName == hopefulFinalName):
						comparisonResult = "matchFound"

				if (comparisonResult == "initialize"):
					realFinalName = hopefulFinalName
					flag = "stop"
				else: # life is trickier
					suffixNumeral = suffixNumeral + 1
					hopefulFinalName = basicCreatedName + "_" + str(suffixNumeral)

			# overwrite check done, new destination file name ready; update dictionary
			builtDict[key] = realFinalName

		return builtDict



# bottom
