from plotly.offline import iplot
import plotly.graph_objs as go
import plotly

from pycpd import deformable_registration

import numpy as np
import numpy.matlib

#plotly.offline.init_notebook_mode()

from dataReader import primaryRead, XYZ, rotation
from pivotCalibration import pivotCalib

#from VizTool import visualize

###

data = primaryRead('Data/pc.txt')

pos = XYZ(data[1])
start = 420
end = len(pos) - 250

pos = XYZ([data[1][i] for i in range(start, end)])
print(len(pos),(pos[0].shape))


x = [pos[i][0,0] for i in range(0, len(pos))]
y = [pos[i][0,1] for i in range(0, len(pos))]
z = [pos[i][0,2] for i in range(0, len(pos))]

rot = rotation([data[1][i] for i in range(start, end)])
print(len(rot),(rot[0].shape))

p_tip, p_dimple = pivotCalib(pos,rot)

###

flat = primaryRead('Data/clampedFlat.txt')
curv = primaryRead('Data/clampedCurved.txt')
sshape = primaryRead('Data/clampedSshape.txt')

flat_pos = XYZ(flat[1])
flat_rot = rotation(flat[1])

curv_pos = XYZ(curv[1])
curv_rot = rotation(curv[1])

sshape_pos = XYZ(sshape[1])
sshape_rot = rotation(sshape[1])

flat_trans = []
curv_trans = []
sshape_trans = []

for i in range(len(flat_pos)):
    flat_trans.append( flat_pos[i] + (flat_rot[i] * p_tip).T )
    
for i in range(len(curv_pos)):
    curv_trans.append( curv_pos[i] + (curv_rot[i] * p_tip).T )
    
for i in range(len(sshape_pos)):
    sshape_trans.append( sshape_pos[i] + (sshape_rot[i] * p_tip).T )

#visualize([flat_trans[0:-70]])
#visualize([curv_trans[95:-120]])
#visualize([sshape_trans[130:-80]])

###

#%matplotlib inline
from functools import partial
from scipy.io import loadmat
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pycpd import deformable_registration
import numpy as np
import time

def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:,0],  X[:,1], X[:,2], color='red')
    ax.scatter(Y[:,0],  Y[:,1], Y[:,2], color='blue')
    plt.draw()
    print("iteration %d, error %.5f" % (iteration, error))
    plt.pause(0.001)

def main(): 
    flat = np.array(flat_trans[0:-70])
    flat = flat.reshape((np.size(flat,0), np.size(flat,2)))
    print(np.shape(flat))

    curv = np.array(curv_trans[95:-120])
    curv = curv.reshape((np.size(curv,0), np.size(curv,2)))

    sshape = np.array(sshape_trans)

    X = np.zeros((flat.shape[0], flat.shape[1] + 1))
    X[:,:-1] = flat

    Y = np.zeros((curv.shape[0], curv.shape[1] + 1))
    Y[:,:-1] = curv

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    callback = partial(visualize, ax=ax)

    reg = deformable_registration(X, Y)
    reg.register(callback)
    plt.show()

if __name__ == '__main__':
    main()
