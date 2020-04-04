import os
import argparse

if __name__ == '__main__':
    pass
    ## parse command line
    parser = argparse.ArgumentParser(description='A script to find duplicate sequences in a fasta file')
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
    table = {}
    sequence = ''
    while line:
        if line.startswith('>'):
            flag = True
            if(len(sequence)>0):
                if sequence in table:
                    counter, title = table[sequence]
                    table[sequence] = (counter+1, title+"_and_"+line[0:].rstrip())
                else:
                    table[sequence] = (1, line[0:].rstrip()) 
            sequence = ''
        elif flag:
            sequence += line
        line = ffasta.readline().rstrip()
    if(len(sequence)>0):
        if sequence in table:
            counter, title = table[sequence]
            table[sequence] = (counter+1, title+"_and_"+line[0:].rstrip())
        else:
            table[sequence] = (1, line[0:].rstrip())
    summaryFile = fastaFile.replace('.fasta','.txt') 
    sfile = open(summaryFile,'w')
    for i in table:
        sfile.write(">" + table[i][1]+ "\n" + i + '\t' + str(table[i][0]) + '\n')
