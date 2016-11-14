# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Manage the flow of LAS-to-Josiah info.

ok- echo 'starting script'
ok- echo 'checking for output'

if output found...
ok- echo 'new file found'
notNeeded- prepare datestampstring
ok- copy original to archives / update tempText
ok- delete original / update tempText
ok- parse file / update tempText
ok- write parsed file out to archives / upate tempText
ok- copy parsed file to destination / update tempText
- email parsed file ready / update tempText
ok- echo 'end script'

if output non found...
ok- echo 'no file found'
"""

import getopt, logging, os, pprint, re, sys

## add project directory to sys.path
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )

from annex_eod_project import settings
import ArgumentReader
import DatePrepper
import Emailer
import FileHandler
import NameConverter
import Parser
import Writer

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( 'script started' )


1/0


# perceive the arguments sent in
opts, args = getopt.getopt(sys.argv[1:], 'd')   # I don't remember what the 'd' is for; look it up someday.



class Controller:



    log = "init"
    sourceDir = "init"
    archiveOrigDir = "init"
    archiveParsedDir = "init"
    destinationDir = "init"
    prefixList = ["QSACS","QSREF","QHACS", "QHREF"]
    timeStamp = "init"
    filesFound = "init" # true or false



    def manageProcessing(self, args):

        print '- in Controller.py, manageProcessing(); starting'

        # prepare the initial text indicating the script is running
        writerInstance = Writer.Writer()
        self.log = writerInstance.obtainStartText()

        # capture and validate the arguments passed by the cron job to Controller (sourceDirectory, archiveDirectory, destinationDirectory)
        argReaderInstance = ArgumentReader.ArgumentReader()
        argCheck = argReaderInstance.ensureNumberOfArgs(args)

        if(argCheck != "valid"):

            self.log = writerInstance.appendText(self.log, " ")
            self.log = writerInstance.appendText(self.log, argReaderInstance.errorMessage)
            self.endProgram()

        #######
        # capture args
        #######

        self.sourceDir = args[0]
        self.archiveOrigDir = args[1]
        self.archiveParsedDir = args[2]
        self.destinationDir = args[3]

        #######
        # check for new files
        #######

        # 'checking' notice
        self.log = writerInstance.appendText(self.log, " ")
        self.log = writerInstance.appendText(self.log, "Checking for new file(s).")

        # validate source-directory existence
        fileHandlerInstance = FileHandler.FileHandler()
        sourceDirectoryExistenceCheck = fileHandlerInstance.checkDirectoryExistence(self.sourceDir)
        if(sourceDirectoryExistenceCheck != "exists"):
            self.log = writerInstance.appendText(self.log, " ")
            self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            self.endProgram()

        # check for files
        filesToExamineList = fileHandlerInstance.scanDirectory(self.sourceDir)
        goodFileList = fileHandlerInstance.makeGoodList(self.prefixList, filesToExamineList)
        self.log = writerInstance.appendText(self.log, " ")
        if ( goodFileList == [] ):
            self.log = writerInstance.appendText(self.log, "No files found.")
            self.endProgram()
        self.filesFound = True
        self.log = writerInstance.appendText(self.log, "File(s) found.")

        #######
        # copy files to archive location
        #######

        # validate archiveOrig directory existence
        archiveDirectoryExistenceCheck = fileHandlerInstance.checkDirectoryExistence(self.archiveOrigDir)
        if(archiveDirectoryExistenceCheck != "exists"):
            self.log = writerInstance.appendText(self.log, " ")
            self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            self.endProgram()

        # make archiveOrig fileName dictionary
        datePrepperInstance = DatePrepper.DatePrepper()
        timeStamp = datePrepperInstance.prepareTimeStamp()
        self.timeStamp = timeStamp
        nameConverterInstance = NameConverter.NameConverter()
        sourceToOriginalDictionary = nameConverterInstance.makeTrueOrigToArchiveOrigDictionary(goodFileList, self.timeStamp)

        # copy files to archiveOrig
        fileCopyCheck = fileHandlerInstance.copyFileDictionary(sourceToOriginalDictionary, self.sourceDir, self.archiveOrigDir)
        if (fileCopyCheck != "success"):
            self.log = writerInstance.appendText(self.log, " ")
            self.log = writerInstance.appendText(self.log, "ERROR: Couldn't copy found files to archive_orig directory. Halting program.")
            self.endProgram()

        #######
        # delete originals
        #######

        # delete files just saved from 'outbound'
        resultOfDeletion = fileHandlerInstance.deleteListFiles(goodFileList, self.sourceDir)
        if (resultOfDeletion != "success"):
            self.log = writerInstance.appendText(self.log, " ")
            self.log = writerInstance.appendText(self.log, "ERROR: Couldn't delete original files: " + fileHandlerInstance.errorMessage + " Halting program.")
            self.endProgram()

        # delete count files
        countFileList = fileHandlerInstance.makeCountFileList(self.sourceDir, self.prefixList)
        fileHandlerInstance.deleteListFiles(countFileList, self.sourceDir)

        #######
        # parse files
        #######

        # validate archiveParsed directory existence
        archiveDirectoryExistenceCheck = fileHandlerInstance.checkDirectoryExistence(self.archiveParsedDir)
        if(archiveDirectoryExistenceCheck != "exists"):
            self.log = writerInstance.appendText(self.log, " ")
            self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            self.endProgram()

        # make archiveParsed fileName dictionary
        archiveOriginalToArchiveParsedDictionary = nameConverterInstance.makeArchiveOrigToArchiveParsedDictionary(sourceToOriginalDictionary, self.timeStamp)

        #parse -- blank files not copied to archiveParse, fileName removed from 'archiveOriginalToArchiveParsedDictionary' below
        parserInstance = Parser.Parser()
        parseCheck = parserInstance.parseFileDictionary(self.archiveOrigDir, self.archiveParsedDir, archiveOriginalToArchiveParsedDictionary)
        self.log = writerInstance.appendText(self.log, " ")
        if (parseCheck != "success"):
            self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            self.endProgram()
        else:
            self.log = writerInstance.appendText(self.log, "Files processed: " + parserInstance.statusMessage + ".")

        archiveOriginalToArchiveParsedDictionary = parserInstance.nonEmptiesDictionary

        #######
        # copy parsed files to destination
        #######

        # get finalDestination dictionary prepared in the 'parse' step above (with blank files removed).
        archiveParsedToFinalDestinationDictionary = nameConverterInstance.prepareFinalDestinationDictionary(archiveOriginalToArchiveParsedDictionary, self.destinationDir)

        # copy to final destination
        finalFilecopyCheck = fileHandlerInstance.copyFileDictionary(archiveParsedToFinalDestinationDictionary, self.archiveParsedDir, self.destinationDir)
        self.log = writerInstance.appendText(self.log, " ")
        if (finalFilecopyCheck != "success"):
            self.log = writerInstance.appendText(self.log, "ERROR: Couldn't copy parsed files to '" + self.destinationDir + "'. Halting program.")
            self.endProgram()
        else:
            self.log = writerInstance.appendText(self.log, "Files ready for Josiah: " + fileHandlerInstance.statusMessage + ".")
            self.endProgram()



    def endProgram(self):
        writerInstance = Writer.Writer()
        endText = writerInstance.obtainEndText()
        finalLog = writerInstance.appendText(self.log, endText)
        print finalLog
        # email notice if files found
        if(self.filesFound == True):
            emailerInstance = Emailer.Emailer()
            message = finalLog
            emailerInstance.sendEmail(message)
        import sys
        sys.exit()



if __name__ == "__main__":
    someClassInstance = Controller()
    someClassInstance.manageProcessing(args)



# bottom
