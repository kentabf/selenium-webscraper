try:
	import _pickle as pickle
except:
	import pickle
import csv
import sys
import os
import multiprocessing as mp

import MultiParser as MP
import Parser as P
import helper as h


def run_process(file_set):

	multiparser = MP.MultiParser(file_set)
	multiparser.start_process()

def run_component():

	#increase limit to handle the increase in depth/width of dictionary objects
	sys.setrecursionlimit(50000)

	#recall we divided up the data into multiple pickle files
	file_list = [f for f in os.listdir('data/data_subsets') if not f.startswith('.')]

	#set the number of processes
	num_proc = 5

	#divide files into (roughly) even number of num_proc
	file_sets = h.chunkify(file_list, num_proc)

	proc_list = []

	for file_set in file_sets:
		proc = mp.Process(target=run_process, args=(file_set,))
		proc_list.append(proc)
	for proc in proc_list:
		proc.start()
	for proc in proc_list:
		proc.join()


