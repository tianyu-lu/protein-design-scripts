#!/bin/bash


for file in `find ./initial_structures/ -regextype posix-extended -regex "^./.*pdb$"`
do
        file_base="$(basename -- "$file")"
	# echo ${file_base}
	file_wo_extension="${file_base%.*}"
	echo ${file_wo_extension}
	#echo ${file}
	#cp ${file} ${file_wo_extension}
	#mkdir ${file_wo_extension}
	#curr_frame_resfile="$(find ./resfiles -regextype posix-extended -regex "^./resfiles/${file_base}.*")"
	#echo $curr_frame_resfile
	#cp ${curr_frame_resfile} ./${file_wo_extension}/cluster1.resfile
	#cp ${file} ${file_wo_extension}

	#cp rosetta.design_3.9.bash ${file_wo_extension}
	#cp design_backrub_ref2015.xml ${file_wo_extension}
	#cp design.options ${file_wo_extension}
	#design_command="mpiexec rosetta_scripts.mpi.linuxgccrelease @design.options -parser:protocol design_backrub_ref2015.xml -out:suffix _design_backrub_rep1 -s ${file_base} -scorefile ${file_wo_extension}_design_rep1.fasc > ${file_wo_extension}_design.out"
	#echo ${design_command} >> ${file_wo_extension}/rosetta.design_3.9.bash

	#sbatch ./${file_wo_extension}/rosetta.design_3.9.bash

	#tar cvfz design_${file_wo_extension}.tar.gz ./*

	cd ${file_wo_extension}
	#rm ./analysis/*
	#rmdir analysis
        #cp ../analysis.resfile .
        #cp ../*.py .
        #cp ../picking_best_models.sh .
	cp ../${file_wo_extension}.fasc .

	#python2.7 design_analysis.py -n ${file_wo_extension}.pdb --title ${file_wo_extension} --res analysis.resfile --prefix *design_backrub_rep1*.pdb
	rm ./sorted_scores.fasc
	rm sequences.fasta
	rm filtered.fasta
	score_file=./*.fasc
	#echo "score file"
	#echo $score_file
	#sort -n -k6 ${score_file} | head -n 100 | awk '{print $NF}' > best_100.txt
	fasta_file=./*.fasta
	#echo "one fasta file"
	echo $fasta_file
	sort -n -k7 ${score_file} > sorted_scores.fasc
	cp $fasta_file sequences.fasta
	python findDuplicatesFasta.py -Sfasta sequences.fasta
	cp sequences.txt filtered.fasta
	python find_pdb.py -Sfasta filtered.fasta -Sfasc sorted_scores.fasc

	# Copy unbiased structures into folder for sequence/energy/logo analysis
	#mkdir unbiased_structures
	cd unbiased_structures
	rm *.pdb
	cp ../best_sequences.txt .
	cut -c2-5 best_sequences.txt | sed -n 'p;n' > unique_structures_codes.txt
	while read -r code; do cp ../${file_wo_extension}_design_backrub_rep1_${code}.pdb .; done < unique_structures_codes.txt
	cp ../*.py .
	cp ../${file_wo_extension}.fasc .
	cp ../analysis.resfile .
	cp ../../union.resfile .
	cp ../${file_wo_extension}.pdb .
	python2.7 design_analysis.py -n ${file_wo_extension}.pdb --title ${file_wo_extension} --res union.resfile --prefix *design_backrub_rep1*.pdb
	#cp *.png ../../short_logos
	cp *design_backrub_rep1*.pdb ../../new_pool
	cp ../../make_table_and_plot_energies.py .
	cp ../sorted_scores.fasc .
	python make_table_and_plot_energies.py
	cp unbiased_scores.fasc ../../unbiased_scores/${file_wo_extension}.fasc

	#mkdir best_structures
	#cd best_structures
	#cp ../sorted_scores.fasc .
	#cp ../analysis.resfile .
	#cp ../${file_wo_extension}.pdb .
	#cp ../*.py .
	#num_files=$(ls -1 | wc -l)
	#num_unique_structures=$((num_files-17))  # there should be 17 non-design pdb files in this folder
	#num_to_extract=$(( num_unique_structures/2 < 300 ? num_unique_structures/2 : 300 ))  # cap number of designs at 300
	#head -n ${num_to_extract} sorted_scores.fasc | awk '{print $NF}' > candidate_designs.txt
	#while read -r file; do cp ../${file}.pdb .; done < candidate_designs.txt
	#python2.7 design_analysis.py -n ${file_wo_extension}.pdb --title ${file_wo_extension} --res analysis.resfile --prefix *design_backrub_rep1*.pdb
	cd ../..
done
echo "design complete"


