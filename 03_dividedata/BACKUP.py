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
import datetime
import json


###====== <PROGRAM/SCRIPT> ======###
# cd 'Dropbox (Econ)/CanadianDoctors/British Columbia/scrape'

pickle_file = 'data.pickle'

#choose number of subfiles
num_subsets = 100

for x in range(1, num_subsets+1):
	sub_filename = "data_subsets/data" + str(x) + ".pickle"
	open(sub_filename, 'w').close()

data = pickle.load(open(pickle_file, 'rb'))

num_entry = len(data)
counter = 1
subset_counter = 1
subset_size = math.floor(num_entry/num_subsets)
subset = {}
array = []
for entry in data:

	subset.update( {entry:data[entry]} )
	counter += 1

	#hit the limit
	if counter == subset_size:

		#for any non-last subfile
		if subset_counter < num_subsets:
			
			array.append(subset)
			subset = {}
			counter = 0
			subset_counter += 1

#last subfile
array.append(subset)

counter = 1
for subset_data in array:
	pickle_subfile = "data_subsets/data" + str(counter) + ".pickle"
	pickle.dump(subset_data, open(pickle_subfile, 'wb'))
	counter+=1
###====== </PROGRAM/SCRIPT> ======###


