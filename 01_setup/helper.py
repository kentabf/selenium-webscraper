

#to seaparate an array into n subset arrays
#credit: https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def chunkify(lst, n):
	return [lst[i::n] for i in range(n)]


