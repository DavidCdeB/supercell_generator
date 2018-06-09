# Table of Contents

<!-- - [What is the QHA program ?](#WhatisQHA)
- [What is the quasi-harmonic approximation ?](#Whatisquasi) -->
1. [What is the `supercell_generator` program ?](#example)
4. [Why is the `supercell_generator` useful ?](#example2)
3. [Statement of the problem](#example3)
4. [How to run `supercell_generator`](#example4)
5. [Test](#example5)
6. [How to cite](#example6)
7. [Contributing](#example7)



<a name="example"></a>
# What is the `supercell_generator.py` program ?]

Given a direct matrix lattice vectors, this program creates a set of supercell matrix candidates for which the new lattice parameters (`a1_SC`, `a2_SC`, `a3_SC`) are greater than a chosen value, and the three of them of the same size, within a tolerance.

This allows to construct supercells for different polymorphs with lattice parameters of equal legth, so that we ensure phonons are calculated within a "sphere" of equal radius.

<a name="example2"></a>
# Why is the `supercell_generator` useful ? 

Let's consider this example:

Calcite I is a trigonal crystal, where the primitive cell is trigonal, and the crystallographic is hexagonal. This is the direct lattice vectors matrix for the primitive cell:

```
 DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)
          X                    Y                    Z
   0.288155519353E+01   0.000000000000E+00   0.568733333333E+01
  -0.144077759676E+01   0.249550000000E+01   0.568733333333E+01
  -0.144077759676E+01  -0.249550000000E+01   0.568733333333E+01
```
Which would be an adequate supercell that would produce the three lattice parameters `a1_SC`, `a2_SC` and `a3_SC` approximately equal and greater than 10 Angstrom?

Well, in this case, the following supercell:

```
2 0 0
0 2 0
0 0 2
```
will produce the following:

`a1_SC = a2_SC = a3_SC = 12.88458   12.88458   12.88458`

This was a simple case. Now, consider Aragonite, in which the primitive cell is orthorombic, and the direct lattice vectors matrix is:

 ```
 DIRECT LATTICE VECTORS CARTESIAN COMPONENTS (ANGSTROM)
          X                    Y                    Z
   0.496160000000E+01   0.000000000000E+00   0.000000000000E+00
   0.000000000000E+00   0.797050000000E+01   0.000000000000E+00
   0.000000000000E+00   0.000000000000E+00   0.573940000000E+01
```
In this case it is not so straightforward which would be the minimum volume supercell that would produce `a1_SC`, `a2_SC` and `a3_SC` approximately equal and greater than 10 Angstrom. It is this following supercell:

```
-1   1  -1
-1  -1   1
-1  -1  -1
```

that will produce the following:

`a1_SC = a2_SC = a3_SC = 11.00396   11.00396   11.00396`. This supercell is not that easy to sort it out... The goal of this program is to sort out this supercell for any given direct lattice matrix vectors.

<a name="example3"></a>
# Statement of the problem

Given the matrices `{aij}`, `{Eij}` and `{aij_SC}`, it is satisfied that:

```
  |a1x_SC a1y_SC  a1z_SC|           |E11 E12  E13|           |a1x a1y  a1z|  
  |a2x_SC a2y_SC  a2z_SC|   =       |E21 E22  E23|     x     |a2x a2y  a2z|    
  |a3x_SC a3y_SC  a3z_SC|           |E31 E32  E33|           |a3x a3y  a3z|  
 \-----------------------/         \--------------/         \--------------/  
    {aij_SC} matrix                  {Eij} matrix             {aij} matrix
    (i=1,2,3; j=x_SC,y_SC,z_SC)      (i,j=1,2,3)             (i=1,2,3; j=x,y,z)
                                                                Known
```


where `x` stands for a standard matrix multiplication (rows, columns).

In other words:

<p align="center">
  <img src="https://github.com/DavidCdeB/supercell_generator/blob/master/Images_for_README/65.png">
</p>

<!-- -
[![enter image description here][2]][2] -->

<p align="center">
  <img src="https://github.com/DavidCdeB/supercell_generator/blob/master/Images_for_README/64.png">
</p>

<!-- 
[![enter image description here][3]][3] -->

**1)** Each element of `{aij}` matrix is known:

``` 
a1x = 0.288155519353E+01
a1y = 0.000000000000E+00
a1z = 0.568733333333E+01
    
a2x = -0.144077759676E+01             # Eqns(1)
a2y = 0.249550000000E+01
a2z = 0.568733333333E+01
    
a3x = -0.144077759676E+01
a3y = -0.249550000000E+01
a3z = 0.568733333333E+01
```

**2)** Each element of `{Eij}` is a list of possible integer values, the same for each element:

```
E11 = [0, 1, 2, -1, -2]
E12 = [0, 1, 2, -1, -2]
E13 = [0, 1, 2, -1, -2]
    
E21 = [0, 1, 2, -1, -2]              
E22 = [0, 1, 2, -1, -2]              # Eqns(2)
E23 = [0, 1, 2, -1, -2]
    
E31 = [0, 1, 2, -1, -2]
E32 = [0, 1, 2, -1, -2]
E33 = [0, 1, 2, -1, -2]
```

**3)** `a1_SC`, `a2_SC` and `a3_SC` are calculated in the following way:

```
a1_SC =  (a1x_SC**2 + a1y_SC**2 + a1z_SC**2)**(0.5)
a2_SC =  (a2x_SC**2 + a2y_SC**2 + a2z_SC**2)**(0.5)    # Eqns(3)
a3_SC =  (a3x_SC**2 + a3y_SC**2 + a3z_SC**2)**(0.5)
```

I would like to brute force loop over all possible `Eij` values (Eqns(2)) so that I can find those `Eij` for which:

<!--
<p align="center">
  <img src="https://github.com/DavidCdeB/supercell_generator/blob/master/Images_for_README/67.png">
</p> -->

```
a1_SC ~= a2_SC ~= a3_SC > 10
```

<!-- 
[![enter image description here][1]][1] -->

In reality, I am imposing two conditions: 
* Lattice parameter of the supercell to be similar (within a tolerance) AND 
greater than a value.
The following function implements this double condition:

```
def tolerance(a1_SC, a2_SC, a3_SC):
    tol_1 = 10
    tol_2 = 0.001
    return a1_SC > tol_1\
           and a2_SC > tol_1\
           and a3_SC > tol_1\
           and abs(a1_SC - a2_SC) < tol_2\
           and abs(a1_SC - a3_SC) < tol_2\ 
           and abs(a2_SC - a3_SC) < tol_2
```
When it comes the time to calculate:

```
a1x_SC = E11 * a1x + E12 * a2x + E13 * a3x
a1y_SC = E11 * a1y + E12 * a2y + E13 * a3y
a1z_SC = E11 * a1z + E12 * a2z + E13 * a3z

a2x_SC = E21 * a1x + E22 * a2x + E23 * a3x           # Eqns (4)
a2y_SC = E21 * a1y + E22 * a2y + E23 * a3y
a2z_SC = E21 * a1z + E22 * a2z + E23 * a3z

a3x_SC = E31 * a1x + E32 * a2x + E33 * a3x
a3y_SC = E31 * a1y + E32 * a2y + E33 * a3y
a3z_SC = E31 * a1z + E32 * a2z + E33 * a3z
```

There is this problem: considering what has been said above, it would be necessary to loop over the 5 possible values of `E11` (`E11 = [0, 1, 2, -1, -2]`), while  `E12`, `E13`, `E21`, `E22`, `E23`, `E31`, `E32` and `E33` remain the same. Something like:

```
    for e11 in E11:
      a1x_SC = e11 * a1x + E12[0] * a2x + E13[0] * a3x
      a1y_SC = e11 * a1y + E12[0] * a2y + E13[0] * a3y
      a1z_SC = e11 * a1z + E12[0] * a2z + E13[0] * a3z
    
      a2x_SC = E21[0] * a1x + E22[0] * a2x + E23[0] * a3x           # Eqns (5)
      a2y_SC = E21[0] * a1y + E22[0] * a2y + E23[0] * a3y
      a2z_SC = E21[0] * a1z + E22[0] * a2z + E23[0] * a3z
    
      a3x_SC = E31[0] * a1x + E32[0] * a2x + E33[0] * a3x
      a3y_SC = E31[0] * a1y + E32[0] * a2y + E33[0] * a3y
      a3z_SC = E31[0] * a1z + E32[0] * a2z + E33[0] * a3z
    
      #####
    
      a1x_SC = e11 * a1x + E12[1] * a2x + E13[1] * a3x
      a1y_SC = e11 * a1y + E12[1] * a2y + E13[1] * a3y
      a1z_SC = e11 * a1z + E12[1] * a2z + E13[1] * a3z
    
      a2x_SC = E21[1] * a1x + E22[1] * a2x + E23[1] * a3x           # Eqns (6)
      a2y_SC = E21[1] * a1y + E22[1] * a2y + E23[1] * a3y
      a2z_SC = E21[1] * a1z + E22[1] * a2z + E23[1] * a3z
    
      a3x_SC = E31[1] * a1x + E32[1] * a2x + E33[1] * a3x
      a3y_SC = E31[1] * a1y + E32[1] * a2y + E33[1] * a3y
      a3z_SC = E31[1] * a1z + E32[1] * a2z + E33[1] * a3z

      .
      .
      .

```

but this would not be considering all the possible combinations, because for a given `e11`, for instance, it is also valid:

```
a1x_SC = e11 * a1x + E12[0] * a2x + E13[0:-1] * a3x
```
This is very cumbresome.

An alternative solution, the one finally adopted,
is to create all the possible 3x3 integer matrices
that can be constructed with integers being +1, -1, 2, -2.
The number of candidate matrices is then: `(Number of integers)**9`.
For example:
* If there are 3 integers: `[0, 1, -1]` there will be a total number of `19683` 3x3 supercell expansion matrices candidates.
* If there are 5 integers: `[0, 1, -1, 2, -2]` there will be a total number of `1953125` 3x3 supercell expansion matrices candidates.


<a name="example3"></a>
# How to run `supercell_generator`. A guided tour

* Get the code: `git clone https://github.com/DavidCdeB/supercell_generator`
* Copy to the `supercell_generator` folder, any output for a single point calculation in the primitive cell.
* The code will grab the direct matrix lattice vectors from this output.
* Remember that name of all ths output has to end in `*.out`
* Alternatively, you can hard code directly the direct matrix lattice vectors (primitive cell) in the variable `A`.

* The default is to search supercell expansion matrices given by the integers 0, 1, -1. If you would like to use also integers +2 and -2, edit the `supercell_generator.py` code, the line 

```
itertools.product([0, 1, -1]
```
should be changed by

```
itertools.product([0, 1, 2, -1, -2]
```

* Set two tolerances. Remember this condition:

```
a1_SC ~= a2_SC ~= a3_SC > tol_1
```
    * `tol_1` controls how big the lattice parameters are. Tipically this value is 10 Angtrom. This is the default in the program.

    * `tol_2` controls how similar are the lattice parameters. Typically this value is 1E-6, although it can be stricter. This is the default in the program.

* Run `./supercell_generator.sh`

If you run this program in the `TEST` folder, you will have the oppotunity to test this on Aragonite. The output is the following:

``` 
./aragonite_SINGLE_POINT.out
```
> This confirms that the output is being read.

```
A array =  [[ 4.9616  0.      0.    ]
 [ 0.      7.9705  0.    ]
 [ 0.      0.      5.7394]]
```
> This tells you the direct matrix of lattice parameters that has been extracted.

```
tol_1 =  10
tol_2 =  0.01
```
> This confirms the tolerances being used.

```
len(E) =  19683
```
> This confirms the number of matrices candidates for a combination of integers `0, 1, -1`.

At this point, all the sucessful candidates will be printed:

> The direct lattice vectors of the supercell:
```
A_SC =  [[ 4.9616  7.9705  5.7394]
 [ 4.9616  7.9705 -5.7394]
 [-4.9616  7.9705  5.7394]]
```
> The lattice parameters of the supercell. They are equal (with a small tolerance `tol_1`)

```
a1_SC =  11.0039564326
a2_SC =  11.0039564326
a3_SC =  11.0039564326
```

> The determintant of the supercell expansion matrix:

```
det_indx_E =  4.0
```

> The supercell expansion matrix we are up to:
```
E_sol =  [[ 1.  1.  1.]
 [ 1.  1. -1.]
 [-1.  1.  1.]]
END ++++++++++
````
The supercell expansion matrix `E_sol` will be appropiate to satisty this condition:

```
a1_SC ~= a2_SC ~= a3_SC > tol_1
```


<a name="example4"></a>
## Test

Under the `TEST` folder, you will find the python program needed, 
together with an output file for aragonite.

If you run the program, you will obtain all the possible supercell expansion
matrices needed.

<a name="example5"></a>
## How to cite

Please cite the following reference when using this code:

Carrasco-Busturia, D., Erba, A., Mallia, G., Mellan, T. A. and Harrison, N. M. "Computed phase stability and phase transition mechanisms in CaCO3 at finite temperature and pressure" _In progress_

<a name="example6"></a>
## Contributing

`QHA` is free software released under the Gnu Public Licence version 3.
All contributions to improve this code are more than welcome.

* Have a look at GitHub's ["How to contribute"](https://guides.github.com/activities/contributing-to-open-source/#contributing).

* If you are familiar with `git`: fork this repository and submit a pull request.

* If you are not familiar with `git`:

    * If something should be improved, open an issue here on GitHub
    * If you think a new feature would be interesting, open an issue
    * If you need a particular feature for your project contact me directly.

