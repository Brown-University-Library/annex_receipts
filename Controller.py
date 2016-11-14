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

import datetime, getopt, logging, os, pprint, re, sys

## add project parent-directory to sys.path
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )

from annex_eod_project import settings
from annex_eod_project import FileHandler
# import DatePrepper
# import Emailer
# import FileHandler
# import NameConverter
# import Parser
# import Writer

logging.basicConfig(
    # filename=settings.LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( 'script started' )


fileHandlerInstance = FileHandler.FileHandler()


## perceive the arguments sent in
opts, args = getopt.getopt(sys.argv[1:], 'd')   # I don't remember what the 'd' is for; look it up someday.


class Controller( object ):

    def __init__( self ):
        log.debug( 'controller initialized' )
        self.sourceDir = settings.SOURCE_DIR
        self.archiveOrigDir = settings.ARCHIVE_ORIGINAL_DIR
        self.archiveParsedDir = settings.ARCHIVE_PARSED_DIR
        self.destinationDir = settings.DESTINATION_DIR
        self.prefixList = settings.PREFIX_LIST
        self.timeStamp = "init"
        self.filesFound = "init" # will be True or False
        self.email_message = ''

    def manageProcessing( self, args ):

        ## prepare the initial text indicating the script is running
        message = """
-------

Cron job starting at `{}`.
""".format( unicode(datetime.datetime.now()) )

        self.email_message = message
        log.info( message )

        #######
        # check for new files
        #######

        ## 'checking' notice
        message = 'Checking for new file(s).'
        self.email_message = '\n{}\n'.format( message )
        log.info( message )

        ## validate source-directory existence
        fileHandlerInstance = FileHandler.FileHandler()
        sourceDirectoryExistenceCheck = fileHandlerInstance.checkDirectoryExistence(self.sourceDir)
        if(sourceDirectoryExistenceCheck != "exists"):
            # self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            log.error( 'Error validating source-directory existence, ```{}```'.format(fileHandlerInstance.errorMessage) )
            self.endProgram()

        # check for files
        filesToExamineList = fileHandlerInstance.scanDirectory(self.sourceDir)
        goodFileList = fileHandlerInstance.makeGoodList(self.prefixList, filesToExamineList)
        if ( goodFileList == [] ):
            # self.log = writerInstance.appendText(self.log, "No files found.")
            log.info( 'No files found.' )
            self.endProgram()
        self.filesFound = True
        # self.log = writerInstance.appendText(self.log, "File(s) found.")
        message = 'File(s) found.'
        self.email_message = '\n{}\n'.format( message )
        log.info( message )

        #######
        # copy files to archive location
        #######

        # validate archiveOrig directory existence
        archiveDirectoryExistenceCheck = fileHandlerInstance.checkDirectoryExistence(self.archiveOrigDir)
        if(archiveDirectoryExistenceCheck != "exists"):
            # self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            log.error( 'Error validating archive-original-directory existence, ```{}```'.format(fileHandlerInstance.errorMessage) )
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
            # self.log = writerInstance.appendText(self.log, "ERROR: Couldn't copy found files to archive_orig directory. Halting program.")
            log.error( 'ERROR: Couldn\'t copy found files to archive_orig directory. Halting program.' )
            self.endProgram()

        #######
        # delete originals
        #######

        # delete files just saved from 'outbound'
        resultOfDeletion = fileHandlerInstance.deleteListFiles(goodFileList, self.sourceDir)
        if (resultOfDeletion != "success"):
            # self.log = writerInstance.appendText(self.log, "ERROR: Couldn't delete original files: " + fileHandlerInstance.errorMessage + " Halting program.")
            log.error( 'ERROR: Couldn\'t delete original files: ```{}```. Halting program.'.format(fileHandlerInstance.errorMessage) )
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
            # self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            log.error( 'Error validating archive-parsed-directory existence, ```{}```'.format(fileHandlerInstance.errorMessage) )
            self.endProgram()

        # make archiveParsed fileName dictionary
        archiveOriginalToArchiveParsedDictionary = nameConverterInstance.makeArchiveOrigToArchiveParsedDictionary(sourceToOriginalDictionary, self.timeStamp)

        #parse -- blank files not copied to archiveParse, fileName removed from 'archiveOriginalToArchiveParsedDictionary' below
        parserInstance = Parser.Parser()
        parseCheck = parserInstance.parseFileDictionary(self.archiveOrigDir, self.archiveParsedDir, archiveOriginalToArchiveParsedDictionary)
        if (parseCheck != "success"):
            # self.log = writerInstance.appendText(self.log, fileHandlerInstance.errorMessage)
            log.error( 'Error parsing file, ```{}```. Halting program.'.format(fileHandlerInstance.errorMessage) )
            self.endProgram()
        else:
            # self.log = writerInstance.appendText(self.log, "Files processed: " + parserInstance.statusMessage + ".")
            log.info( 'Files parsed: ```{}```.'.format(parserInstance.statusMessage) )

        archiveOriginalToArchiveParsedDictionary = parserInstance.nonEmptiesDictionary

        #######
        # copy parsed files to destination
        #######

        # get finalDestination dictionary prepared in the 'parse' step above (with blank files removed).
        archiveParsedToFinalDestinationDictionary = nameConverterInstance.prepareFinalDestinationDictionary(archiveOriginalToArchiveParsedDictionary, self.destinationDir)

        # copy to final destination
        finalFilecopyCheck = fileHandlerInstance.copyFileDictionary(archiveParsedToFinalDestinationDictionary, self.archiveParsedDir, self.destinationDir)
        if (finalFilecopyCheck != "success"):
            # self.log = writerInstance.appendText(self.log, "ERROR: Couldn't copy parsed files to '" + self.destinationDir + "'. Halting program.")
            log.error( 'Error copying file to final destination, ```{}```. Halting program.'.format(self.destinationDir) )
            self.endProgram()
        else:
            # self.log = writerInstance.appendText(self.log, "Files ready for Josiah: " + fileHandlerInstance.statusMessage + ".")
            message = 'Files ready for Josiah: ```{}```.'.format(fileHandlerInstance.statusMessage)
            self.email_message = '\n{}\n'.format( message )
            log.info( message )
            self.endProgram()



    def endProgram(self):
        writerInstance = Writer.Writer()
        endText = writerInstance.obtainEndText()
        # finalLog = writerInstance.appendText(self.log, endText)
        # print finalLog
        self.email_message = '\n{}\n'.format( endText )
        log.debug( 'ending program, ```{}```'.endText )
        # email notice if files found
        if(self.filesFound == True):
            emailerInstance = Emailer.Emailer()
            message = self.email_message
            emailerInstance.sendEmail(message)
        sys.exit()



if __name__ == "__main__":
    someClassInstance = Controller()
    someClassInstance.manageProcessing(args)



# bottom
