try:
	import _pickle as pickle
except:
	import pickle
import time
import datetime
import numpy as np
import threading

import DoctorScraper as DS

class ScrapeThread(threading.Thread):

	def __init__(self, threadID, num_threads, keys, data_filename, metadata_filename, data, session, metadata):
		super(ScrapeThread, self).__init__()
		self.threadID = threadID
		self.num_threads = num_threads
		self.keys = keys
		self.data_filename = data_filename
		self.metadata_filename = metadata_filename
		self.data = data
		self.session = session
		self.metadata = metadata

	def run(self):
	
		time_sum = 0 #summing total scrapetime for a given update_interval
		counter = 0 #counting number of scrapes for this thread
		search_length = len(self.keys) #total keys to search in this thread

		update_interval = 150 #how often data is dumped in pickle file

		for key in self.keys:
			counter += 1
			doctor = self.data[key]

			#in case this scrape has been performed already in a previous session
			if ('done_search' in doctor['SCRAPING']):
				if doctor['SCRAPING']['done_search']:
					continue
			
			#scrape
			start_time = time.time()
			doctor_scraper = DS.DoctorScraper(doctor)
			doctor_scraper.search()

			#update dictionary objects
			doctor_scraper.doctor['SCRAPING'].update({ 'threadID':self.threadID, 'num_threads':self.num_threads, 'session':self.session})
			self.metadata['data'][self.session][self.threadID].append(doctor_scraper.meta)
			self.data[key] = doctor_scraper.doctor #this line may be redundant, but added it here for debugging

			time_sum += (time.time()-start_time)

			#for updating python pickle files
			if (counter % update_interval == 0):

				#note: we work directly onto the memory of search_array instead of a copy of it, as python works with pass by reference
				pickle.dump(self.data, open(self.data_filename, 'wb'))
				pickle.dump(self.metadata, open(self.metadata_filename, 'wb'))
				print('== thread %s, thread size %s, average time taken to scrape (and process) is %s, percentage completed to scrape is %s' % (self.threadID, self.num_threads, time_sum/update_interval, 100*counter/search_length))
				time_sum = 0

		print('#### ==thread %s is complete== ####' % (self.threadID))

