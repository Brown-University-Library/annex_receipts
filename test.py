# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, logging, os, sys, unittest
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )
from annex_eod_project.DatePrepper import DatePrepper

""" To run tests:
    - activate v-env
    - cd into annex_eod_project dir
    - All tests...
      python ./test.py
    - Single test, eg:
      python ./test.py DatePrepper_Test.test__prepareTimeStamp """


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




if __name__ == "__main__":
  unittest.TestCase.maxDiff = None  # allows error to show in long output
  unittest.main()
