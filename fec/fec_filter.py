# remove unfavourable mutations

import os
import argparse

def contains_unfav(seq):
    if seq[131] == 'E':
        if seq[86] == 'K' or seq[83] == 'K':
            return True
    elif seq[124] == 'E':
        if seq[83] == 'L' or seq[39] == 'T' or seq[145] == 'A':
            return True

if __name__ == '__main__':
    pass
    ## parse command line
    parser = argparse.ArgumentParser(description='A script to remove unfavourable mutations')
    # required params
    parser.add_argument('-Sfasta', '--fasta_file', nargs=1, type=str, const=None,
                            help="Name of the file that stores fasta sequences",
                            dest='fasta_file')
    
    args = parser.parse_args()
    fastaFile = args.fasta_file[0]
    try:
        ffasta = open(fastaFile,'r')
    except IOError:
        print ("Could not read file: ", fname)
        sys.exit()
    line = ffasta.readline().rstrip()
    label = ""
    count = 0
    corr = 0
    total_seqs = 0
    while line:
        if line.startswith('>'):
            label = line
        elif len(line) > 80:
            total_seqs += 1
            if contains_unfav(line):
                if line[86] == 'E':    # Counts how many unfavourable sequences T87E is present in
                    with open("fec_filtered.fasta", "a") as g:
                        g.write(label + "\n" + line + "\n")
                    corr += 1
                    count -= 1
                count += 1
            else:
                with open("fec_filtered.fasta", "a") as g:
                    g.write(label + "\n" + line + "\n")
        line = ffasta.readline().rstrip()
    with open("fec_filtered.fasta", "a") as g:
        message = "Total seqs: " + str(total_seqs) + '\n'
        message += "Removed " + str(count) + " sequences.\n"
        message += "Unfav correlated with " + str(corr) + "sequences."
        g.write(message)
