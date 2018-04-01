try:
	import _pickle as pickle
except:
	import pickle
import json
import time
import datetime
import requests


class Geocode:

	def __init__(self, api_key, address):
		self.api_key = api_key
		self.address = address
		self._dict = {}

	def search():

		#as per googlemaps geocode API
		url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + self.address + '&region=ca&key=' + self.api_key
		response = requests.get(url)
		
		#keep time of geocode request made, just in case
		self._dict.update( {'date_time':datetime.datetime.now()} )

		#convert to json format, as per googlemaps recommendation/API
		geocode_results = response.json()
		
		results_handler(geocode_results)

	def results_handler(geocode_results):

		status = geocode_results['status']

		#handle the case that a result (or empty result) wasn't returned
		if not (status == 'OK' and status == 'ZERO RESULTS'):
			raise Exception('Exception raised. Status was: ' + status)

		#convert to string
		geocode_results = json.dumps(geocode_results)

		self._dict.update( { 'results': geocode_results } )




