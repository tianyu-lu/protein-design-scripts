# Outputs the names of the top 20% of structures
# Assumptions:
# Scores are in unbiased_scores.fasc
import argparse
import os

if __name__ == '__main__':
	pass

	try:
		ffasc = open('unbiased_scores.fasc','r')
	except IOError:
		print ("Could not read fasc file.")
		sys.exit()
	top_codes = []
	lines = ffasc.readlines()
	total_lines = len(lines)
	curr_line = 1
	for line in lines:
		if curr_line < total_lines/5:
			pdb_name = line.split()[-1].rstrip()
			top_codes.append(pdb_name)
		else:
			break
		curr_line += 1

	sfile = open("top_20_perc.txt",'w')
	sfile.write('\n'.join(top_codes))