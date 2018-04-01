try:
	import _pickle as pickle
except:
	import pickle
from random import shuffle
import sys
import time
import datetime
import os

import Geocode as G


def run_component():


	sys.setrecursionlimit(50000)

	api_key = "AIzaSyCXXvQOEt31dz8Nw070bye9pwEDBEl0g1o" 
	#received 2018/01/24/15:52 kentabaronfuruyama@gmail.com, 1st "BC Doctors1"

	file_list = [f for f in os.listdir('data_subsets') if not f.startswith('.')]

	#to capture how many requests were made with the given api_key
	search_counter = 0

	for file in file_list:
		pickle_file = "data_subsets/" + file

		data = pickle.load(open(pickle_file, 'rb'))

		num_docs = len(data)
		update_freq = 75
		upload_freq = 50

		counter = 0

		#for each doctor
		for doc_key in data:
			
			counter +=1

			doctor = data[doc_key]

			#check if it has been googled already
			if 'googled' in doctor['GOOGLE']:
				if doctor['GOOGLE']['googled']:
					continue

			#set up dictionary
			doctor['GOOGLE'].update( {'googled':False} )
			doctor['GOOGLE'].update( { 'geo_data':{} } )

			#for each search result for a given doctor
			for result_number in doctor['HTML_PARSING']['parsed_infos']:

				address = doctor['HTML_PARSING']['parsed_infos'][result_number]['address']

				#don't want to waste a request on empty address
				if (address != "" and not address.isspace()):
					geocode = G.Geocode(api_key, address)
					geocode.search()
					search_counter += 1
					doctor['GOOGLE']['geo_data'].update( { result_number:geocode._dict } )

				#update boolean
				doctor['GOOGLE'].update( {'googled':True} )


			if (counter % update_freq == 0):
				print("percentage completed to google for %s is: %s" % (file, counter*100/num_docs))
				print('number of geocode queries made is: %s' % (search_counter))
				print("==")
			if (counter % upload_freq == 0):
				pickle.dump(data, open(pickle_file, 'wb'))
				print('..saved..')



		pickle.dump(data, open(pickle_file, 'wb'))
