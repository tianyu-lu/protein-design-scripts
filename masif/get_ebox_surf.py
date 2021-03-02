# sequence of commands to get surface of ebox DNA motif
from subprocess import Popen, PIPE
import os

### Same functionality as 01-pdb_extract_and_triangulate.py

args = ["reduce", "-Trim", "ebox.pdb"]
p2 = Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = p2.communicate()
outfile = open("ebox_ignh.pdb", "w")
outfile.write(stdout.decode('utf-8').rstrip())
outfile.close()
# Now add them again.
args = ["reduce", "-HIS", "ebox_ignh.pdb"]
p2 = Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = p2.communicate()
outfile = open("ebox.pdb", "w")
outfile.write(stdout.decode('utf-8'))
outfile.close()

import pymesh	# order somehow matters
from subprocess import Popen, PIPE
import os
from Bio.PDB import *
from xyzrn import output_pdb_as_xyzrn
from read_msms import read_msms
from computeCharges import computeCharges, assignChargesToNewMesh
from computeHydrophobicity import *
from fixmesh import fix_mesh
from masif_opts import masif_opts
from compute_normal import compute_normal
from save_ply import save_ply
from read_data_from_surface import read_data_from_surface

output_pdb_as_xyzrn("ebox.pdb", "ebox.xyzrn", dna=True)

FNULL = open(os.devnull, 'w')
args = [os.environ['MSMS_BIN'], "-density", "3.0", "-hdensity", "3.0", "-probe",\
                "1.5", "-if", "ebox.xyzrn","-of", "ebox", "-af", "ebox"]

p2 = Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = p2.communicate()

vertices, faces, normals, names = read_msms("ebox")
areas = {}
ses_file = open("ebox"+".area")
next(ses_file) # ignore header line
for line in ses_file:
    fields = line.split()
    areas[fields[3]] = fields[1]

vertex_hbond = computeCharges("ebox", vertices, names)

vertex_hphobicity = computeHydrophobicity("ebox", names)

mesh = pymesh.form_mesh(vertices, faces)
regular_mesh = fix_mesh(mesh, masif_opts['mesh_res'])

vertex_normal = compute_normal(regular_mesh.vertices, regular_mesh.faces)

vertex_hbond = assignChargesToNewMesh(regular_mesh.vertices, vertices,\
        vertex_hbond, masif_opts)

vertex_hphobicity = assignChargesToNewMesh(regular_mesh.vertices, vertices,\
        vertex_hphobicity, masif_opts)

import numpy as np

args = [os.environ['PDB2PQR_BIN'],"--ff=amber","--whitespace","--noopt","--apbs-input","ebox.pdb","ebox"]   # changed ff to amber from parse for nucleic acids handling
p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd="/masif/")
stdout, stderr = p2.communicate()

args = [os.environ['APBS_BIN'], "ebox" + ".in"]
p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd="/masif/")
stdout, stderr = p2.communicate()

vertfile = open("ebox.csv", "w")
for vert in regular_mesh.vertices:
    vertfile.write("{},{},{}\n".format(vert[0], vert[1], vert[2]))

vertfile.close()

args = [os.environ['MULTIVALUE_BIN'], "ebox" + ".csv", "ebox" + ".dx", "ebox" + "_out.csv"]
p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd="/masif/")
stdout, stderr = p2.communicate()

# Read the charge file
chargefile = open("ebox" + "_out.csv")
charges = np.array([0.0] * len(regular_mesh.vertices))
for ix, line in enumerate(chargefile.readlines()):
    charges[ix] = float(line.split(",")[3])

save_ply("ebox.ply", regular_mesh.vertices,\
          regular_mesh.faces, normals=vertex_normal, charges=charges,\
          normalize_charges=True, hbond=vertex_hbond, hphob=vertex_hphobicity)


### 04-masif_precompute.py
params = masif_opts["ppi_search"]
input_feat, rho, theta, mask, neigh_indices, iface_labels, verts = read_data_from_surface("ebox.ply", params)

np.save('ebox_rho_wrt_center', rho)
np.save('ebox_theta_wrt_center', theta)
np.save('ebox_input_feat', input_feat)
np.save('ebox_mask', mask)
np.save('ebox_list_indices', neigh_indices)
np.save('ebox_iface_labels', iface_labels)
# Save x, y, z
np.save('ebox_X.npy', verts[:,0])
np.save('ebox_Y.npy', verts[:,1])
np.save('ebox_Z.npy', verts[:,2])


### masif_ppi_search_comp_desc.py

print("Reading pre-trained network")
from MaSIF_ppi_search import MaSIF_ppi_search

learning_obj = MaSIF_ppi_search(
    params["max_distance"],
    n_thetas=16,
    n_rhos=5,
    n_rotations=16,
    idx_gpu="/gpu:0",
    feat_mask=params["feat_mask"],
)
learning_obj.saver.restore(learning_obj.session, params["model_dir"] + "model")

from train_ppi_search import compute_val_test_desc

# Apply mask to input_feat
def mask_input_feat(input_feat, mask):
    mymask = np.where(np.array(mask) == 0.0)[0]
    return np.delete(input_feat, mymask, axis=2)

p1_rho_wrt_center = np.load("ebox_rho_wrt_center.npy")
p1_theta_wrt_center = np.load("ebox_theta_wrt_center.npy")
p1_input_feat = np.load("ebox_input_feat.npy")
p1_input_feat = mask_input_feat(p1_input_feat, params["feat_mask"])
p1_mask = np.load("ebox_mask.npy")
idx1 = np.array(range(len(p1_rho_wrt_center)))
desc1_str = compute_val_test_desc(
    learning_obj,
    idx1,
    p1_rho_wrt_center,
    p1_theta_wrt_center,
    p1_input_feat,
    p1_mask,
    batch_size=1,
    flip=False,
)

np.save("ebox_desc.npy", desc1_str)
