# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, os


LOG_PATH = unicode( os.environ['ANXEOD__LOG_PATH'] )

SOURCE_DIR = unicode( os.environ['ANXEOD__SOURCE_DIR_PATH'] )                       # should end in '/'
ARCHIVE_ORIGINAL_DIR = unicode( os.environ['ANXEOD__ARCHIVE_ORIGINAL_DIR_PATH'] )   # should end in '/'
ARCHIVE_PARSED_DIR = unicode( os.environ['ANXEOD__ARCHIVE_PARSED_DIR_PATH'] )       # should end in '/'
DESTINATION_DIR = unicode( os.environ['ANXEOD__DESTINATION_DIR_PATH'] )             # should end in '/'

PREFIX_LIST = json.loads( os.environ['ANXEOD__PREFIX_LIST_JSON'] )
