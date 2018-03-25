from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
try:
	import _pickle as pickle
except:
	import pickle
import csv
from random import shuffle
import sys
import time
import numpy as np
import threading
import math
import datetime


###====== <DICTIONARY ORGANIZATION> ======###
'''

data
{ tuple(str,str)=(fname,lname) : { str='RECORDS' : { int=year:str=salary },
						 		   str='SCRAPING' : { str='done_search' : bool=done_search,
						 		   					  str='pages' : array[str=soup],
						 		   					  str='empty_result' : bool=empty_result,
						 		   					  str='scrape_time' : time=scrape_time,
						 		   					  str='date_time' : datetime=now,
						 		   					  str='threadID' : int=threadID,
						 		   					  str='num_threads' : int=num_threads,
						 		   					  str='session' : datetime=session,
						 		   					},
						 		   str='GOOGLE' : { }
								 }
}


metadata
{ str='search_domains' : { int=num_threads : array[(str,str)]=search_subset },
  str='data' : { datetime=session : { int=threadID : array[ { str='scrape_time' : time:scrape_time,
															  str='date_time' : datetime:now,
															  str='fname' : str=fname,
															  str='lname' : str=lname }
														  ] 
  									} 
  			   }
}
	
'''
###====== </DICTIONARY ORGANIZATION> ======###





###====== <DEFINITIONS> ======###

class doctorScraper:

	def __init__(self, dictionary):
		self.doctor = dictionary
		self.doctor['SCRAPING'].update({ 'done_search':False, 'pages':[] })
		self.meta = {}

	def search(self):

		
		url = 'omitted here'
		now = datetime.datetime.now()
		start_time = time.time()

		#start scraping
		browser = webdriver.PhantomJS()
		browser.get(url)

		#enter first name
		search_box_fname = browser.find_element_by_id('edit-filter-first-name')
		search_box_fname.send_keys(self.doctor['fname'])
		
		#enter last name
		search_box_lname = browser.find_element_by_id('edit-filter-last-name')
		search_box_lname.send_keys(self.doctor['lname'])
	
		#begin search
		search_box_lname.submit()
		self.recurse_pages(browser)

		#finish scraping
		browser.close()
		scrape_time = time.time() - start_time

		#update metadata within metadata file and data file
		self.doctor['SCRAPING'].update({ 'done_search':True, 'scrape_time':scrape_time, 'date_time':now} )
		self.meta.update( { 'scrape_time':scrape_time, 'date_time':now, 'fname':self.doctor['fname'], 'lname':self.doctor['lname']} )


	def recurse_pages(self, browser):
		html = browser.page_source
		soup = BeautifulSoup(html, 'html.parser')

		#no results/pages (empty result)
		error = list(soup.find_all('div', class_='messages error'))
		if len(error) != 0:
			self.doctor['SCRAPING'].update({ 'empty_result':True })
			return

		#add current page
		self.doctor['SCRAPING']['pages'].append(str(soup))

		list_pages = (soup.find_all('ul', class_='pager inline item-list'))

		#if more result pages exist
		if (len(list(list_pages))!=0):
			clickables = browser.find_elements_by_link_text('Next Results >')
			if (len(list(clickables))!=0):
				browser.find_element_by_link_text('Next Results >').click()
				self.recurse_pages(browser)
				return
		
		#if no more result pages
		self.doctor['SCRAPING'].update({ 'empty_result':False })


class scrapeThread(threading.Thread):

	def __init__(self, threadID, num_threads, keys, data_filename, metadata_filename, data, session, metadata):
		super(scrapeThread, self).__init__()
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
			doctor_scraper = doctorScraper(doctor)
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


#to seaparate an array into n subset arrays
#credit: https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def chunkify(lst, n):
	return [lst[i::n] for i in range(n)]

###====== </DEFINITIONS> ======###





###====== <PROGRAM/SCRIPT> ======###

pickle_file = 'data.pickle'
meta_file = 'scraping_metadata.pickle'


#load up the data (NOTE: kept the metadata on scrapetime separate because that was a separate project)
data = pickle.load(open(pickle_file, 'rb'))
metadata = pickle.load(open(meta_file, 'rb'))

#has been previously set up in the metadata file
for num_threads in metadata['search_domains']:

	keys = metadata['search_domains'][num_threads]

	#divide up given set of keys into num_threads subsets
	keys_subsets = chunkify(keys, num_threads)

	#each new threadcount group is always a new session, and each time program starts also a new session
	session = datetime.datetime.now()
	metadata['data'].update( { session:{} } )


	thread_list = []
	threadID = 0

	#print for update to keep track
	print("=========== \n NEW MUTLTHREADING \nNEW NUMBER OF THREADS: %s \n===========" % (num_threads))

	#run multiple threads for webdriver
	for thread_keys in keys_subsets:
		threadID += 1
		metadata['data'][session].update( { threadID:[] } )
		thread = scrapeThread(threadID, num_threads, thread_keys, pickle_file, meta_file, data, session, metadata)
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

###====== </PROGRAM/SCRIPT> ======###




###====== <EXTRA> ======###
#function no longer used, kept here just in case
def my_split(search_array, num_to_split):
	length = len(search_array)
	split_length = math.floor(length/num_to_split)
	index_array = []
	index_counter = 0
	for i in range(0, num_to_split):
		if i != (num_to_split-1):
			index_array.append({'start':index_counter, 'end':(index_counter+split_length-1)})
			index_counter = index_counter + split_length
		else:
			index_array.append({'start':index_counter, 'end':(length - 1)})
	return index_array
###====== </EXTRA> ======###
