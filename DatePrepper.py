# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Obtain date in right format when needed.
"""

import logging, time


log = logging.getLogger(__name__)


class DatePrepper(object):

    def __init__(self):
        self.timeToFormat = ""

    def prepareTimeStamp(self):
        if( len(self.timeToFormat) == 0):
            theTime = time.localtime()
        else:
            theTime = self.timeToFormat
        formattedTime = time.strftime("%Y-%m-%dT%H-%M-%S", theTime)
        return formattedTime
