from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
try:
	import _pickle as pickle
except:
	import pickle
import json
import csv
from random import shuffle
import sys
import time
import numpy as np
import multiprocessing as mp
import threading
import math
import datetime
import os
import googlemaps
import requests



# cd 'Dropbox (Econ)/CanadianDoctors/British Columbia/scrape'
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
						 		   str='GOOGLE' : { str='googled' : bool=googled,
						 		   					str='geo_data' : { int=result_number : { str='datetime' : datetime=date_time },
						 		   														   { str='results' : str=geocode_results }
						 		   									 }
						 		   				  },
						 		   str='HTML_PARSING' : { str='parsed' : bool=parsed,
						 		   						  str='parsed_infos' : { int=result_number : { str='address' : str=address,
																									   str='contact_info' : str=contact_info,
																									   str='practice_type' : str=practice_type,
																									   str='practice_detail' : str=practice_detail,
																									   str='gender' : str=gender,
																									   str='languages' : str=languages
																								     }
						 		   					    					   },
						 		   					      str='multiple_results' : bool=mr,
						 		   					      str='num_results' : int=num_results
						 		   					    }
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






###====== <PROGRAM/SCRIPT> ======###

sys.setrecursionlimit(50000)

api_key = "AIzaSyCXXvQOEt31dz8Nw070bye9pwEDBEl0g1o" 
#received 2018/01/24/15:52 kentabaronfuruyama@gmail.com, 1st "BC Doctors1"


file_list = [f for f in os.listdir('data_subsets') if not f.startswith('.')]


search_counter = 0
for subfile in file_list:
	pickle_file = "data_subsets/" + subfile
	data = pickle.load(open(pickle_file, 'rb'))

	num_docs = len(data)
	update_freq = 50
	upload_freq = 100


	counter = 0

	error = False
	error_type = ' = no error set ='

	for doc_key in data:
		
		counter +=1

		doctor = data[doc_key]

		if 'googled' in doctor['GOOGLE']:
			if doctor['GOOGLE']['googled']:
				continue

		doctor['GOOGLE'].update( {'googled':False} )
		doctor['GOOGLE'].update( { 'geo_data':{} } )

		#for each search result
		for result_number in doctor['HTML_PARSING']['parsed_infos']:

			address = doctor['HTML_PARSING']['parsed_infos'][result_number]['address']

			if (address != "" and not address.isspace()):
				url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&region=ca&key=' + api_key
				response = requests.get(url)
				search_counter += 1
				_dict = {result_number: {}}
				_dict.update( {'date_time':datetime.datetime.now()} )
				geocode_results = response.json()

				if geocode_results['status'] != 'OK' and geocode_results['status'] != 'ZERO_RESULTS':
					error_type = geocode_results['status']
					error = True
					break
				else:
					geocode_results = json.dumps(geocode_results)
					_dict.update( {'results':geocode_results} )
					doctor['GOOGLE']['geo_data'].update( _dict )



		if error:
			print('!!! ERROR TOOK PLACE !!!')
			print('== ERROR CODE: ' + error_type + ' ==')
			break

		else:
			doctor['GOOGLE'].update( {'googled':True} )
			if (counter % update_freq == 0):
				print("percentage completed to google for %s is: %s" % (subfile, counter*100/num_docs))
				print('number of queries made is: %s' % (search_counter))
				print("==")
			if (counter % upload_freq == 0):
				pickle.dump(data, open(pickle_file, 'wb'))
				print('..saved..')

	if error:
		break

	pickle.dump(data, open(pickle_file, 'wb'))

###====== </PROGRAM/SCRIPT> ======###
