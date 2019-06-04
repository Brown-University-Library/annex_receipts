# -*- coding: utf-8 -*-

"""
Part of LAS-to-Josiah code.
Scan for existence of files.
"""

import datetime, logging, os, pprint, time

import requests
from . import settings
from annex_eod_project import FileHandler, NameConverter


log = logging.getLogger(__name__)


class Parser(object):

    def __init__(self):
        log.debug( 'parser initialized' )
        self.errorMessage = "init"
        self.statusMessage = "init"
        self.currentFileCount = "init"
        self.nonEmptiesDictionary = {}
        self.count_dct = {
            'date': str( datetime.date.today() ),
            'hay_accessions': 0,
            'hay_refiles': 0,
            'non_hay_accessions': 0,
            'non_hay_refiles': 0
        }

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

        self.build_count_dct( fullSourceFileName, recordCount )

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

        ## end parseSingleFile()

    def build_count_dct( self, source_filename: str, record_count: int ) -> None:
        """ Updates self.count_dct for post to annex_counts webapp.
            Called by parseSingleFile() """
        if 'qhacs' in source_filename.lower():
            self.count_dct['hay_accessions'] = record_count
        elif 'qhref' in source_filename.lower():
            self.count_dct['hay_refiles'] = record_count
        elif 'qsacs' in source_filename.lower():
            self.count_dct['non_hay_accessions'] = record_count
        elif 'qsref' in source_filename.lower():
            self.count_dct['non_hay_refiles'] = record_count
        else:
            log.warning( f"what's up with source_filename ```{source_filename}```?" )
        return

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
        log.debug( f'builtDict, ```{pprint.pformat(builtDict)}```' )

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

        ## post counts to annex_counts webapp
        self.post_counts()

        return returnValue

        ## end def parseFileDictionary()

    def post_counts( self ) -> None:
        """ Posts dct to annex_counts webapp.
            Called by parseFileDictionary() """
        log.debug( f'self.count_dct, ```{pprint.pformat(self.count_dct)}```' )
        self.count_dct['auth_key'] = settings.ANNEX_COUNTS_API_AUTHKEY
        seconds = 5
        try:
            r = requests.post( settings.ANNEX_COUNTS_API_UPDATER_URL, params=self.count_dct, timeout=10 )
        except Exception as e:
            log.warning( f'exception on annex-counts post, ```{str(e)}```; will try again in `{seconds}` seconds' )
            time.sleep( seconds )
            try:
                r = requests.post( settings.ANNEX_COUNTS_API_UPDATER_URL, params=self.count_dct, timeout=10 )
            except Exception as e:
                log.error( f'exception on annex-counts post, ```{str(e)}```' )
        log.debug( 'well that seemed to go well' )
        return

    ## end class Parser
