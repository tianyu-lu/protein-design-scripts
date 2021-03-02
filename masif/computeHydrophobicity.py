import numpy as np
import pickle

# Kyte Doolittle scale
kd_scale = {}
kd_scale["ILE"] = 4.5
kd_scale["VAL"] = 4.2
kd_scale["LEU"] = 3.8
kd_scale["PHE"] = 2.8
kd_scale["CYS"] = 2.5
kd_scale["MET"] = 1.9
kd_scale["ALA"] = 1.8
kd_scale["GLY"] = -0.4
kd_scale["THR"] = -0.7
kd_scale["SER"] = -0.8
kd_scale["TRP"] = -0.9
kd_scale["TYR"] = -1.3
kd_scale["PRO"] = -1.6
kd_scale["HIS"] = -3.2
kd_scale["GLU"] = -3.5
kd_scale["GLN"] = -3.5
kd_scale["ASP"] = -3.5
kd_scale["ASN"] = -3.5
kd_scale["LYS"] = -3.9
kd_scale["ARG"] = -4.5
kd_scale["DA"] = -4.5
kd_scale["DC"] = -4.5
kd_scale["DG"] = -4.5
kd_scale["DT"] = -4.5

# For each vertex in names, compute hydrophobicity and saves a vertex id to resid and resname mapping
def computeHydrophobicity(pdbid, names):
    hp = np.zeros(len(names))
    id_to_res_map = []
    for ix, name in enumerate(names):
        aa = name.split("_")[3]
        aa_idx = name.split("_")[1]
        hp[ix] = kd_scale[aa]
        id_to_res_map.append(aa + "_" + aa_idx)
    np.save(pdbid+".npy", np.array(id_to_res_map))
    return hp

# l = ['ASN_255', 'GLU_45']
# a = np.array(l)
# print(a)