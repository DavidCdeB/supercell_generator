#

import numpy as np
import itertools
import sys
import pdb
from itertools import product
import glob
import os

path='./'
filename = os.path.join(path, '*.out')
#filename = glob.glob(name)
for fname in glob.glob(filename):
  print fname

P0 = []
P1 = []
P2 = []

with open(fname) as gout:
#   final_optimized_geometry = False
    for line in gout:
        if 'DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)' in line:
            final_optimized_geometry = True
            done = gout.next()
            done = gout.next()
            print 'done = ', done

            p00 = done.split()[0]
            P0.append(p00)

            p01 = done.split()[1]
            P0.append(p01)

            p02 = done.split()[2]
            P0.append(p02)
     
            print 'p00 = ', p00

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

print 'P0 = ', P0
print 'type(P0) = ', type(P0)
for i in P0:
 print type(i)

P0 = np.array(P0)
P1 = np.array(P1)
P2 = np.array(P2)
print 'P0 = ', P0
print 'type(P0) = ', type(P0)
for i in P0:
 print type(i)

P0 = P0.astype(np.float)
P1 = P1.astype(np.float)
P2 = P2.astype(np.float)
print 'P0 = ', P0
print 'type(P0) = ', type(P0)
for i in P0:
 print type(i)

print 'shape(P2) = ', np.shape(P2)

A = np.vstack((P0, P1, P2))
print 'A array = ', A
print 'shape(A array) = ', np.shape(A)



# Alternative, you can provide here the direct matrix lattice vectors (primitive cell):
# Aragonite:
#A =np.array([[0.496160000000e+01,   0.000000000000e+00 ,  0.000000000000e+00],
#             [0.000000000000e+00,   0.797050000000e+01,   0.000000000000e+00],
#             [0.000000000000e+00,   0.000000000000e+00,   0.573940000000e+01]])

# True description of calcite II:
#A =np.array([[   0.606983596000E+01,   0.371670258988E-15,   0.000000000000E+00 ],   
#             [   0.000000000000E+00,   0.501688998000E+01,   0.000000000000E+00 ],
#             [  -0.196296039941E+01,   0.459955262889E-15,   0.725062164908E+01 ]])


print 'A =  ', A
print 'shape(A array) = ', np.shape(A)
#sys.exit()

print 'A[0][0] =  ', A[0][0]
print 'A[0][1] =  ', A[0][1]
print 'A[0][2] =  ', A[0][2]

# Direct matrix lattice vectors (primitive cell):
# Calcite I:
#A =np.array([[   0.288155519353E+01,   0.000000000000E+00,   0.568733333333E+01],
#             [  -0.144077759676E+01,   0.249550000000E+01,   0.568733333333E+01],
#             [  -0.144077759676E+01,  -0.249550000000E+01,   0.568733333333E+01]])

# Supercell expansion matrix generator:
# Calcite I:
K = 3
N = 3
#E = [np.reshape(np.array(i), (K, N)) for i in itertools.product([0, 2], repeat = K*N)]

# Supercell expansion matrix generator:
# Aragonite:
K = 3
N = 3
#E = [np.reshape(np.array(i), (K, N)) for i in itertools.product([0, 1, -1, 2, -2], repeat = K*N)]
E = [np.reshape(np.array(i), (K, N)) for i in itertools.product([0, 1, -1], repeat = K*N)]



tol_1 = 10
#tol_2 = 1E-8
#tol_2 = 1E-7
#tol_2 = 1E-6
#tol_2 = 1E-5
#tol_2 = 1E-4
#tol_2 = 1E-3
#tol_2 = 1E-2
#tol_2 = 1E-1
tol_2 = 1

print "tol_2 = ", tol_2
print 'type(E) = ', type(E) # Each E candidate is saved in a list
#print 'E = ', E            # If you want to check all possible combinations.
print 'len(E) = ', len(E)   # No. combinations = (#integers)**9 
sys.exit()

for indx_E in E:
#     print 'type(indx_E) = ', type(indx_E) # They're already a <numpy.ndarray>
#     indx_E = np.asarray(indx_E)  # Each indx_E is already a <numpy.ndarray>; there is no need to convert. 
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

      if  a1_SC > tol_1\
          and a2_SC > tol_1\
          and a3_SC > tol_1\
          and abs(a1_SC - a2_SC) <= tol_2\
          and abs(a1_SC - a3_SC) <= tol_2\
          and abs(a2_SC - a3_SC) <= tol_2\
          and det_indx_E > 0.0:
             print 'A_SC = ', A_SC

             print 'a1_SC = ', a1_SC
             print 'a2_SC = ', a2_SC
             print 'a3_SC = ', a3_SC
             print 'det_indx_E = ', det_indx_E 
             E_sol = np.dot(A_SC, np.linalg.inv(A))
             print 'E_sol = ', E_sol
             print 'END ++++++++++' 
#              

