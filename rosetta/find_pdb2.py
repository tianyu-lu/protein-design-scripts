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
            columns = line.split()
            pdb_name = columns[-1].rstrip()
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
            pdb_nums = line.split("_and_>")
            pdb_nums[0] = pdb_nums[0][2:]
            best_pos = 10000
            best_pn = pdb_nums[0]
            if len(pdb_nums) > 1:
                for pn in pdb_nums:
                    if len(pn) > 1:
                        curr_pos = sorted_pdbs.index(pn.split("_and_")[0])
                        if curr_pos < best_pos:
                            best_pos = curr_pos
                            best_pn = pn
            output = output + ">" + best_pn + "\n"
        else:
            output = output + line + "\n"
        line = ffasta.readline().rstrip()

    sfile = open("best_sequences.txt",'w')
    sfile.write(output)
