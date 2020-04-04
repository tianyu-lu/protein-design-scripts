#!/bin/bash
#SBATCH --nodes=2
#SBATCH --gres=gpu:2
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --job-name=name
#SBATCH --account=account_name
#SBATCH --time=36:00:00
#SBATCH --mail-user=email@domain.com
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=ALL




module --force purge
module load nixpkgs/16.09  gcc/7.3.0  cuda/10.0.130  openmpi/3.1.2
module load gromacs/2019.3
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"


