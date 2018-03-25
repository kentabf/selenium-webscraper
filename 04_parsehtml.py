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
import os
import time
import numpy as np
import multiprocessing as mp
import threading
import math
import datetime
import json


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
						 		   str='GOOGLE' : { },
						 		   str='HTML_PARSING' : { str='parsed' : bool=parsed,
						 		   						  str='parsed_infos' : { int=page_number : { str='address' : str=address,
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







###====== <DEFINITIONS> ======###

def parse_pages(doc_data):

	doc_data.update( { 'HTML_PARSING': { 'parsed':False, 'parsed_infos':{} } })

	#if searched, return and don't parse -- should be searched for all
	if not doc_data['SCRAPING']['done_search']:
		return

	#if parsed, return and don't parse
	if doc_data['HTML_PARSING']['parsed']:
		return

	
	num = 1

	for page in doc_data['SCRAPING']['pages']:
		infos = parse_page(page, num)
		num += len(infos)
		doc_data['HTML_PARSING']['parsed_infos'].update( infos )

	#info on number of results
	num_info = len(doc_data['HTML_PARSING']['parsed_infos'])
	mr = False
	if num_info>1:
		mr = True
	doc_data['HTML_PARSING'].update( { 'multiple_results':mr, 'num_results':num_info } )
	if len(doc_data['SCRAPING']['pages']) == 0:
		doc_data['HTML_PARSING'].update( { 'parsed_infos':0 } )
	doc_data['HTML_PARSING'].update( { 'parsed':True } )
	
def parse_page(page, num):
	infos = {}

	soup = BeautifulSoup(page, 'lxml')
	table = soup.find('table', class_='sticky-enabled tableheader-processed sticky-table')
	table_body = table.find('tbody')
	table_rows = table_body.find_all('tr')
	
	counter = num
	for row in table_rows:
		info = { counter:parse_row(row) }
		infos.update( info )
		counter += 1

	return infos

def parse_row(row):

	info = {}

	entries = row.find_all('td')

	#for address
	first_col = entries[0]
	address_data = first_col.find('div', class_='physio-address-data')
	address_lines = []
	if (address_data != None):
		address_lines = address_data.find_all(text=True)
	address = ''
	for line in address_lines:
		address = address + line + '\n'
	address = str(address)

	#for phone number
	contact_lines = []
	temp = first_col.find('li', class_='first last')
	if (temp != None):
		contact_lines = list(temp.children)
	contact_info = ''
	if len(contact_lines)>1:
		contact_info = contact_lines[1]
	contact_info = str(contact_info)

	#for practice type and detail
	second_col = entries[1]
	practice_type = ''
	if (second_col.children != None and len(list(second_col.children))>0):
		practice_type = list(second_col.children)[0]
	practice_detail_ul = second_col.find('ul', class_='specialty_list')
	practice_detail_lines= []
	if (practice_detail_ul != None):
		practice_detail_lines = practice_detail_ul.find_all(text=True)
	practice_detail = ''
	for line in practice_detail_lines:
		practice_detail = practice_detail + line + '\n'
	practice_detail = str(practice_detail)

	#for gender
	gender = entries[2].text
	gender = str(str)

	#for accepting new patients
	status = entries[3].text
	status = str(status)

	#for additional languages
	languages = entries[4].text
	languages = str(languages)

	info.update( { 'address':address, 'contact_info':contact_info,
		'practice_type':practice_type, 'practice_detail':practice_detail,
		'gender':gender, 'status':status, 'languages':languages } )

	return info

###====== </DEFINITIONS> ======###






###====== <PROGRAM/SCRIPT> ======###

#Increase limit to handle the increase in depth/width of dictionary objects
sys.setrecursionlimit(50000)

#Recall we divided up the data into multiple pickle files
file_list = [f for f in os.listdir('data_subsets') if not f.startswith('.')]

num_files = len(file_list)

counter = 0
for subfile in file_list:
	counter += 1

	pickle_file = "data_subsets/" + subfile

	data = pickle.load(open(pickle_file, 'rb'))

	num_docs = len(data)

	for doctor in data:
	
		parse_pages(data[doctor])

	pickle.dump(data, open(pickle_file, 'wb'))
	print("finished parsing %s , %s left to go out of %s " % (subfile, str(num_files-counter), str(num_files)))

###====== </PROGRAM/SCRIPT> ======###

