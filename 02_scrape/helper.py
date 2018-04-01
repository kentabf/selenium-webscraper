import math

#to seaparate an array into n subset arrays
#credit: https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def chunkify(lst, n):
	return [lst[i::n] for i in range(n)]


#function no longer used, kept here just in case
#mainly does what chunkify above does (but linearly)
def my_split(search_array, num_to_split):
	length = len(search_array)
	split_length = math.floor(length/num_to_split)
	index_array = []
	index_counter = 0
	for i in range(0, num_to_split):
		if i != (num_to_split-1):
			index_array.append({'start':index_counter, 'end':(index_counter+split_length-1)})
			index_counter = index_counter + split_length
		else:
			index_array.append({'start':index_counter, 'end':(length - 1)})
	return index_array
