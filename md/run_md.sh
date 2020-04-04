#!/bin/bash
#SBATCH --account=account-name
#SBATCH --nodes=2                # number of nodes
#SBATCH --gres=gpu:2
#SBATCH --ntasks-per-node=8      # request 8 MPI tasks per node
#SBATCH --cpus-per-task=4        # 4 OpenMP threads per MPI task => total: 8 x 4 = 32 CPUs/node
#SBATCH --mem=0                  # request all available memory on the node
#SBATCH --time=2-00:00           # time limit (D-HH:MM)
#SBATCH --job-name=2_1_L125E
#SBATCH --mail-user=email@domain.com
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=ALL

module purge
module load gcc/7.3.0  openmpi/3.1.2  gromacs/2019.3
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"


gmx grompp -f nvt.mdp -c em.gro -r em.gro -p 2_1_L125E.pdb.top -n -o nvt.tpr
srun gmx_mpi mdrun -v -s -deffnm nvt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -p 2_1_L125E.pdb.top -n -o npt.tpr
srun gmx_mpi mdrun -v -s -deffnm npt
gmx grompp -f production.mdp -c npt.gro -p 2_1_L125E.pdb.top -o md_0_1.tpr
srun gmx_mpi mdrun -v -s -deffnm md_0_1
