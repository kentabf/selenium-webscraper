
###====== <DICTIONARY ORGANIZATION> ======###
'''

data
{ tuple(str,str)=(fname,lname) : { str='RECORDS' : { int=year:str=salary },
						 		   str='SCRAPING' : { },
						 		   str='GOOGLE' : { }
								 }
}

metadata
{ str='search_domains' : { int=num_threads : array[(str,str)]=search_subset },
  str='data' : {  }
}
	
'''
###====== </DICTIONARY ORGANIZATION> ======###