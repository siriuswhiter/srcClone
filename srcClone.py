import sys, os

from parse import Parser
from slice import Vector
from crANN import CRANN

# input: filename
# output: AllSP
def src2sps(file):
    re = None
    cmd = "srcml --position {0} -o {0}.xml".format(file)
    with os.popen(cmd) as c1:
        cmd2 = "srcslice {0}.xml".format(file)
        with os.popen(cmd2) as c2:
            result = c2.read()
            # print(result)
            parser = Parser()
            re = parser.parse(result.split("\n"))
    
    return re



# input: AllSP
# output: variable/ function/ file level's slicing vector: [Vector()]
def sps2vecs(all_sp):
    vecset = []

    for file_name, file_sp in all_sp.file_sp_dict.items ():
        for func_name, func_sp in file_sp.func_sp_dict.items ():
            for var_name in func_sp.var_sp_dict:
                print("{0}-{1}-{2} : {3}".format(file_name, func_name, var_name, func_sp.get_vvector_by_name(var_name).vec()))
            print("{0}-{1} : {2}".format(file_name, func_name,func_sp.get_vector().vec()))
            
    return vecset


def main(file1, file2):
    slice_profiles_1 = src2sps(file1)
    slicing_vectors_1 = sps2vecs(slice_profiles_1)

    slice_profiles_2 = src2sps(file2)
    slicing_vectors_2 = sps2vecs(slice_profiles_2)

    # similarity and matching
    crANN = CRANN(slicing_vectors_1)
    match_num = 0
    for vector in slicing_vectors_2:
        if crANN.query_bool(vector):
            match_num += 1
    probability = float(match_num)/float(len(slicing_vectors_2))
    print(probability)
    return probability




if __name__ == "__main__":
    if len(sys.argv)<3:
        exit("Usage: python3 srcClone.py file1 file2")
    main(sys.argv[1], sys.argv[2])