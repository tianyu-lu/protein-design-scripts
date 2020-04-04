#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=4
#SBATCH --mem=0
#SBATCH --job-name=distribute_scripts
#SBATCH --account=account_name
#SBATCH --time=1-00:00

for folder in 1*
do
	cd ${folder}/complex
	cp ../../fe_calc_script.bash .
	bash fe_calc_script.bash
	cd ../..
	cd ${folder}/receptor
	cp ../../fe_calc_script.bash .
	bash fe_calc_script.bash
	cd ../..
done
