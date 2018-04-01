try:
	import _pickle as pickle
except:
	import pickle
import csv
from random import shuffle
import sys
import time
import numpy as np

import helper as h



def run_component():
	
	csv_directory = '/Users/kenta/Dropbox (Econ)/CanadianDoctors/British Columbia/BC Doctors/table/'

	pickle_file = 'data/data.pickle'
	meta_file = 'data/scraping_metadata.pickle'

	data = {}
	metadata = { 'search_domains':{}, 'data':{}}

	#CSV files between years 2000-2016 (inclusive)
	for x in range(1, 17):
		
		year = 2000 + x

		csvfile = csv_directory + "doc_" + str(year) + ".csv"

		with open(csvfile, 'r', encoding = 'utf-8') as fname:
			reader = csv.reader(fname)
			reader_list = list(reader)


			#some csv parsing
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
	chunks = h.chunkify(keys_array,num_subs)

	#organize the metadata dictionary
	for x in range(0, num_subs):
		num_threads = 2*x + 1
		search_subset = {num_threads:chunks[x]}
		metadata['search_domains'].update(search_subset)


	pickle.dump(data, open(pickle_file, 'wb'))
	pickle.dump(metadata, open(meta_file, 'wb'))

