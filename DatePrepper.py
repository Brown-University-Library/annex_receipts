# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging, time

"""
Part of LAS-to-Josiah code.
Obtain date in right format when needed.
"""


log = logging.getLogger(__name__)


class DatePrepper(object):

    def __init__(self):
        self.timeToFormat = ""

    def obtainDate(self):
        # import time
        if( len(self.timeToFormat) == 0):
            theTime = time.localtime()
        else:
            theTime = self.timeToFormat
        formattedTime = time.strftime("%a %b %d %H:%M:%S %Z %Y", theTime)
        log.debug( 'type, formattedTime, `{}`'.format(type(formattedTime)) )
        return formattedTime

    def prepareTimeStamp(self):
        # import time
        if( len(self.timeToFormat) == 0):
            theTime = time.localtime()
        else:
            theTime = self.timeToFormat
        formattedTime = time.strftime("%Y-%m-%dT%H-%M-%S", theTime)
        return formattedTime
