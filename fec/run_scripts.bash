#!/bin/bash

for folder in 1*
do
	cd ${folder}/complex/runA.1
	mutation_name="${folder##*_}"
	sbatch equilibration.bash
	cd ../runB.1
	sbatch equilibration.bash
	cd ../../receptor/runA.1
	sbatch equilibration.bash
        cd ../runB.1
	sbatch equilibration.bash
	cd ../../..
done
