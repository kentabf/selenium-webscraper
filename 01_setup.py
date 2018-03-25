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
import multiprocessing as mp
import threading
import math


###====== <DICTIONARY ORGANIZATION> ======###
'''

data
{ tuple(str,str)=(fname,lname) : { str='RECORDS' : { int=year:str=salary },
						 		   str='SCRAPING' : { },
						 		   str='GOOGLE' : { }
								 }
}

metadata
{ str='search_domains' : { int=num_threads : array[(str,str)]=search_subset },
  str='data' : {  }
}
	
'''
###====== </DICTIONARY ORGANIZATION> ======###





###====== <DEFINITIONS> ======###
#to seaparate an array into n subset arrays
#credit: https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def chunkify(lst, n):
	return [lst[i::n] for i in range(n)]
###====== </DEFINITIONS> ======###





###====== <PROGRAM/SCRIPT> ======###

data_directory = '/Users/kenta/Dropbox (Econ)/CanadianDoctors/British Columbia/BC Doctors/table/'
# cd "Dropbox (Econ)/CanadianDoctors/British Columbia/scrape"

pickle_file = 'data.pickle'
meta_file = 'scraping_metadata.pickle'

data = {}
metadata = { 'search_domains':{}, 'data':{}}


for x in range(1, 17):
	
	year = 2000 + x

	csvfile = data_directory + "doc_" + str(year) + ".csv"

	with open(csvfile, 'r', encoding = 'utf-8') as fname:
		reader = csv.reader(fname)
		reader_list = list(reader)

		for row in reader_list[1:]:
			fname = row[1]
			lname = row[0]
			salary = row[2]

			if (fname, lname) in data:
				data[(fname,lname)]['RECORDS'].update( { year:salary } )

			else:
				data.update( { (fname,lname):{ 'fname':fname, 'lname':lname, 'RECORDS':{}, 'SCRAPING':{}, 'GOOGLE':{} } } )
				data[(fname,lname)]['RECORDS'].update( { year:salary } )

			data[(fname,lname)].update({ 'fname':fname, 'lname':lname })

#this will contain arrays of (fname,lname) keys
keys_array = []

#fill array with all (fname,lname) keys
for key in data:
	keys_array.append(key)

#choose lower&upper bound on threadcount, as well as incrementing size
low = 1
high = 17
step_size = 2
num_subs = (low+high)//step_size

#randomization
np.random.shuffle(keys_array)

#chunks is an array of arrays containing (fname,lname) keys
chunks = chunkify(keys_array,num_subs)

#organize the metadata dictionary
for x in range(0, num_subs):
	num_threads = 2*x + 1
	search_subset = {num_threads:chunks[x]}
	metadata['search_domains'].update(search_subset)


pickle.dump(data, open(pickle_file, 'wb'))
pickle.dump(metadata, open(meta_file, 'wb'))

###====== </PROGRAM/SCRIPT> ======###