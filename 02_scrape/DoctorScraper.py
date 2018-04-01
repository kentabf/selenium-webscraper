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

class DoctorScraper:

	def __init__(self, dictionary):
		self.doctor = dictionary
		self.doctor['SCRAPING'].update({ 'done_search':False, 'pages':[] })
		self.meta = {}

	def search(self):

		
		url = 'https://www.cpsbc.ca/physician_search'
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
