# -*- coding: utf-8 -*-

import argparse, datetime, glob, json, logging, os, pprint, random, time
from functools import partial
from operator import itemgetter
from typing import Iterator, List, Optional

import asks, trio


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


class Updater:
    """ Updates db. """

    def __init__( self ):
        self.COUNT_TRACKER_PATH = os.environ['ANXEOD__TRACKER_B_PATH']
        self.UPDATED_COUNT_TRACKER_PATH = os.environ['ANXEOD__TRACKER_C_PATH']
        self.API_UPDATER_URL = os.environ['ANXEOD__ANNEX_COUNTS_API_UPDATER_URL']
        self.API_AUTHKEY = os.environ['ANXEOD__ANNEX_COUNTS_API_AUTHKEY']
        self.updated_count_tracker_dct = {}
        self.nursery = None
        self.throttle: float = 1.0
        self.mutex = None
        self.continue_worker_flag = True
        self.start = datetime.datetime.now()

    def update_db( self ) -> None:
        """ Calls concurrency-manager function.
            Called by main()
            Credit: <https://stackoverflow.com/questions/51250706/combining-semaphore-and-time-limiting-in-python-trio-with-asks-http-request>
            """
        self.setup_final_tracker()
        trio.run( partial(self.manage_concurrent_updates, n_workers=3) )
        log.debug( f'total time taken, `{str( datetime.datetime.now() - self.start )}` seconds' )
        return

    def setup_final_tracker( self ) -> None:
        """ Initializes final tracker if it doesn't exist.
            Called by update_db() """
        try:
            with open( self.UPDATED_COUNT_TRACKER_PATH, 'r' ) as f:
                self.updated_count_tracker_dct = json.loads( f.read() )
                log.debug( 'existing updated_count_tracker found and loaded' )
        except Exception as e:
            log.debug( f'updated_count_tracker _not_ found, exception was ```{e}```, so creating it' )
            with open( self.COUNT_TRACKER_PATH, 'r' ) as f:
                count_tracker_dct = json.loads( f.read() )
            for date_key in count_tracker_dct.keys():
                entry = count_tracker_dct[date_key]
                entry['updated'] = None
            self.updated_count_tracker_dct = count_tracker_dct
            with open( self.UPDATED_COUNT_TRACKER_PATH, 'w' ) as f:
                f.write( json.dumps(self.updated_count_tracker_dct, sort_keys=True, indent=2) )
        return

    async def manage_concurrent_updates(self, n_workers: int ):
        """ Manages asynchronous processing of db updates.
            Called by update_db() """
        async with trio.open_nursery() as nursery:
            self.nursery = nursery
            for _ in range(n_workers):
                self.nursery.start_soon( self.run_worker_job )

    async def run_worker_job( self ) -> None:
        """ Manages worker job.
            Called by manage_concurrent_updates() """
        log.debug( 'function starting' )
        temp_counter = 0
        while self.continue_worker_flag is True:
            temp_counter += 1
            await self.get_mutex().acquire()
            log.debug( 'mutex acquired to start job' )
            self.nursery.start_soon( self.tick )
            entry: Optional[dict] = self.grab_next_entry()
            if entry is None:
                log.info( 'no more entries -- cancel' )
                self.continue_worker_flag = False
            elif temp_counter == 3:  # sanity-check
                log.info( f'temp_counter, `{temp_counter}`, so will stop' )
                self.continue_worker_flag = False
            else:
                # params: dict = self.prep_params( entry )
                # response = await asks.post( entry, data=params )
                # self.update_tracker( response )
                await self.post_update( entry )
                log.debug( 'url processed' )
                self.save_updated_tracker()
        return

    def get_mutex( self ):
        if self.mutex == None:
            self.mutex = trio.Semaphore(1)
        else:
            pass
        log.debug( 'returning mutex' )
        return self.mutex

    async def tick( self ) -> None:
        await trio.sleep( self.throttle )
        self.mutex.release()

    def grab_next_entry( self ) -> Optional[dict]:
        """ Finds and returns next entry to process.
            Called by run_worker_job() """
        key_entry: Optional[dict] = None
        for key, count_info in self.updated_count_tracker_dct.items():
            log.debug( f'current key, `{key}`; current count_info, ```{count_info}```' )
            if count_info['updated'] is None:
                log.debug( 'found next entry to process' )
                key_entry = { key: count_info }
                count_info['updated'] = 'in_process'
                break
        log.debug( f'returning key_entry, ```{key_entry}```' )
        log.debug( f'self.updated_count_tracker_dct, ```{pprint.pformat(self.updated_count_tracker_dct)[0:1000]}```' )
        return key_entry

    async def post_update( self, entry: dict  ):
        """ Runs the post.
            Called by run_worker_job() """
        params: dict = self.prep_params( entry )
        params['auth_key'] = self.API_AUTHKEY
        temp_process_id = random.randint( 1111, 9999 )
        log.debug( f'`{temp_process_id}` -- about to hit url' )
        resp = await asks.post( self.API_UPDATER_URL, data=params, timeout=10 )
        log.debug( f'status_code, `{resp.status_code}`; type(status_code), `{type(resp.status_code)}`' )
        log.debug( f'content, ```{resp.content.decode("utf-8")}```')
        log.debug( f'`{temp_process_id}` -- url response received, ```{resp.content}```' )
        date_key, other = list(entry.items())[0]
        self.updated_count_tracker_dct[date_key]['updated'] = True
        return

    def prep_params( self, entry: dict ):
        """ Preps post params.
            Called by post_update() """
        ( date_key, info ) = list( entry.items() )[0]  # date_key: str, info: dict
        log.debug( f'info, ```{info}```' )
        param_dct = {
            'date': date_key,
            'hay_accessions': info['hay_accessions'],
            'hay_refiles': info['hay_refiles'],
            'non_hay_accessions': info['non-hay_accessions'],
            'non_hay_refiles': info['non-hay_refiles'],
        }
        log.debug( f'param_dct, ```{param_dct}```' )
        return param_dct

    def save_updated_tracker( self ) -> None:
        """ Writes dct attribute.
            Called by run_worker_job() """
        with open( self.UPDATED_COUNT_TRACKER_PATH, 'w' ) as f:
            f.write( json.dumps(self.updated_count_tracker_dct, sort_keys=True, indent=2) )
        log.debug( 'updated tracker saved' )
        return

    ## end class Updater




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
    updater = Updater()
    safe_dispatcher = {
        'initialize_tracker': initializer.initialize_tracker,
        'build_counts': counter.build_count_tracker,
        'update_db': updater.update_db
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
