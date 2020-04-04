#!/bin/csh

foreach S( runA.1/morphes/frame* runB.1/morphes/frame*)
python $PWD/make_morphe_jobs-3.py $S 
end

