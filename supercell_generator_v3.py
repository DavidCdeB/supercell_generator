#

import numpy as np
import itertools
import sys
import pdb
from itertools import product
import glob
import os
import math

path='./'
filename = os.path.join(path, '*.out')
for fname in glob.glob(filename):
  print fname

P0 = []
P1 = []
P2 = []

with open(fname) as gout:
    for line in gout:
        if 'DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)' in line:
            final_optimized_geometry = True
            done = gout.next()
            done = gout.next()

            p00 = done.split()[0]
            P0.append(p00)

            p01 = done.split()[1]
            P0.append(p01)

            p02 = done.split()[2]
            P0.append(p02)
     
            done = gout.next()

            p10 = done.split()[0]
            P1.append(p10)

            p11 = done.split()[1]
            P1.append(p11)

            p12 = done.split()[2]
            P1.append(p12)

            done = gout.next()

            p20 = done.split()[0]
            P2.append(p20)

            p21 = done.split()[1]
            P2.append(p21)

            p22 = done.split()[2]
            P2.append(p22)

P0 = np.array(P0)
P1 = np.array(P1)
P2 = np.array(P2)

P0 = P0.astype(np.float)
P1 = P1.astype(np.float)
P2 = P2.astype(np.float)

A = np.vstack((P0, P1, P2))
print 'A array = ', A



# Alternatively, you can provide here the direct matrix lattice vectors (primitive cell):
# Aragonite:
#A =np.array([[0.496160000000e+01,   0.000000000000e+00 ,  0.000000000000e+00],
#             [0.000000000000e+00,   0.797050000000e+01,   0.000000000000e+00],
#             [0.000000000000e+00,   0.000000000000e+00,   0.573940000000e+01]])


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

vector = P0
print 'unit_vector(vector) = ', unit_vector(vector)



#sys.exit()

# Supercell expansion matrix generator:
K = 3
N = 3
E = [np.reshape(np.array(i), (K, N)) for i in itertools.product([0, 1, -1, 2, -2], repeat = K*N)]

tol_1=10
tol_2=2
tol_3=50

print "tol_1 = ", tol_1
print "tol_2 = ", tol_2
print 'type(E) = ', type(E) # Each E candidate is saved in a list
print 'len(E) = ', len(E)   # No. combinations = (#integers)**9 

for indx_E in E:
      A_SC = np.dot(indx_E,A)
      a1_SC = np.linalg.norm(A_SC[0])
      a2_SC = np.linalg.norm(A_SC[1])
      a3_SC = np.linalg.norm(A_SC[2])

      det_indx_E = np.linalg.det(indx_E)

#     If you want to print each iteration, uncomment this block:
#     print 'a1_SC = ', a1_SC
#     print 'a2_SC = ', a2_SC
#     print 'a3_SC = ', a3_SC
#     print 'det_indx_E = ', det_indx_E

#     print  abs(a1_SC - a2_SC) == tol_2  # All False, thus we have to use <=
#     print  abs(a1_SC - a2_SC) <= tol_2

#     Calculation of angles:
      alpha = angle_between(A_SC[1], A_SC[2])
      beta = angle_between(A_SC[0], A_SC[2])
      gamma = angle_between(A_SC[0], A_SC[1])
      
      alpha_deg = alpha*180/math.pi
      beta_deg = beta*180/math.pi  
      gamma_deg = gamma*180/math.pi  
 
      if  a1_SC > tol_1\
          and a2_SC > tol_1\
          and a3_SC > tol_1\
          and abs(a1_SC - a2_SC) <= tol_2\
          and abs(a1_SC - a3_SC) <= tol_2\
          and abs(a2_SC - a3_SC) <= tol_2\
          \
          and abs(alpha_deg - beta_deg) <= tol_3\
          and abs(alpha_deg - gamma_deg) <= tol_3\
          and abs(beta_deg - gamma_deg) <= tol_3\
          \
          and det_indx_E > 0.0:
             print 'A_SC = ', A_SC

             print 'a1_SC = ', a1_SC
             print 'a2_SC = ', a2_SC
             print 'a3_SC = ', a3_SC
            
             print 'alpha_deg = ', alpha_deg
             print 'beta_deg = ', beta_deg
             print 'gamma_deg = ', gamma_deg

             print 'det_indx_E = ', det_indx_E 
             E_sol = np.dot(A_SC, np.linalg.inv(A))
             E_sol_int = E_sol.astype(int)  
             print 'Supercell Expansion Matrix = '
             print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
                   for row in E_sol_int]))

             print 'END ++++++++++' 
#              

# Redirect to an output, i.e python *py > *out
# Search for the candidate in the *out as:
# pcregrep -M "\[\[ 1  2  1].*\n.*\[ 0  2  1].*\n.*\[-1  0  1]]" calcite_14__tol2_2.out

# BETTER:
# pcregrep -n -M "   0   0  -1.*\n.*  -1   1   0.*\n.*   2  -2   0" calcite_14__tol2_2.out


