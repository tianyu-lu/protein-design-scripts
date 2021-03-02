import MDAnalysis
from Bio.PDB import *
import os
import numpy as np
import math
import sys
import io
import matplotlib.pyplot as plt
import glob

import warnings
warnings.simplefilter("ignore")

aa_to_int = {"I":1, "V":2, "L":3, "F":4, "C":5, "M":6, "A":7, "G":8, "T":9, "S":10, 
			 "W":11, "Y":12, "P":13, "H":14, "E":15, "Q":16, "D":17, "N":18, "K":19, "R":20,
			 "START":21, "END":22}
three_to_one = {"ILE":"I", "VAL":"V", "LEU":"L", "PHE":"F", "CYS":"C", 
				"MET":"M", "ALA":"A", "GLY":"G", "THR":"T", "SER":"S", 
				"TRP":"W", "TYR":"Y", "PRO":"P", "HIS":"H", "GLU":"E", 
				"GLN":"Q", "ASP":"D", "ASN":"N", "LYS":"K", "ARG":"R"}

def new_dihedral(p):
	"""Praxeolitic formula
	1 sqrt, 1 cross product"""
	p0 = p[0]
	p1 = p[1]
	p2 = p[2]
	p3 = p[3]

	b0 = -1.0*(p1 - p0)
	b1 = p2 - p1
	b2 = p3 - p2

	# normalize b1 so that it does not influence magnitude of vector
	# rejections that come next
	b1 /= np.linalg.norm(b1)

	# vector rejections
	# v = projection of b0 onto plane perpendicular to b1
	#   = b0 minus component that aligns with b1
	# w = projection of b2 onto plane perpendicular to b1
	#   = b2 minus component that aligns with b1
	v = b0 - np.dot(b0, b1)*b1
	w = b2 - np.dot(b2, b1)*b1

	# angle between v and w in a plane is the torsion angle
	# v and w may not be normalized but that's fine since tan is y/x
	x = np.dot(v, w)
	y = np.dot(np.cross(b1, v), w)
	return np.arctan2(y, x)

def save_cartesian():
	for f in glob.glob("*.pdb"):
		print(f)

		u = MDAnalysis.Universe(f)
		atoms = u.select_atoms('protein and backbone and not name O and not altloc B and not altloc C')
		# for a in atoms[45*3:48*3]:
		# 	print(a.type)
		# assert atoms[0].type == 'N'
		atoms = np.array(atoms.positions)
		np.save(f[:-4] + "_cartesian.npy", atoms)

# added omega angles
def save_phi_psi(normalized=False):
	for f in glob.glob("*_cartesian.npy"):
		dihedrals = []
		print(f)
		protein = np.load(f)
		for i in range(2, len(protein)-7, 3):
			phi = new_dihedral(protein[i:i+4])
			psi = new_dihedral(protein[i+1:i+5])
			omg = new_dihedral(protein[i+2:i+6])
			dihedrals.append([phi, psi, omg])
		dihedrals = np.array(dihedrals)
		if normalized:
			dihedrals = (dihedrals + math.pi) / (2 * math.pi)
		dihedrals = np.concatenate((np.zeros((len(dihedrals), 1)), dihedrals), axis=1)
		dihedrals = np.concatenate((np.array([[21., 0., 0., 21.]]), dihedrals, np.array([[22., 22., 0., 0.]])), axis=0)
		np.save(f[:-14] + "_phi_psi_normed.npy", dihedrals)

save_cartesian()
save_phi_psi(normalized=True)
