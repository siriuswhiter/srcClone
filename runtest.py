
import os

with open("./test/pair.txt", "r") as p:
    for pair in p.readlines():
        file_0 = "./test/pairs/{0}.java".format(pair.split()[0])
        file_1 = "./test/pairs/{0}.java".format(pair.split()[1])
        cmd = "python3 srcClone.py {0} {1}".format(file_0, file_1)
        print(cmd)
        os.system(cmd)
        # sleep(1000)