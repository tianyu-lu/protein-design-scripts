#!/bin/bash
#SBATCH --time=5:06:15
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=4G
#SBATCH --account=def-pmkim

module purge
module load singularity/3.5
singularity pull docker://pablogainza/masif:latest
singularity run -B /scratch docker://pablogainza/masif
singularity exec -B /scratch masif_latest.sif python get_mimics_surf.py
python delete.py

