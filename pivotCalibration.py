'''
Manyu Sharma 
Rohit Joshi
CIS 2
3D Pivot calibration
'''

import numpy as np
import numpy.matlib


def pivotCalib(Pos,Rot):
	''' Function to perform pivot calibration of tool given set of measurements
	
	Pos is a list of numpy matricies, each matrix being a sequential frame
	representing an individual point position.

	Rot is a list of numpy matricies, each matrix being a sequential frame
	representing an individual rotation.
	
	Returns the tip of of the tool in coordinate frame of the tool
	'''

	# Find all transforms relative to first frame
	n = len(Rot)
	
	R_lstsq = numpy.matlib.zeros((n * 3, 6)) # Matrix for rotations and neg identity
	p_lstsq = numpy.matlib.zeros((n * 3, 1)) # Column vector for displacements
	
	
	for i in range(n):
		R = Rot[i]
		p = Pos[i]
		negativeIdentity = np.matrix([(-1,0,0),(0,-1,0),(0,0,-1)])
		R = np.append(R,negativeIdentity,1)
		R_lstsq[i * 3 : i * 3 + 3] = R 			# Building up linear system
		p_lstsq[i * 3 : i * 3 + 3] = -p.T

	# Solve overdetermined system
	solution = np.linalg.lstsq(R_lstsq,p_lstsq)

	# Break solution into top and bottom half
	p_tip = solution[0][0:3]
	p_dimple = solution[0][3:6]

	return p_tip, p_dimple