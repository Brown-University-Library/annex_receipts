# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, os


LOG_PATH = unicode( os.environ['ANXEOD__LOG_PATH'] )

SOURCE_DIR = unicode( os.environ['ANXEOD__SOURCE_DIR_PATH'] )                       # should end in '/'
ARCHIVE_ORIGINAL_DIR = unicode( os.environ['ANXEOD__ARCHIVE_ORIGINAL_DIR_PATH'] )   # should end in '/'
ARCHIVE_PARSED_DIR = unicode( os.environ['ANXEOD__ARCHIVE_PARSED_DIR_PATH'] )       # should end in '/'
DESTINATION_DIR = unicode( os.environ['ANXEOD__DESTINATION_DIR_PATH'] )             # should end in '/'

PREFIX_LIST = json.loads( os.environ['ANXEOD__PREFIX_LIST_JSON'] )

MAIL_SMTPSERVER = unicode( os.environ['ANXEOD__MAIL_SMTPSERVER'] )
MAIL_RECIPIENTS = json.loads( os.environ['ANXEOD__MAIL_RECIPIENTS_JSON'] )
MAIL_SENDER = unicode( os.environ['ANXEOD__MAIL_SENDER'] )
MAIL_HEADERTO = unicode( os.environ['ANXEOD__MAIL_HEADERTO'] )
MAIL_HEADERCC = unicode( os.environ['ANXEOD__MAIL_HEADERCC'] )
MAIL_HEADERFROM = unicode( os.environ['ANXEOD__MAIL_HEADERFROM'] )
MAIL_SUBJECT = unicode( os.environ['ANXEOD__MAIL_SUBJECT'] )
