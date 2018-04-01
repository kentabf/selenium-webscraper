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

import helper as h

def my_f(lst):
	arr = []
	for elem in lst:
		arr.append(elem*elem)
	raise Exception('my erorrr')
	print(arr)

def multi():
	lst = [i for i in range(300)]

	num_proc = 1
	array_sets = h.chunkify(lst, num_proc)

	proc_list = []

	for array_set in array_sets:
		proc = mp.Process(target=my_f, args=(array_set,))
		proc_list.append(proc)
	for proc in proc_list:
		proc.start()
	for proc in proc_list:
		proc.join()

multi()


