#!/bin/bash
for x in runA.1/morphes/frame* runB.1/morphes/frame*; do cd $x; sbatch jobscript; cd ../../../; done
