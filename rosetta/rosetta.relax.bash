#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=4
#SBATCH --mem=0
#SBATCH --job-name=relax-remaining-clusters
#SBATCH --account=account-name
#SBATCH --time=1-00:00
#SBATCH --mail-user=email@domain.com
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=ALL




module purge
module load nixpkgs/16.09  gcc/5.4.0  openmpi/2.1.1
module load rosetta/3.9
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"


for file in `find . -regextype posix-extended -regex "^./frame1?[0-9].pdb$"`
do
        echo $file
	mpiexec relax.mpi.linuxgccrelease @relax.options -s $file -scorefile ${file}.fasc > ${file}_relax.out
done
echo "relax complete"


