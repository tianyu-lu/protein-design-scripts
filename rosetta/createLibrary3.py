import os
import argparse
import random
from random import choices
import time

AA = ['A', 'C', 'E', 'D', 'G', 'F', 'I', 'H', 'K', 'M', 'L', 'N', 'Q', 'P', 'S', 'R', 'T', 'W', 'V', 'Y']
FREQ = [32,  4, 52, 96, 28, 40, 20, 56, 12, 64, 12, 24, 16, 20, 12, 44, 28, 32, 8, 50]

def readingFasta(fastaFile):
    table = []
    try:
        ffasta = open(fastaFile,'r')
    except IOError:
        print ("Could not read file: ", fname)
        sys.exit()
    line = ffasta.readline().rstrip()
    sequence = ''
    while line:
        if line.startswith('>'):
            flag = True
            if(len(sequence)>0):
                if sequence not in table:
                    table.append(sequence)
            sequence = ''
        elif flag:
            sequence += line
        line = ffasta.readline().rstrip()
    if(len(sequence)>0):
        if sequence not in table:
            table.append(sequence)
    return table

if __name__ == '__main__':
    pass
    ## parse command line
    parser = argparse.ArgumentParser(description='A script to increase diversity of a set of sequences')
    # required params
    parser.add_argument('-Sfasta', '--fasta_file', nargs=1, type=str, const=None,
                            help="Name of the file that stores fasta sequences",
                            dest='fasta_file')
    parser.add_argument('-SListMutations', '--list_mutations', nargs=1, type=str, const=None,
                            help="Please insert the list of your mutations (e.x., 3,4,5,6,7,9,10,11,12,15,16,17,18,21,22,23,24)?",
                            dest='list_mutations')
    parser.add_argument('-NumSeqs', '--num_sequences', nargs=1, type=int, const=None,
                            help="Number of sequences to be generated",
                            dest='num_sequences')

    import time
    start_time = time.time()
    args = parser.parse_args()
    fastaFile = args.fasta_file[0]
    numSeqs = int(args.num_sequences[0])
    listPositions = args.list_mutations[0].split(',')
    temporalList = []
    finalList = []
    auxList = []
    fastaList = readingFasta(fastaFile)
    processingList = list(fastaList)
    finalList.extend(fastaList)
    remainingList = []

    targetLen = len(processingList[0])
    while len(finalList) < numSeqs:
        total = len(AA) * len(listPositions) * len(processingList)
        totalList = list(range(total))
        flag = False
        temporalList = []
        valid_list = list(totalList)
        while (len(valid_list)>0 and (len(finalList) + len(temporalList) < numSeqs)):
            randomIndex = random.randrange(len(valid_list))
            newSeq = int(valid_list[randomIndex]/(len(AA) * len(listPositions)))
            newSeqPos = int((valid_list[randomIndex] % (len(AA) * len(listPositions))) / len(AA))

            # sample from distribution over amino acids (DMP biased)
            # newAAPos = valid_list[randomIndex]%len(AA)
            newAA = choices(population=AA , weights=FREQ , k=1)[0]

            #listPositions contains the indexes + 1, that is the reason for the -1
            newSequence = processingList[newSeq][0:int(listPositions[newSeqPos])-1] + newAA + processingList[newSeq][int(listPositions[newSeqPos]):]
            valid_list.pop(randomIndex)
            if (newSequence not in finalList and newSequence not in temporalList):
                temporalList.append(newSequence)
        finalList.extend(temporalList)
        processingList = list(temporalList)
    #print(len(finalList))
    fw = open("point_mutations.fasta",'w')
    for i in range(len(finalList)):
        fw.write('>'+str(i)+'\n'+finalList[i]+'\n')
    fw.close()
    print("--- %s seconds ---" % (time.time() - start_time))
