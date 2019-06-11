# -*- coding: utf-8 -*-

import argparse, datetime, glob, json, logging, os, pprint, time
from operator import itemgetter
from typing import List


logging.basicConfig(
    # filename=settings.LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


class Initializer:
    """ Creates initial tracker. """

    def __init__( self ):
        self.SOURCE_DIR_PATH = os.environ['ANXEOD__SOURCE_DIR_PATH']
        self.DESTINATION_PATH = os.environ['ANXEOD__TRACKER_A_PATH']
        self.filepath_tracker = []
        self.start = datetime.datetime.now()
        self.files: list = glob.glob( f'{self.SOURCE_DIR_PATH}/*.dat' )

    def initialize_tracker( self ):
        """ Manages build.
            Called by main() """
        log.debug( f'len(files), `{len(self.files)}`' )
        for path in self.files:
            self.build_initial_tracker( path )
        sorted_filepath_tracker = self.build_sorted_tracker()
        time_taken = str( datetime.datetime.now() - self.start )
        log.debug( f'time_taken, `{time_taken}`' )
        with open( self.DESTINATION_PATH, 'w' ) as f:
            jsn: str = json.dumps( sorted_filepath_tracker, sort_keys=True, indent=2 )
            f.write( jsn )
        return

    def build_initial_tracker( self, path: str ) -> None:
        """ Creates initial dict of file-info & appends it to self.filepath_tracker list.
            Called by initialize_tracker() """
        file_timestamp: float = os.path.getmtime( path )
        timestamp: datetime.datetime = datetime.datetime.fromtimestamp( file_timestamp )
        info: dict = { 'path': path, 'timestamp': timestamp, 'updated': None }
        self.filepath_tracker.append( info )
        return

    def build_sorted_tracker( self ) -> list:
        """ Sorts initial tracker & updates timestamp-type.
            Called by initialize_tracker() """
        sorted_filepath_tracker: list = sorted( self.filepath_tracker, key=itemgetter('timestamp') )
        for entry in sorted_filepath_tracker:
            entry['timestamp'] = str( entry['timestamp'] )  # needs for json dump
        log.debug( f'len(sorted_filepath_tracker), `{len(sorted_filepath_tracker)}`' )
        return sorted_filepath_tracker

    ## end class Initializer


class Counter:
    """ Creates count-tracker. """

    def __init__( self ):
        self.INITIAL_TRACKER_PATH = os.environ['ANXEOD__TRACKER_A_PATH']
        self.COUNT_TRACKER_PATH = os.environ['ANXEOD__TRACKER_B_PATH']
        self.date_dct = {}
        self.start = datetime.datetime.now()

    def build_count_tracker( self ) -> None:
        """
        Flow...
        load file
        create new count_tracker file
        create a list of date-dicts by going through all entries
        for each entry
            determin the proper date
            determine the _kind_ of count
            determine the count
            update the count-tracker file
        """
        file_entries: List[dict] = self.load_file_list()
        self.initialize_count_tracker()
        self.make_date_dict( file_entries )
        for entry in file_entries:
            entry_date: datetime.date = datetime.datetime.strptime( entry['timestamp'], '%Y-%m-%d %H:%M:%S' ).date()
            count_type: str = self.parse_type( entry['path'] )
            count: int = self.parse_count( entry['path'] )
            self.date_dct[str(entry_date)][count_type] = count
        self.update_count_tracker()
        return

    def load_file_list( self ) -> List[dict]:
        """ Loads tracker-a.
            Called by build_count_tracker() """
        with open( self.INITIAL_TRACKER_PATH, 'r' ) as f:
            entries_jsn: str = f.read()
            entries: list = json.loads( entries_jsn )
        return entries

    def initialize_count_tracker( self ) -> None:
        """ Saves empty list file.
            Called by build_count_tracker() """
        count_tracker: list = []
        empty_count_tracker_jsn: str = json.dumps( count_tracker )
        with open( self.COUNT_TRACKER_PATH, 'w' ) as f:
            f.write( empty_count_tracker_jsn )
        return

    def make_date_dict( self, file_entries: List[dict] ) -> None:
        """ Populates self.date_dct.
            Called by build_count_tracker() """
        for entry in file_entries:
            timestamp: str = entry['timestamp']
            date_obj: datetime.date = datetime.datetime.strptime( timestamp, '%Y-%m-%d %H:%M:%S' ).date()
            date_str: str = str( date_obj )
            self.date_dct[date_str] = {}
        log.debug( f'self.date_dct, ```{pprint.pformat(self.date_dct)[0:100]}```' )
        log.debug( f'num-dates, `{len(self.date_dct.keys())}`' )
        return

    def parse_type( self, path: str ) -> str:
        """ Parses count type.
            Called by build_count_tracker() """
        count_type: str = ''
        if 'QHACS' in path:
            count_type = 'hay_accessions'
        elif 'QSACS' in path:
            count_type = 'non-hay_accessions'
        elif 'QHREF' in path:
            count_type = 'hay_refiles'
        elif 'QSREF' in path:
            count_type = 'non-hay_refiles'
        else:
            raise Exception( 'unhandled count-type' )
        return count_type

    def parse_count( self, path: str ) -> int:
        """ Loads file and parses count.
            Called by build_count_tracker() """
        with open( path, 'r' ) as f:
            data = f.readlines()
        count = len( data )
        return count

    def update_count_tracker( self ) -> None:
        """ Writes file.
            Called by build_count_tracker() """
        jsn: str = json.dumps( self.date_dct, sort_keys=True, indent=2 )
        with open( self.COUNT_TRACKER_PATH, 'w' ) as f:
            f.write( jsn )
        log.debug( f'time-taken, `{str( datetime.datetime.now() - self.start )}`' )
        return

    ## end class Counter


## setup

# SOURCE_DIR_PATH = os.environ['ANXEOD__SOURCE_DIR_PATH']

# filepath_tracker = []
# date_count_tracker = []

# logging.basicConfig(
#     # filename=settings.LOG_PATH,
#     level=logging.DEBUG,
#     format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
#     datefmt='%d/%b/%Y %H:%M:%S' )
# log = logging.getLogger(__name__)


# ## get list of files

# files: list = glob.glob( f'{SOURCE_DIR_PATH}/*.dat' )
# # log.debug( f'files, ```{pprint.pformat(files)}```' )
# log.debug( f'len(files), `{len(files)}`' )


# ## populate filepath_tracker

# start = datetime.datetime.now()
# for path in files:
#     # log.debug( f'path, `{path}`' )

#     file_timestamp: float = os.path.getmtime( path )
#     # log.debug( f'file_timestamp, `{file_timestamp}`; type, `{type(file_timestamp)}`' )

#     timestamp: datetime.datetime = datetime.datetime.fromtimestamp(file_timestamp)
#     # log.debug( f'timestamp, `{timestamp}`; type(timestamp), `{type(timestamp)}`' )

#     info: dict = { 'path': path, 'timestamp': timestamp, 'updated': None }
#     filepath_tracker.append( info )

# sorted_filepath_tracker: list = sorted( filepath_tracker, key=itemgetter('timestamp') )
# # log.debug( f'sorted_filepath_tracker, ```{pprint.pformat(sorted_filepath_tracker)}```' )
# log.debug( f'len(sorted_filepath_tracker), `{len(sorted_filepath_tracker)}`' )

# time_taken = str( datetime.datetime.now() - start )
# log.debug( f'time_taken, `{time_taken}`' )


## for each file...

# record: dict
# for record in files:

    ## get count

    ## post

    ## update tracker




# --------------------
# trio experimentation from: <https://stackoverflow.com/questions/51250706/combining-semaphore-and-time-limiting-in-python-trio-with-asks-http-request>
# --------------------


# (neither of the two methods below work with requests)


# # --------------------
# # works...
# # --------------------

# import pprint
# from functools import partial
# from typing import List, Iterator

# import asks
# import trio

# links: List[str] = [
#     'https://httpbin.org/delay/7',
#     'https://httpbin.org/delay/6',
#     'https://httpbin.org/delay/3'
# ] * 2

# responses = []

# async def fetch_urls(urls: Iterator, responses: list, n_workers: int, throttle: int ):
#     # Using binary `trio.Semaphore` to be able
#     # to release it from a separate task.
#     mutex = trio.Semaphore(1)

#     async def tick():
#         await trio.sleep(throttle)
#         mutex.release()

#     async def worker():
#         for url in urls:
#             await mutex.acquire()
#             print( f'[{round(trio.current_time(), 2)}] Start loading link: {url}' )
#             nursery.start_soon(tick)
#             response = await asks.get(url)
#             responses.append(response)

#     async with trio.open_nursery() as nursery:
#         for _ in range(n_workers):
#             nursery.start_soon(worker)

# # trio.run( fetch_urls, iter(links), responses, 5, 1 )  # works
# # trio.run( fetch_urls, urls=iter(links), responses=responses, n_workers=5, throttle=1 )  # doesn't work
# trio.run( partial(fetch_urls, urls=iter(links), responses=responses, n_workers=5, throttle=1) )  # works

# print( f'responses, ```{pprint.pformat(responses)}```' )


# --------------------
# works...
# --------------------

# from typing import List, Iterator

# import asks
# import trio


# asks.init('trio')

# links: List[str] = [
#     'https://httpbin.org/delay/4',
#     'https://httpbin.org/delay/3',
#     'https://httpbin.org/delay/1'
# ] * 3


# async def fetch_urls(urls: List[str], number_workers: int, throttle_rate: float):

#     async def token_issuer(token_sender: trio.abc.SendChannel, number_tokens: int):
#         async with token_sender:
#             for _ in range(number_tokens):
#                 await token_sender.send(None)
#                 await trio.sleep(1 / throttle_rate)

#     async def worker(url_iterator: Iterator, token_receiver: trio.abc.ReceiveChannel):
#         async with token_receiver:
#             for url in url_iterator:
#                 await token_receiver.receive()

#                 print(f'[{round(trio.current_time(), 2)}] Start loading link: {url}')
#                 response = await asks.get(url)
#                 # print(f'[{round(trio.current_time(), 2)}] Loaded link: {url}')
#                 responses.append(response)

#     responses = []
#     url_iterator = iter(urls)
#     token_send_channel, token_receive_channel = trio.open_memory_channel(0)

#     async with trio.open_nursery() as nursery:
#         async with token_receive_channel:
#             nursery.start_soon(token_issuer, token_send_channel.clone(), len(urls))
#             for _ in range(number_workers):
#                 nursery.start_soon(worker, url_iterator, token_receive_channel.clone())

#     return responses

# responses = trio.run(fetch_urls, links, 5, 1.)


# --------------------
# caller
# --------------------


def parse_args():
    """ Parses arguments when module called via __main__ """
    parser = argparse.ArgumentParser( description='Required: function-name.' )
    parser.add_argument( '--function', '-f', help='function name required', required=True )
    args_dict = vars( parser.parse_args() )
    return args_dict


def call_function( function_name: str ) -> None:
    """ Safely calls function named via input string to __main__
        Credit: <https://stackoverflow.com/a/51456172> """
    log.debug( f'function_name, ```{function_name}```' )
    initializer = Initializer()
    counter = Counter()
    safe_dispatcher = {
        'initialize_tracker': initializer.initialize_tracker,
        'build_counts': counter.build_count_tracker
        }
    try:
        safe_dispatcher[function_name]()
    except:
        raise Exception( 'invalid function' )
    return


if __name__ == '__main__':
    args: dict = parse_args()
    log.debug( f'args, ```{args}```' )
    submitted_function: str = args['function']
    call_function( submitted_function )
