try:
	import _pickle as pickle
except:
	import pickle
import sys
import time
import datetime
import threading

import ScrapeThread as ST
import helper as h


def run_component():

	pickle_file = 'data/data.pickle'
	meta_file = 'data/scraping_metadata.pickle'


	#load up the data (NOTE: kept the metadata on scrapetime on a separate cPickle file because that was a separate project)
	data = pickle.load(open(pickle_file, 'rb'))
	metadata = pickle.load(open(meta_file, 'rb'))

	#has been previously set up in the metadata file
	for num_threads in metadata['search_domains']:

		keys = metadata['search_domains'][num_threads]

		#divide up given set of keys into num_threads subsets
		keys_subsets = h.chunkify(keys, num_threads)

		#each new threadcount group is always a new session, and each time program starts it's also a new session
		session = datetime.datetime.now()
		metadata['data'].update( { session:{} } )


		thread_list = []
		threadID = 0

		#print for update to keep track
		print("=========== \n NEW MUTLTHREADING \nNEW NUMBER OF THREADS: %s \n===========" % (num_threads))

		#run multiple threads
		for thread_keys in keys_subsets:
			threadID += 1
			metadata['data'][session].update( { threadID:[] } )
			thread = ST.scrapeThread(threadID, num_threads, thread_keys, pickle_file, meta_file, data, session, metadata)
			thread_list.append(thread)
		for thread in thread_list:
			thread.start()
		for thread in thread_list:
			thread.join()

		#final update of data within session
		pickle.dump(data, open(pickle_file, 'wb'))
		pickle.dump(metadata, open(meta_file, 'wb'))

	#final update of data after entire program
	pickle.dump(data, open(pickle_file, 'wb'))
	pickle.dump(metadata, open(meta_file, 'wb'))
