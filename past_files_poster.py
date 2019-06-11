# -*- coding: utf-8 -*-

import datetime, glob, json, logging, os, pprint, time
from operator import itemgetter


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

    # def initialize_tracker( self ):
    #     """ Manages build.
    #         Called by main() """
    #     log.debug( f'len(files), `{len(self.files)}`' )
    #     for path in self.files:
    #         file_timestamp: float = os.path.getmtime( path )
    #         timestamp: datetime.datetime = datetime.datetime.fromtimestamp( file_timestamp )
    #         info: dict = { 'path': path, 'timestamp': timestamp, 'updated': None }
    #         self.filepath_tracker.append( info )
    #     sorted_filepath_tracker: list = sorted( self.filepath_tracker, key=itemgetter('timestamp') )
    #     for entry in sorted_filepath_tracker:
    #         entry['timestamp'] = str( entry['timestamp'] )
    #     log.debug( f'len(sorted_filepath_tracker), `{len(sorted_filepath_tracker)}`' )
    #     time_taken = str( datetime.datetime.now() - self.start )
    #     log.debug( f'time_taken, `{time_taken}`' )
    #     with open( self.DESTINATION_PATH, 'w' ) as f:
    #         jsn: str = json.dumps( sorted_filepath_tracker, sort_keys=True, indent=2 )
    #         f.write( jsn )
    #     return

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



if __name__ == '__main__':
    initializer = Initializer()
    initializer.initialize_tracker()
