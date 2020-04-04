import sys,os

d = sys.argv[1]
try:
    ncpu = int(sys.argv[2])
except:
    ncpu = 16
try:
    wt = sys.argv[3]
except:
    wt = "2:00:00"
root = os.path.abspath('.')
mut_dir = os.path.join(root,d)
name = '_'.join(mut_dir.split('/')[3:])
if name[-1] == '_': name = name[:-1]
os.chdir(mut_dir)
ad = mut_dir #os.path.abspath(A_dir)
fp = open('jobscript','w+')
fp.write('#!/bin/bash \n')
fp.write('#SBATCH --nodes=1 \n')
fp.write('#SBATCH --ntasks-per-node=8 \n')
fp.write('#SBATCH --cpus-per-task=4 \n')
fp.write('#SBATCH --mem=8000 \n')
fp.write('#SBATCH --job-name=fe_calc \n')
fp.write('#SBATCH --account=account-name \n')
fp.write('#SBATCH --time=0:30:00 \n')


fp.write('export GMXLIB=/home/lutian5/.local/lib/python2.7/site-packages/pmx/data/mutff45 \n')


fp.write('module purge \n')
fp.write ('module load nixpkgs/16.09  gcc/7.3.0  openmpi/3.1.2 \n')
fp.write ('module load gromacs/2019.3 \n')
fp.write ('export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}" \n')



fp.write('mpiexec gmx_mpi mdrun -s topol.tpr \n')
fp.close()

os.chdir(root)
