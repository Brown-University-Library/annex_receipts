# -*- coding: utf-8 -*-

import json, os


LOG_PATH = os.environ['ANXEOD__LOG_PATH']
LOG_LEVEL = os.environ['ANXEOD__LOG_LEVEL']
assert LOG_LEVEL in [ 'D', 'I', 'E' ]  # debug, info, error

SOURCE_DIR = os.environ['ANXEOD__SOURCE_DIR_PATH']                       # should end in '/'
ARCHIVE_ORIGINAL_DIR = os.environ['ANXEOD__ARCHIVE_ORIGINAL_DIR_PATH']   # should end in '/'
ARCHIVE_PARSED_DIR = os.environ['ANXEOD__ARCHIVE_PARSED_DIR_PATH']       # should end in '/'
DESTINATION_DIR = os.environ['ANXEOD__DESTINATION_DIR_PATH']             # should end in '/'

PREFIX_LIST = json.loads( os.environ['ANXEOD__PREFIX_LIST_JSON'] )

MAIL_SMTPSERVER = os.environ['ANXEOD__MAIL_SMTPSERVER']
MAIL_RECIPIENTS = json.loads( os.environ['ANXEOD__MAIL_RECIPIENTS_JSON'] )
MAIL_SENDER = os.environ['ANXEOD__MAIL_SENDER']
MAIL_HEADERTO = os.environ['ANXEOD__MAIL_HEADERTO']
MAIL_HEADERCC = os.environ['ANXEOD__MAIL_HEADERCC']
MAIL_HEADERFROM = os.environ['ANXEOD__MAIL_HEADERFROM']
MAIL_SUBJECT = os.environ['ANXEOD__MAIL_SUBJECT']

ANNEX_COUNTS_API_UPDATER_URL = os.environ['ANXEOD__ANNEX_COUNTS_API_UPDATER_URL']
ANNEX_COUNTS_API_AUTHKEY = os.environ['ANXEOD__ANNEX_COUNTS_API_AUTHKEY']
