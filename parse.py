from slice import *

class Parser:
    def __init__(self):
        self.all_sp = AllSP()

    @staticmethod
    def readuntil(s,c):
        if s=="":
            return s
        end = 0
        while end<len(s) and s[end]!=c:
            end += 1
        end += 1
        return s[:end]

    # "def{2,3}" -> {2,3}
    def str2set(self, input):
        start = len(self.readuntil(input,"{"))
        content = input[start:len(input)-1]
        if content != "":
            return set(content.split(","))-set([""])
        else:
            return set()

        # funcname -> list
    def __parse_cfuncs(self, input):
        Cfuncs = {}
        # cfuncs{foo{1},foo{2}}
        start = len(self.readuntil(input,"{"))
        content = input[start:len(input)]
        # foo{1},foo{2}}
        while True:
            name_start = 0
            name_end = len(self.readuntil(content, "{")) -1
            func_name = content[name_start:name_end]

            if func_name == "":
                break
            arg_line_start = name_end + 1
            arg_line_end = len(self.readuntil(content, "}")) -1
            arg_lines = set([int(i) for i in content[arg_line_start:arg_line_end].split(",")])

            if Cfuncs.get(func_name) == None:
                Cfuncs[func_name] = arg_lines
            else:
                Cfuncs[func_name] = Cfuncs[func_name].union(arg_lines)
        
            if content[arg_line_end+1] == "}":
                break
            else:
                content = content[arg_line_end+2:]
        return Cfuncs

    # sumProd.c,sumProd,i,def{4},use{4,5,6},dvars{prod,sum},pointers{},cfuncs{}
    def __parse(self, input):
        sinput = input.split(",")
        file=sinput[0]
        func=sinput[1]
        var=sinput[2]

        # def{4},use{4,5,6},dvars{prod,sum},pointers{},cfuncs{}
        left = ",".join(sinput[3:])
        defs = self.readuntil(left, "}")
        Def=set([int(i) for i in self.str2set(defs)]) 

        left = left[len(defs)+1:]
        uses = self.readuntil(left, "}")
        Use=set([int(i) for i in self.str2set(uses)]) 

        left = left[len(uses)+1:]
        dvars = self.readuntil(left, "}")
        Dvars = self.str2set(dvars)
        
        left = left[len(dvars)+1:]
        pointers = self.readuntil(left, "}")
        Ptrs = self.str2set(pointers)

        left = left[len(pointers)+1:]
        Cfuncs = self.__parse_cfuncs(left)

        sp = SliceProfile(Def, Use, Dvars, Ptrs,Cfuncs)
        vsp = VariableSP(var, sp)
        self.all_sp.get_fsp_by_name(file).get_fsp_by_name(func).add_variable_sp(vsp)

    def parse(self, inputs):
        for input in inputs:
            if input != "":
                self.__parse(input)
        return self.all_sp
