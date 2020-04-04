#!/bin/bash

for folder in 1*
do
	cd ${folder}/complex/runA.1
	cp ../../../equilibration.bash .
	mutation_name="${folder##*_}"
	#echo "export GMXLIB=/home/lutian5/.local/lib/python2.7/site-packages/pmx-2.0+27.g39c1c0a.dirty-py2.7-linux-x86_64.egg/pmx/data/mutff45" >> equilibration.bash
	#echo "mpiexec gmx_mpi mdrun -v -s -deffnm complex_${mutation_name}_emA" >> equilibration.bash
	#echo "mpiexec gmx_mpi grompp -f eqA.mdp -c complex_${mutation_name}_emA.gro -p ../topol.top -o complex_${mutation_name}_eqA.tpr -maxwarn 2" >> equilibration.bash
	#echo "mpiexec gmx_mpi mdrun -v -s -deffnm complex_${mutation_name}_eqA" >> equilibration.bash
	echo "mpiexec gmx_mpi mdrun -s -cpi complex_${mutation_name}_eqA.cpt -deffnm complex_${mutation_name}_eqA -append" >> equilibration.bash
	cd ../runB.1
	cp ../../../equilibration.bash .
	#echo "export GMXLIB=/home/lutian5/.local/lib/python2.7/site-packages/pmx-2.0+27.g39c1c0a.dirty-py2.7-linux-x86_64.egg/pmx/data/mutff45" >> equilibration.bash	
	#echo "mpiexec gmx_mpi mdrun -v -s -deffnm complex_${mutation_name}_emB" >> equilibration.bash
        #echo "mpiexec gmx_mpi grompp -f eqB.mdp -c complex_${mutation_name}_emB.gro -p ../topol.top -o complex_${mutation_name}_eqB.tpr -maxwarn 2" >> equilibration.bash
	#echo "mpiexec gmx_mpi mdrun -v -s -deffnm complex_${mutation_name}_eqB" >> equilibration.bash
	echo "mpiexec gmx_mpi mdrun -s -cpi complex_${mutation_name}_eqB.cpt -deffnm complex_${mutation_name}_eqB -append" >> equilibration.bash
	cd ../../receptor/runA.1
	cp ../../../equilibration.bash .
	#echo "export GMXLIB=/home/lutian5/.local/lib/python2.7/site-packages/pmx-2.0+27.g39c1c0a.dirty-py2.7-linux-x86_64.egg/pmx/data/mutff45" >> equilibration.bash
	#echo "mpiexec gmx_mpi mdrun -v -s -deffnm receptor_${mutation_name}_emA" >> equilibration.bash
        #echo "mpiexec gmx_mpi grompp -f eqA.mdp -c receptor_${mutation_name}_emA.gro -p ../topol.top -o receptor_${mutation_name}_eqA.tpr -maxwarn 2" >> equilibration.bash
        #echo "mpiexec gmx_mpi mdrun -v -s -deffnm receptor_${mutation_name}_eqA" >> equilibration.bash
        echo "mpiexec gmx_mpi mdrun -s -cpi receptor_${mutation_name}_eqA.cpt -deffnm receptor_${mutation_name}_eqA -append" >> equilibration.bash
	cd ../runB.1
        cp ../../../equilibration.bash .
	#echo "export GMXLIB=/home/lutian5/.local/lib/python2.7/site-packages/pmx-2.0+27.g39c1c0a.dirty-py2.7-linux-x86_64.egg/pmx/data/mutff45" >> equilibration.bash
	#echo "mpiexec gmx_mpi mdrun -v -s -deffnm receptor_${mutation_name}_emB" >> equilibration.bash
        #echo "mpiexec gmx_mpi grompp -f eqB.mdp -c receptor_${mutation_name}_emB.gro -p ../topol.top -o receptor_${mutation_name}_eqB.tpr -maxwarn 2" >> equilibration.bash
        #echo "mpiexec gmx_mpi mdrun -v -s -deffnm receptor_${mutation_name}_eqB" >> equilibration.bash
	echo "mpiexec gmx_mpi mdrun -s -cpi receptor_${mutation_name}_eqB.cpt -deffnm receptor_${mutation_name}_eqB -append" >> equilibration.bash
	cd ../../..
done
