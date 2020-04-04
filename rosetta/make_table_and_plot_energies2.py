# Plots the energies of the unbiased structures and outputs its table representation
# Assumptions:
# Scores are in sorted_scores.fasc
# Unique codes are in unique_structures_codes.txt
import argparse
import os
import seaborn as sns, numpy as np
import pandas as pd

if __name__ == '__main__':
	pass

	try:
		fcodes = open('unique_structures_codes.txt','r')
	except IOError:
		print ("Could not read unique_structures_codes file.")
		sys.exit()
	line = fcodes.readline().rstrip()
	unbiased_codes = []
	while line:
		unbiased_codes.append(line)
		line = fcodes.readline().rstrip()

	try:
		ffasc = open('sorted_scores.fasc','r')
	except IOError:
		print ("Could not read fasc file.")
		sys.exit()
	line = ffasc.readline().rstrip()
	output_table = []
	while line:
		if line.startswith('SCORE'):
			pdb_name = line.split()[-1].rstrip()
			if pdb_name in unbiased_codes:
				output_table.append(line)
		line = ffasc.readline().rstrip()

	data = []
	for line in output_table:
		energy = line.split()[6]	#sixth column of score file
		data.append(float(energy))

	sfile = open("unbiased_scores.fasc",'w')
	sfile.write('\n'.join(output_table))

	sns.set()
	data = pd.Series(data, name="Rosetta Energy")
	hist = sns.distplot(data)
	fig = hist.get_figure()
	fig.savefig("designed_energies.png")
