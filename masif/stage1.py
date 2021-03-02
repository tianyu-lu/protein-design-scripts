import numpy as np
import glob
# do stage 1 of masif-ppi-search
print("Stage 1 of MaSIF-ppi-search")

ebox_desc = np.load("ebox_desc.npy")           # can subset this to make more efficient, search only at critical binding interfaces
ebox_desc = [ebox_desc[274], ebox_desc[2333]]
ebox_idx = np.load("ebox_list_indices.npy")
matches = []
database = glob.glob("*_desc_straight.npy")   # shape: (num_vertices, 80)
database_np = np.array(database)
K = 5
for i, patch in enumerate(ebox_desc):
    all_dists = []
    for desc in database: 
        desc_name = desc[:-18]
        desc_idx = np.load(desc_name + "_list_indices.npy")
        q = np.load(desc)
        dists = np.linalg.norm(q - patch, axis=1)
        min_idxs = np.argsort(dists)                          # could consider relaxing to best 3 or best K matches
        min_dists = dists[min_idxs[:K]]
        for md in min_dists:
            all_dists.append(md)
    best_match_idxs = np.floor_divide(np.argsort(np.array(all_dists)), K)         # same here
    filenames = database_np[best_match_idxs]
    for f in np.unique(filenames):
        q = np.load(f)
        dists = np.linalg.norm(q - patch, axis=1)
        min_idxs = np.argsort(dists)[:K]
        desc_name = f[:-18]
        desc_idx = np.load(desc_name + "_list_indices.npy")
        for mi in min_idxs:
            matches.append((f, desc_idx[mi]))

# map patch indices to resnames and resids
import pickle
for m in matches:
    to_aa = np.load(m[0][:-18] + ".npy")
    aas = to_aa[m[1]]
    # aas = [a[0] for a in aas]
    aas = set(aas)
    print("Matching {}".format(m[0][:-18]))
    for aa in aas:
        print(aa.split('_')[1], end=' ')
    print('')