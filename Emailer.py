# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Part of LAS-to-Josiah code.
Handle sending of email when files are found.
"""

import logging, smtplib
from annex_eod_project import settings


log = logging.getLogger(__name__)


class Emailer( object ):

    def __init__( self ):
        log.debug( 'emailer initialized' )
        self.smtpserver = settings.MAIL_SMTPSERVER
        self.AUTHREQUIRED = 0   # if you need to use SMTP AUTH set to 1
        self.smtpuser = ''      # for SMTP AUTH, set SMTP username here
        self.smtppass = ''      # for SMTP AUTH, set SMTP password here
        self.RECIPIENTS = settings.MAIL_RECIPIENTS
        self.SENDER = settings.MAIL_SENDER
        self.headerTo = settings.MAIL_HEADERTO
        self.headerCc = settings.MAIL_HEADERCC
        self.headerFrom = settings.MAIL_HEADERFROM
        self.headerSubject = settings.MAIL_SUBJECT
        self.basicHeaderInfo = self.headerTo + "\n" + self.headerCc + "\n" + self.headerFrom + "\n" + self.headerSubject + "\n"
        self.full_message = None

    def sendEmail(self, message):
        self.full_message = self.update_full_message( message )
        session = smtplib.SMTP(self.smtpserver)
        if self.AUTHREQUIRED:
            session.login(self.smtpuser, self.smtppass)
        returnValue = "init"
        try:
            smtpresult = session.sendmail( self.SENDER, self.RECIPIENTS, self.full_message )
            # if smtpresult:
            #     errorString = ""
            #     for recip in smtpresult.keys():
            #         errorString = "Could not deliver mail to: " + recip + "\n"
            #         errorString = errorString + "Server said: " + smtpresult[recip][0] + "\n"
            #         errorString = errorString + smtpresult[recip][1] + "\n"
            #         errorString = errorString + errstr
            #     raise smtplib.SMTPException, errstr
        except:
            session.quit()
            print "\n"
            print "Attempt to send email failed with following errors: " + str(smtpresult)
            returnValue = smtpresult
        else:
            session.quit()
            returnValue = "success"
        return returnValue

    def update_full_message( self, message ):
        """ Stores full message; for easy unit-testing without sending.
            Called by sendEmail() """
        self.full_message = self.basicHeaderInfo + message
        return self.full_message
