# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Scan for existence of files.
"""

# import logging, os, string
import logging, os
from annex_eod_project import FileHandler, NameConverter


log = logging.getLogger(__name__)


class Parser(object):

    def __init__(self):
        log.debug( 'parser initialized' )
        self.errorMessage = "init"
        self.statusMessage = "init"
        self.currentFileCount = "init"
        self.nonEmptiesDictionary = {}



    def parseSingleFile(self, fullSourceFileName, fullOutputFileName):

        sourceFileReference = open(fullSourceFileName, 'r')
        fileList = sourceFileReference.readlines()

        self.currentFileCount = "init"
        recordCount = 0
        for line in fileList:
            indexNumber = fileList.index(line)
            line = "n:" + line
            fileList[indexNumber] = line
            recordCount = recordCount + 1

        self.currentFileCount = "count-" + str(recordCount)

        if(recordCount > 0):
            # destinationText = string.join(fileList, '')
            destinationText = ''.join(fileList)
            destinationFileReference = open(fullOutputFileName, 'w')
            destinationFileReference.write(destinationText)
            destinationFileReference.close()

            # built-in check of ability to read just-written file
            parsedFileReference = open(fullOutputFileName, 'r')
            parsedLineList = parsedFileReference.readlines()

            if(parsedLineList == fileList):
                returnValue = "success"
            else:
                returnValue = "failure"
        else:
            returnValue = "success" # sort of cheating, but ok

        return returnValue



#   def parseFileDictionary(self, sourceDirectory, destinationDirectory, nameDictionary):
#
#       if (sourceDirectory.endswith("/") == False):
#           sourceDirectory = sourceDirectory + "/"
#       if (destinationDirectory.endswith("/") == False):
#           destinationDirectory = destinationDirectory + "/"
#
#       returnValue = "init"
#       filesParsed = ""
#
#       builtDict = {}
#       for sourceFileName in nameDictionary.keys():
#           fullSourceFileName = sourceDirectory + sourceFileName
#           fullDestinationFileName = destinationDirectory + nameDictionary[sourceFileName]
#           self.parseSingleFile(fullSourceFileName, fullDestinationFileName)
#
#           # update new dictionary
#           if(self.currentFileCount != "count-0"):
#               key = sourceFileName
#               value = nameDictionary[key]
#               builtDict[key] = value
#
#           nameConverterInstance = NameConverter.NameConverter()
#           fileName = nameConverterInstance.convertInputToOriginal(sourceFileName)
#
#           if(filesParsed == ""):
#               filesParsed = "\n" + "'" + fileName + "', " + self.currentFileCount + "\n"
#           else:
#               filesParsed = filesParsed + "'" + fileName + "', " + self.currentFileCount + "\n"
#
#       # update non-Empties dictionary
#       self.nonEmptiesDictionary = builtDict
#
#       # take off that final newline character
#       lengthOfFilesParsedString = len(filesParsed)
#       charactersToChopForFinalNewline = 1
#       charactersToKeep = lengthOfFilesParsedString - charactersToChopForFinalNewline
#       filesParsedString = filesParsed[:charactersToKeep]
#       self.statusMessage = filesParsedString
#
#       if(returnValue == "init"):
#           returnValue = "success"
#
#       return returnValue



    def parseFileDictionary(self, sourceDirectory, destinationDirectory, nameDictionary):

        if (sourceDirectory.endswith("/") == False):
            sourceDirectory = sourceDirectory + "/"
        if (destinationDirectory.endswith("/") == False):
            destinationDirectory = destinationDirectory + "/"

        returnValue = "init"
        filesParsed = ""

        builtDict = {}
        filesProcessedList = [] # for log/email
        for sourceFileName in nameDictionary.keys():
            fullSourceFileName = sourceDirectory + sourceFileName
            fullDestinationFileName = destinationDirectory + nameDictionary[sourceFileName]
            self.parseSingleFile(fullSourceFileName, fullDestinationFileName)

            # update new dictionary, eliminating files that have zero records
            if(self.currentFileCount != "count-0"):
                key = sourceFileName
                value = nameDictionary[key]
                builtDict[key] = value

            # build list for log/email
            nameConverterInstance = NameConverter.NameConverter()
            fileName = nameConverterInstance.convertInputToOriginal(sourceFileName)
            filesProcessedList.append("'" + fileName + "', " + self.currentFileCount)

        # sort and save filesProcessedList
        filesProcessedList.sort()
        # stringFromList = string.join(filesProcessedList, "\n")
        stringFromList = '\n'.join( filesProcessedList )
        filesProcessedString = "\n" + stringFromList
        self.statusMessage = filesProcessedString

        # update non-Empties dictionary
        self.nonEmptiesDictionary = builtDict

        if(returnValue == "init"):
            returnValue = "success"

        return returnValue





# bottom
