import os

for f in os.listdir("."):
    if f.endswith(".pdb") or f.endswith(".out"):
        continue
    os.system("rm {}".format(f))
os.system("rm -rf data")
os.system("rm -rf source")
os.system("rm *_ignh.pdb")

