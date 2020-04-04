#!/bin/bash

cd runA.1
rm traj.xtc
trajectory=./*.xtc
ln -s $trajectory traj.xtc
rm topol.tpr
topology=./*eq*.tpr
ln -s $topology topol.tpr
echo $trajectory
echo $topology
cd ../runB.1
rm traj.xtc
trajectory=./*.xtc
ln -s $trajectory traj.xtc
rm topol.tpr
topology=./*eq*.tpr
ln -s $topology topol.tpr
echo $trajectory
echo $topology
cd ..

cp ../../tiA.mdp .
cp ../../make_jobs-cedar.sh .
cp ../../make_morphe_jobs-3.py .
cp ../../submit-2.sh .

cd runA.1
rm -rf morphes/*
rmdir morphes
cd ../runB.1
rm -rf morphes/*
rmdir morphes
cd ..

export GMXLIB=/home/lutian5/.local/lib/python2.7/site-packages/pmx/data/mutff45
module load nixpkgs/16.09  gcc/7.3.0  openmpi/3.1.2
module load gromacs/2019.3
python2.7 /home/lutian5/scratch/work/free_energy/pmx/pmx/scripts/prepare_crooks_runs_mod.py -d $PWD -mdp tiA.mdp -sw_time 100


csh make_jobs-cedar.sh
bash submit-2.sh

