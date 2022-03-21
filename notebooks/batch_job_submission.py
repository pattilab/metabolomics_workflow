import os
import sys

dir = sys.argv[1]
polarity = sys.argv[2]

files = [x for x in os.listdir(dir) if ".mzML" in x]

for file in files[:1]:
    bsub = open("/storage1/fs1/gjpattij/Active/Ethan/polar_metabolite_identification/run_scripts/base_bsub","r").readlines()
    bsub += ["python3 run_DecoID_single_file" + polarity + ".py " + dir + file]
    tmp = open("tmp.bsub","w")
    [tmp.write(x) for x in bsub]
    tmp.close()
    os.system("active_dir bsub < tmp.bsub")