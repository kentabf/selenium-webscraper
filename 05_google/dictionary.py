
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