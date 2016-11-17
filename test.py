# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, logging, os, pprint, sys, time, unittest
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )
from annex_eod_project import settings
from annex_eod_project.DatePrepper import DatePrepper
from annex_eod_project.Emailer import Emailer
from annex_eod_project.FileHandler import FileHandler
from annex_eod_project.NameConverter import NameConverter

""" To run tests:
    - activate v-env
    - cd into annex_eod_project dir
    - All tests...
      python ./test.py
    - Single test, eg:
      python ./test.py DatePrepper_Test.test__prepareTimeStamp """


lvl_dct = { 'D': logging.DEBUG, 'I': logging.INFO, 'E': logging.ERROR }
logging.basicConfig(
    filename=settings.LOG_PATH,
    level=lvl_dct[ settings.LOG_LEVEL ],
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


class DatePrepper_Test(unittest.TestCase):
    """ Tests DatePrepper.py code. """

    def setUp(self):
        self.dt_prppr = DatePrepper()

    def test__prepareTimeStamp(self):
        """ Tests returned date. """
        self.dt_prppr.timeToFormat = (2005, 7, 13, 13, 41, 39, 2, 194, 1) # 'Wed Jul 13 13:41:39 EDT 2005'
        self.assertEquals(
            unicode, type(self.dt_prppr.prepareTimeStamp())
            )
        self.assertEquals(
            '2005-07-13T13-41-39', self.dt_prppr.prepareTimeStamp()
            )

    # end class DatePrepper_Test


class Emailer_Test(unittest.TestCase):
    """ Tests Emailer.py code. """

    def setUp(self):
        self.emlr = Emailer()

    def test__update_full_message(self):
        """ Tests full message. """
        result = self.emlr.update_full_message( 'hello world' )
        self.assertEquals( unicode, type(result) )
        lines = result.split( '\n' )
        # log.debug( 'lines, ```{}```'.format(pprint.pformat(lines)) )
        log.debug( 'lines, ```%s```' % pprint.pformat(lines) )
        self.assertEquals( True, 'To:' in lines[0] )
        self.assertEquals( True, settings.MAIL_HEADERTO in lines[0] )
        self.assertEquals( True, 'Cc:' in lines[1] )
        self.assertEquals( True, settings.MAIL_HEADERCC in lines[1] )
        self.assertEquals( True, 'From:' in lines[2] )
        self.assertEquals( True, settings.MAIL_HEADERFROM in lines[2] )
        self.assertEquals( settings.MAIL_SUBJECT, lines[3] )
        self.assertEquals( 'hello world', lines[4] )

    # end class Emailer_Test


class FileHandler_Test(unittest.TestCase):
    """ Tests FileHandler.py code. """

    def setUp(self):
        self.flhndlr = FileHandler()

    def test__scanDirectory(self):
        """ Tests list of files returned. """
        cwd = os.path.abspath( os.getcwd() )
        # log.debug( 'cwd, ```{}```'.format(cwd) )
        log.debug( 'cwd, ```%s```' % cwd )
        result = self.flhndlr.scanDirectory( cwd )
        self.assertEquals( list, type(result) )
        self.assertEquals( True, '.DS_Store' not in result )  # cleaned file
        self.assertEquals( True, '.git' not in result )  # directories removed

    def test__makeGoodList(self):
        """ Tests filter for valid data-file from file-list. """
        prefix_list = settings.PREFIX_LIST  # Our list of prefix codes indicate whether the end-of-day reports are for re-accessions or returns, and whether they're for general, or restricted circulation items.
        file_list = [ 'a.txt', 'a.cnt', 'b.txt', 'b.cnt', 'QSREF.txt', 'QSREF.cnt' ]
        self.assertEquals(
            ['QSREF.txt'], self.flhndlr.makeGoodList( prefix_list, file_list )
            )

    # end class FileHandler_Test


class NameConverter_Test(unittest.TestCase):
    """ Tests NameConverter.py code. """

    def setUp(self):
        self.nmcnvrtr = NameConverter()

    def test_makeTrueOrigToArchiveOrigDictionary(self):
        """ Tests adding timestamp and prefix to original filename. """
        formatted_time = unicode( time.strftime(
            '%Y-%m-%dT%H-%M-%S', (2005, 7, 13, 13, 41, 39, 2, 194, 1)) )  # u'Wed Jul 13 13:41:39 EDT 2005'
        file_list = [ 'QHACS_1110.txt', 'QHREF_1110.txt' ]
        self.assertEquals(
            {u'QHACS_1110.txt': u'ORIG_QHACS_2005-07-13T13-41-39.dat', u'QHREF_1110.txt': u'ORIG_QHREF_2005-07-13T13-41-39.dat'},
            self.nmcnvrtr.makeTrueOrigToArchiveOrigDictionary(file_list, formatted_time) )

    def test_makeArchiveOrigToArchiveParsedDictionary(self):
        """ Tests creation of original-to-parsed filename dictionary. """
        formatted_time = unicode( time.strftime(
            '%Y-%m-%dT%H-%M-%S', (2005, 7, 13, 13, 41, 39, 2, 194, 1)) )  # u'Wed Jul 13 13:41:39 EDT 2005'
        input_dct = {u'QHACS_1110.txt': u'ORIG_QHACS_2005-07-13T13-41-39.dat', u'QHREF_1110.txt': u'ORIG_QHREF_2005-07-13T13-41-39.dat'}
        self.assertEquals(
            {u'ORIG_QHREF_2005-07-13T13-41-39.dat': u'PARSED_QHREF_2005-07-13T13-41-39.dat', u'ORIG_QHACS_2005-07-13T13-41-39.dat': u'PARSED_QHACS_2005-07-13T13-41-39.dat'},
            self.nmcnvrtr.makeArchiveOrigToArchiveParsedDictionary(input_dct, formatted_time) )

    def test_convertInputToOriginal(self):
        """ Tests de-conversion of extended filename back into original filename. """
        filename = 'PARSED_QHREF_2005-07-13T13-41-39.dat'
        self.assertEquals(
            'QHREF_0713.txt', self.nmcnvrtr.convertInputToOriginal(filename) )

    def test_prepareFinalDestinationDictionary(self):
        """ Tests de-conversion of extended filename back into original filename. """
        original_to_parsed_dct = {u'ORIG_QHREF_2005-07-13T13-41-39.dat': u'PARSED_QHREF_2005-07-13T13-41-39.dat', u'ORIG_QHACS_2005-07-13T13-41-39.dat': u'PARSED_QHACS_2005-07-13T13-41-39.dat'}
        destination_dir = settings.DESTINATION_DIR
        self.assertEquals(
            {u'PARSED_QHACS_2005-07-13T13-41-39.dat': u'qhacs0713.txt', u'PARSED_QHREF_2005-07-13T13-41-39.dat': u'qhref0713.txt'},
            self.nmcnvrtr.prepareFinalDestinationDictionary(original_to_parsed_dct, destination_dir) )

    # end class NameConverter_Test



if __name__ == "__main__":
  unittest.TestCase.maxDiff = None  # allows error to show in long output
  unittest.main()
