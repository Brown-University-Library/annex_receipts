# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, logging, os, pprint, sys, unittest
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )
from annex_eod_project import settings
from annex_eod_project.DatePrepper import DatePrepper
from annex_eod_project.Emailer import Emailer
from annex_eod_project.FileHandler import FileHandler

""" To run tests:
    - activate v-env
    - cd into annex_eod_project dir
    - All tests...
      python ./test.py
    - Single test, eg:
      python ./test.py DatePrepper_Test.test__prepareTimeStamp """


logging.basicConfig(
    # filename=settings.LOG_PATH,
    level=logging.DEBUG,
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
        log.debug( 'lines, ```{}```'.format(pprint.pformat(lines)) )
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
        log.debug( 'cwd, ```{}```'.format(cwd) )
        result = self.flhndlr.scanDirectory( cwd )
        self.assertEquals( list, type(result) )
        self.assertEquals( True, '.DS_Store' not in result )  # cleaned file
        self.assertEquals( True, '.git' not in result )  # directories removed

    # end class FileHandler_Test




if __name__ == "__main__":
  unittest.TestCase.maxDiff = None  # allows error to show in long output
  unittest.main()
