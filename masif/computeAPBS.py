import os
import numpy
from subprocess import Popen, PIPE
import pymesh

# from default_config.global_vars import apbs_bin, pdb2pqr_bin, multivalue_bin
import random

"""
computeAPBS.py: Wrapper function to compute the Poisson Boltzmann electrostatics for a surface using APBS.
Pablo Gainza - LPDI STI EPFL 2019
This file is part of MaSIF.
Released under an Apache License 2.0
"""

def computeAPBS(vertices, pdb_file, tmp_file_base):
    """
        Calls APBS, pdb2pqr, and multivalue and returns the charges per vertex
    """
    fields = tmp_file_base.split("/")[0:-1]
    directory = "/".join(fields) + "/"
    filename_base = tmp_file_base.split("/")[-1]
    pdbname = pdb_file.split("/")[-1]
args = [os.environ['PDB2PQR_BIN'],"--ff=amber","--whitespace","--noopt","--apbs-input","ebox.pdb","ebox"]   # changed ff to amber from parse for nucleic acids handling
p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd="/masif/")
stdout, stderr = p2.communicate()

args = [os.environ['APBS_BIN'], "ebox" + ".in"]
p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd="/masif/")
stdout, stderr = p2.communicate()

vertfile = open("ebox.csv", "w")
for vert in vertices:
    vertfile.write("{},{},{}\n".format(vert[0], vert[1], vert[2]))
vertfile.close()

args = [os.environ['MULTIVALUE_BIN'], "ebox" + ".csv", "ebox" + ".dx", "ebox" + ".csv"]
p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd="/masif/")
stdout, stderr = p2.communicate()

# Read the charge file
chargefile = open("ebox" + ".csv")
charges = numpy.array([0.0] * len(vertices))
for ix, line in enumerate(chargefile.readlines()):
    charges[ix] = float(line.split(",")[3])

    return charges
