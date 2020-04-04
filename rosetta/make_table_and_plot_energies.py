# Plots the energies of the unbiased structures and outputs its table representation
# Assumptions:
# Scores are in sorted_scores.fasc
# Unique codes are in unique_structures_codes.txt
import argparse
import os
import matplotlib.pyplot as plt

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
			pdb_name = line[-4:].rstrip()
			if pdb_name in unbiased_codes:
				output_table.append(line)
		line = ffasc.readline().rstrip()

	data = []
	for line in output_table:
		energy = line.split()[6]	#sixth column of score file
		data.append(energy)

	sfile = open("unbiased_scores.fasc",'w')
	sfile.write('\n'.join(output_table))

	fig, ax = plt.subplots(1, 1)
	energy_hist = ax.hist(data, bins=100)
	for tick in ax.get_xticklabels():
		tick.set_rotation(45)
	plt.xlabel("dG_separated/dSASAx100")
	plt.ylabel("Frequency")
	plt.title("Energy of Unbiased Structures")
	plt.savefig("energies_plot.PNG", dpi=200)
