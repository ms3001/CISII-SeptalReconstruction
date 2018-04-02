import csv
import numpy as np
import numpy.matlib

def primaryRead(filename):
	'''
	Returns a list of data lists. 

	'''
	d = []
	with open(filename) as f:
		reader = csv.reader(f, delimiter="\t")
		d = list(reader)

	
	n = len(d[0]) // 17
	rows = len(d)

	output = []

	for i in range(n):
		temp = []
		for j in range(rows):
			temp.append(d[j][i * 17 : 17 + i * 17])
		output.append(temp)

	return output

def XYZ(rawDataCol):
	'''
	Returns a list of N numpy matricies, each (1 x 3). 

	'''
	out = []
	for row in rawDataCol:
		out.append(  np.matlib.matrix( [float(row[i]) for i in range(4,7)] )  )

	return out

def rotation(rawDataCol):
	'''
	Returns a list of N numpy matricies, each (3 x 3). 

	'''
	out = []
	for row in rawDataCol:

		r = [ [float(row[7]),float(row[8]),float(row[9])] , [float(row[10]),float(row[11]),float(row[12])] , [float(row[13]),float(row[14]),float(row[15])] ]
		out.append(  np.matlib.matrix(r)  )

	return out