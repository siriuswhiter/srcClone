import sys, os

from parse import Parser
from slice import Vector

# input: filename
# output: SliceProfile list
def src2slices(file):
    re = []
    cmd = "srcml --position {0} -o {0}.xml".format(file)
    with os.popen(cmd) as c1:
        cmd2 = "srcslice {0}.xml".format(file)
        with os.popen(cmd2) as c2:
            parser = Parser()
            re = parser.parse_all(c2.read().split("\n"))
    
    return re


def slice_based_cognitive_complexity_metrics():
    pass

# algorithm 1
# input: slice profile list
# output: variable/ function/ file level's slicing vector: [Vector()]
def slices2vectors(slices):
    vecset = []

    for slice in slices:
        # 1. calculate complete slice

        # 2. calculate the slice-based cognitive complexity metrics
        slice_based_cognitive_complexity_metrics()
        
        # 3. encoding the slicing vector
        # vecset.append(Vector())

    return vecset



def main(file1, file2):
    slice_profiles_1 = src2slices(file1)
    slicing_vectors_1 = slices2vectors(slice_profiles_1)

    slice_profiles_2 = src2slices(file2)
    slicing_vectors_2 = slices2vectors(slice_profiles_2)

    # similarity and matching



if __name__ == "__main__":
    if len(sys.argv)<3:
        exit("Usage: python3 srcClone.py file1 file2")
    main(sys.argv[1], sys.argv[2])