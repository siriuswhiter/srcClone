from slice import SliceProfile

class Parser:
    def __init__(self):
        pass

    @staticmethod
    def readuntil(s,c):
        end = 0
        while s[end]!=c:
            end += 1
        end += 1
        return s[:end]

    # "def{2,3}" -> {2,3}
    def str2set(self, input):
        start = len(self.readuntil(input,"{"))
        return set(input[start:len(input)-1].split(","))

    # sumProd.c,sumProd,i,def{4},use{4,5,6},dvars{prod,sum},pointers{},cfuncs{}
    def parse(self, input):
        sinput = input.split(",")
        file=sinput[0]
        func=sinput[1]
        var=sinput[2]

        # def{4},use{4,5,6},dvars{prod,sum},pointers{},cfuncs{}
        left = ",".join(sinput[3:])
        defs = self.readuntil(left, "}")
        Def=self.str2set(defs)

        left = left[len(defs)+1:] # jump ,
        uses = self.readuntil(left, "}")
        Use=self.str2set(uses)

        left = left[len(uses)+1:]
        dvars = self.readuntil(left, "}")
        Dvars = self.str2set(dvars)
        
        left = left[len(dvars)+1:]
        pointers = self.readuntil(left, "}")
        Ptrs = self.str2set(pointers)

        left = left[len(pointers)+1:]
        Cfuncs = self.str2set(left)

        return SliceProfile(file, func, var, Def, Use, Dvars, Ptrs,Cfuncs)

    def parse_all(self, inputs):
        re = []
        for input in inputs:
            if input != "":
                re.append(self.parse(input))
        return re
