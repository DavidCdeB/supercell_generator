#
Scriptdir=`pwd`

rm -Rf ./results/supercells_integers_0_1_-1_2_-2/tol_1_equal_to_10
mkdir -p  ./results/supercells_integers_0_1_-1_2_-2/tol_1_equal_to_10

cd ./results/supercells_integers_0_1_-1_2_-2/tol_1_equal_to_10

Workdir=`pwd`

cd $Scriptdir

cp supercell_generator_v2.py $Workdir


FILES="
8
7
6
5
4
3
2
1
0
"


for i in ${FILES}; do

cd $Workdir

rm -Rf ${i}
mkdir ${i}

done

#####
for i in ${FILES}; do

cd $Workdir

cp supercell_generator_v2.py ./${i}
cd ${i} 

sed -i s/tol_2=1E-5/tol_2=1E-${i}/ supercell_generator_v2.py

python supercell_generator_v2.py >  calcite_14__1E-${i}.out

cd $Workdir

done
