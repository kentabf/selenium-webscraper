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

import Parser as P


class MultiParser:

	def __init__(self, file_set):
		self.file_set = file_set
		self.interval = 100

	def start_process():

		for file_set in self.file_set:

			pickle_file = "data/data_subsets/" + file_set

			data = pickle.load(open(pickle_file, 'rb'))

			counter = 0
			for doctor in data:

				counter += 1

				parser = P.Parser(data[doctor])
				parser.parse_pages()

				if (counter % self.interval == 0):
					pickle.dump(data, open(pickle_file, 'wb'))

			pickle.dump(data, open(pickle_file, 'wb'))
			print('finished parsing %s' % (file_set))




	


