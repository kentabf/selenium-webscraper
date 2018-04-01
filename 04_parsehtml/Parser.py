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



class Parser:

	def __init__(self, doct_data):
		self.doc_data = doc_data

	def parse_pages():

		self.doc_data.update( { 'HTML_PARSING': { 'parsed':False, 'parsed_infos':{} } })

		#if not searched, return and don't parse -- should be searched for all
		if not self.doc_data['SCRAPING']['done_search']:
			return

		#if parsed, return and don't parse
		if self.doc_data['HTML_PARSING']['parsed']:
			return

		
		num = 1

		#parse per page
		for page in self.doc_data['SCRAPING']['pages']:
			infos = parse_page(page, num)
			num += len(infos)
			self.doc_data['HTML_PARSING']['parsed_infos'].update( infos )

		#update info on number of results
		num_info = len(self.doc_data['HTML_PARSING']['parsed_infos'])
		mr = False
		if num_info>1:
			mr = True
		self.doc_data['HTML_PARSING'].update( { 'multiple_results':mr, 'num_results':num_info } )
		if len(self.doc_data['SCRAPING']['pages']) == 0:
			self.doc_data['HTML_PARSING'].update( { 'parsed_infos':0 } )

		#final boolean update
		self.doc_data['HTML_PARSING'].update( { 'parsed':True } )
		
	def parse_page(page, num):
		infos = {}

		soup = BeautifulSoup(page, 'lxml')
		table = soup.find('table', class_='sticky-enabled tableheader-processed sticky-table')
		table_body = table.find('tbody')
		table_rows = table_body.find_all('tr')
		
		result_number = num

		#parse per row of result
		for row in table_rows:
			info = { result_number:parse_row(row) }
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

		#update the dicionary object
		info.update( { 'address':address, 'contact_info':contact_info,
			'practice_type':practice_type, 'practice_detail':practice_detail,
			'gender':gender, 'status':status, 'languages':languages } )

		return info




