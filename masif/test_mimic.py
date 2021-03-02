
### Same functionality as 01-pdb_extract_and_triangulate.py
import numpy as np
import glob
import pymesh   # order somehow matters
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
import os

# Apply mask to input_feat
def mask_input_feat(input_feat, mask):
    mymask = np.where(np.array(mask) == 0.0)[0]
    return np.delete(input_feat, mymask, axis=2)

def get_masif(fbase):
    try:
        fbase = fbase.split(".")[0]
        print(fbase)
        args = ["reduce", "-Trim", fbase+".pdb"]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()
        outfile = open(fbase+"_ignh.pdb", "w")
        outfile.write(stdout.decode('utf-8').rstrip())
        outfile.close()
        # Now add them again.
        args = ["reduce", "-HIS", fbase+"_ignh.pdb"]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()
        outfile = open(fbase+".pdb", "w")
        outfile.write(stdout.decode('utf-8'))
        outfile.close()

        os.system("sed -i \'/USER/d\' " + fbase+".pdb")

        output_pdb_as_xyzrn(fbase+".pdb", fbase+".xyzrn")

        FNULL = open(os.devnull, 'w')
        args = [os.environ['MSMS_BIN'], "-density", "3.0", "-hdensity", "3.0", "-probe",\
                        "1.5", "-if", fbase+".xyzrn","-of", fbase+"", "-af", fbase+""]

        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()

        vertices, faces, normals, names = read_msms(fbase+"")
        areas = {}
        ses_file = open(fbase+""+".area")
        next(ses_file) # ignore header line
        for line in ses_file:
            fields = line.split()
            areas[fields[3]] = fields[1]

        vertex_hbond = computeCharges(fbase+"", vertices, names)

        vertex_hphobicity = computeHydrophobicity(fbase, names)

        mesh = pymesh.form_mesh(vertices, faces)
        regular_mesh = fix_mesh(mesh, masif_opts['mesh_res'])

        vertex_normal = compute_normal(regular_mesh.vertices, regular_mesh.faces)

        vertex_hbond = assignChargesToNewMesh(regular_mesh.vertices, vertices,\
                vertex_hbond, masif_opts)

        vertex_hphobicity = assignChargesToNewMesh(regular_mesh.vertices, vertices,\
                vertex_hphobicity, masif_opts)

        old_resids = np.load(fbase+'.npy')
        print("Old resid length: ", len(old_resids))
        new_resid = assignChargesToNewMesh(regular_mesh.vertices, vertices,\
                old_resids, None)
        print("Length of new resids: ", len(new_resid))
        np.save(fbase+'.npy', new_resid)

        pdb2pqr_path = "/home/lutian5/scratch/work/pdb2pqr/pdb2pqr-linux-bin64-2.1.1/pdb2pqr"
        args = [pdb2pqr_path,"--ff=amber","--whitespace","--noopt","--apbs-input",fbase+".pdb",fbase+""]   # changed ff to amber from parse for nucleic acids handling
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()

        args = [os.environ['APBS_BIN'], fbase+"" + ".in"]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()

        vertfile = open(fbase+".csv", "w")
        for vert in regular_mesh.vertices:
            vertfile.write("{},{},{}\n".format(vert[0], vert[1], vert[2]))

        vertfile.close()

        args = [os.environ['MULTIVALUE_BIN'], fbase+"" + ".csv", fbase+"" + ".dx", fbase+"" + "_out.csv"]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()

        # Read the charge file
        chargefile = open(fbase+"" + "_out.csv")
        charges = np.array([0.0] * len(regular_mesh.vertices))
        for ix, line in enumerate(chargefile.readlines()):
            charges[ix] = float(line.split(",")[3])

        save_ply(fbase+".ply", regular_mesh.vertices,\
                  regular_mesh.faces, normals=vertex_normal, charges=charges,\
                  normalize_charges=True, hbond=vertex_hbond, hphob=vertex_hphobicity)
        return 0
    except:
        return 1


for f in glob.glob("*.pdb"):
    print(f)
    get_masif(f)

