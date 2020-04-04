for folder in ./2*
do
	cd $folder
	file=./*.sh
	sbatch $file
	cd ..
done
