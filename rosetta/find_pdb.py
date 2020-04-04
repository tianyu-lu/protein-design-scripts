import argparse
import os

if __name__ == '__main__':
    pass
    ## parse command line
    parser = argparse.ArgumentParser(description='For each list of pdb filenames with the same sequence,\n replaces it with the filename of the pdb with the lowest column value')
    # required params
    parser.add_argument('-Sfasta', '--fasta_file', nargs=1, type=str, const=None,
                            help="Name of the file that stores fasta sequences",
                            dest='fasta_file')
    parser.add_argument('-Sfasc', '--fasc_file', nargs=1, type=str, const=None,
                            help="Name of the sorted score (.fasc) file",
                            dest='fasc_file')
    
    args = parser.parse_args()
    fastaFile = args.fasta_file[0]
    fascFile = args.fasc_file[0]
    try:
        ffasc = open(fascFile,'r')
    except IOError:
        print ("Could not read file: ", fname)
        sys.exit()
    line = ffasc.readline().rstrip()
    sorted_pdbs = []
    while line:
        if line.startswith('SCORE'):
            pdb_name = line[-4:].rstrip()
            sorted_pdbs.append(pdb_name)
        line = ffasc.readline().rstrip()
    output = ""
    # very naive solution
    try:
        ffasta = open(fastaFile,'r')
    except IOError:
        print ("Could not read file: ", fname)
        sys.exit()
    line = ffasta.readline().rstrip()
    while line:
        if line.startswith('>'):
            pdb_nums = line.split("_and_")	# a list of the four-digit code (suffix) output from Rosetta Design
            pdb_nums[0] = pdb_nums[0][1:]	# remove the > that preceeds the first element
            best_pos = 10000			# no more than 10000 structures are generated, safe upper bound
            best_pn = pdb_nums[0]
            if len(pdb_nums) > 1:
                for pn in pdb_nums:
                    if len(pn) > 1:
                        curr_pos = sorted_pdbs.index(pn) # index of four-digit code in the sorted .fasc score file
                        if curr_pos < best_pos:
                            best_pos = curr_pos		# smaller index imples lower energy
                            best_pn = pn
            output = output + ">" + best_pn + "\n"	# append the lowest energy code to output
        else:
            output = output + line + "\n"		# append the sequence to output
        line = ffasta.readline().rstrip()

    sfile = open("best_sequences.txt",'w')		# write to output
    sfile.write(output)
