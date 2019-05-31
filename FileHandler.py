# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Scan for existence of files.
"""

import logging, os, pprint, shutil, string, time


log = logging.getLogger(__name__)


class FileHandler( object ):

    def __init__( self ):
        self.errorMessage = "init"
        self.statusMessage = "init"

    def checkDirectoryExistence(self, directory):
        """ Confirms path.
            Called by controller. """
        if ( os.path.exists(directory) ):
            returnValue = "exists"
        else:
            returnValue = "doesNotExist"
            self.errorMessage = "The directory '" + directory + "' does not exist."
        # log.debug( 'existence-check for dir `{dir}` has returnValue, `{val}`'.format(dir=directory, val=returnValue) )
        log.debug( 'existence-check for dir `%s` has returnValue, `%s`' % (directory, returnValue) )
        return returnValue

    def scanDirectory( self, directory ):
        """ Lists files.
            Called by controller. """
        if (directory.endswith("/") == False):
            directory = directory + "/"
        fileList = os.listdir(directory)
        # log.debug( 'fileList, ```{}```'.format(pprint.pformat(fileList)) )
        log.debug( 'fileList, ```%s```' % pprint.pformat(fileList) )
        ## 1) eliminate .DS_Store & 2) eliminate directories
        newFileList = []
        for fileName in fileList:
            if(fileName == ".DS_Store"):
                pass
            else:
                subdirectoryName = directory + fileName
                if( os.path.isdir(subdirectoryName) ):
                    pass
                else:
                    newFileList.append(fileName)
        # log.debug( 'scan-dir newFileList for directory, `{dirZ}` is, ```{lstZ}```'.format(dirZ=directory, lstZ=pprint.pformat(newFileList)) )
        log.debug( 'scan-dir newFileList for directory, `%s` is, ```%s```' % (directory, pprint.pformat(newFileList)) )
        return newFileList



    def makeGoodList(self, prefixList, fileList):

        newList = []

        for prefix in prefixList:
            for fileName in fileList:
                positionOfPrefix = str.find( fileName, prefix )   # haystack, needle. Will be -1 if not found
                positionOfCountIndicator = str.find(fileName, ".cnt")
#               if ( (1 == 1) & (2==2) ):
#                   print "do something"
                if ( (positionOfPrefix != -1) & (positionOfCountIndicator == -1) ): # if (prefixes exist AND '.cnt' substring doesn't)
                    newList.append(fileName)

        newList.sort() # don't need to do this for the production code, but it makes the test easier.
        return newList



    def copyFile(self, sourceFullPath, destinationFullPath):

        # import shutil
        shutil.copyfile(sourceFullPath, destinationFullPath)

        postCopyExistenceCheck = self.checkFileExistence(destinationFullPath)
        if (postCopyExistenceCheck == "exists"):
            returnValue = "success"
        else:
            returnValue = "failure"

        return returnValue



    def checkFileExistence(self, fullFilePath):

        try:
            file = open(fullFilePath)
        except:
            returnValue = "doesNotExist"
            # import os.path
            fileName=os.path.basename(fullFilePath)
            self.errorMessage = fileName
        else:
            returnValue = "exists"

        return returnValue



    def deleteDirectoryFiles(self, directory):

        if (directory.endswith("/") == False):
            directory = directory + "/"

        log.debug( 'about to call scanDirectory()' )
        fileList = self.scanDirectory(directory)

        # import os
        for fileName in fileList:
            fullFileName = directory + fileName
            os.remove(fullFileName)

        log.debug( 'about to call scanDirectory()' )
        newFileList = self.scanDirectory(directory)
        if ( newFileList == [] ):
            returnValue = "success"
        else:
            returnValue = "failure"

        return returnValue



    def copyFileDictionary(self, fileDictionary, sourceDirectory, destinationDirectory):

        # print '- in copyFileDictionary(); starting'
        log.debug( 'starting copyFileDictionary()' )

        if (sourceDirectory.endswith("/") == False):
            sourceDirectory = sourceDirectory + "/"
        if (destinationDirectory.endswith("/") == False):
            destinationDirectory = destinationDirectory + "/"

        for sourceFileName in fileDictionary.keys():

            fullSourceFileName = sourceDirectory + sourceFileName
            fullDestinationFileName = destinationDirectory + fileDictionary[sourceFileName]

            # log.debug( 'current directory, ```{}```'.format(os.getcwd()) )
            log.debug( 'current directory, ```%s```' % os.getcwd() )
            # log.debug( 'fullSourceFileName, ```{src}```; fullDestinationFileName, ```{dst}```'.format(src=fullSourceFileName, dst=fullDestinationFileName) )
            log.debug( 'fullSourceFileName, ```%s```; fullDestinationFileName, ```%s```' % (fullSourceFileName, fullDestinationFileName) )
            shutil.copy(fullSourceFileName, fullDestinationFileName)
            log.debug( 'copied ok' )

        # verify success and build listing of files ready for log & email
            # (first update destination directory to ensure it has a full-path instead of a relative-path)
        # import os
        fullDestinationDirectory = os.path.abspath(destinationDirectory) + "/" # fine if destinationDirectory is already complete

        returnValue = "init"
        filesCopiedList = []
        for destinationFileName in fileDictionary.values():
            try:
                fullFilePath = fullDestinationDirectory + destinationFileName
                file = open(fullFilePath)
            except:
                returnValue = "failure"
                break
            else:
                filesCopiedList.append("'" + fullFilePath + "'")

        # filesCopiedList.sort()
        # stringFromList = string.join(filesCopiedList, '\n')
        # filesCopiedString = "\n" + stringFromList
        # self.statusMessage = filesCopiedString

        filesCopiedList.sort()
        log.debug( f'filesCopiedList, ```{pprint.pformat(filesCopiedList)}```' )
        # stringFromList = string.join(filesCopiedList, '\n')
        stringFromList = '\n'.join( filesCopiedList )
        log.debug( f'stringFromList, ```{stringFromList}```' )
        filesCopiedString = "\n" + stringFromList
        self.statusMessage = filesCopiedString

        if(returnValue == 'init'):
            returnValue = 'success'
        return returnValue


    ## 2016-Nov-16: doesn't look like this function's used; delete after 2016-Dec-16
    # def makeFilesToParseList(self, fileList):
    #     for fileName in fileList:
    #         indexNumber = fileList.index(fileName)
    #         fileName = "archive_" + fileName
    #         fileList[indexNumber] = fileName
    #     return fileList



    def deleteListFiles(self, fileList, directory):

        # delete
        # import os
        for fileName in fileList:
            fullFileName = directory + fileName
            os.remove(fullFileName)

        # verification
        returnValue = "init"
        log.debug( 'about to call scanDirectory()' )
        filesStillInDirectory = self.scanDirectory(directory)

        for newFileName in filesStillInDirectory:
            try:
                indexTest = filesStillInDirectory.index(fileName) # returns an index number if originalFileName (fileName) is in newFileList (filesStillInDirectory -- it should *not* be.
                returnValue = "failure" # if we're here it means that the old file name is still here after the deletion code.
                self.errorMessage = "Unable to delete original file '" + fileName + "'."
                break
            except:
                pass

        if(returnValue == "init"):
            returnValue = "success"

        return returnValue



    def makeCountFileList(self, directory, prefixList):

        log.debug( 'about to call scanDirectory()' )
        initialList = self.scanDirectory(directory)
        newList = []

        for fileName in initialList:

            for prefix in prefixList:
                positionOfPrefix = string.find( fileName, prefix )   # haystack, needle. Will be -1 if not found
                positionOfCountIndicator = string.find(fileName, ".cnt")
                if ( (positionOfPrefix != -1) & (positionOfCountIndicator != -1) ): # if (prefix exists AND '.cnt' substring exists)
                    newList.append(fileName)
                    break

        newList.sort()
        return newList



# bottom
