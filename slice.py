import sys

class SliceProfile:
    def __init__(self, Def, Use, Dvars, Ptrs,Cfuncs):
        self.Def = Def
        self.Use = Use
        self.Dvars = Dvars
        self.Ptrs = Ptrs
        self.Cfuncs = Cfuncs

class VariableSP:
    def __init__(self, name, sp):
        self.name = name
        self.sp = sp

class FunctionSP:
    def __init__(self, name):
        self.name = name
        self.var_sp_dict = {}
        self.var_slice_dict = {}
        self.var_vector_dict = {}
        self.sp = None
        self.slice = None
        self.vector = None

    def add_variable_sp(self, var_sp):
        self.var_sp_dict[var_sp.name] = var_sp.sp

    def get_vsp_by_name(self, var_name):
        return self.var_sp_dict.get(var_name)

    def get_vslice_by_name(self, var_name):
        vslice = self.var_slice_dict.get(var_name)
        if vslice == None:
            vslice = self.__calc_vslice_by_name(var_name)
            self.var_slice_dict[var_name] = vslice
        return vslice

    def get_vvector_by_name(self, var_name):
        vvector = self.var_vector_dict.get(var_name)
        if vvector == None:
            vvector = self.__calc_vvector_by_name(var_name)
            self.var_vector_dict[var_name] = vvector
        return vvector

    def get_sp(self):
        if self.sp == None:
            self.sp = self.__calc_sp()
        return self.sp

    def get_slice(self):
        if self.slice == None:
            self.__calc_slice()
        return self.slice

    def get_vector(self):
        if self.vector == None:
            self.vector = self.__calc_vector()
        return self.vector

    '''
      The complete slice is computed by srcSlice by taking the union of the slice profile
    of the slicing variable (that is, definition (Def) and use (Use) sets) with the slice profiles 
    of the identifiers included in the dependent variables (Dvars), called functions (Cfuncs), and 
    pointers (Ptrs) fields of the slicing variable, minus any lines that are before the initial 
    definition of the slicing variable (that is, the set {1, ... ,def(v)-1}).
    '''
    def __calc_vslice_by_name(self, var_name):
        vsp = self.get_vsp_by_name(var_name)
        if vsp == None:
            sys.exit("can't find {}'s slice profile.".format(var_name))

        re = set()
        re = re.union(vsp.Def)
        re = re.union(vsp.Use)

        #  union dvars slice
        for dvar in vsp.Dvars:
            re = re.union(self.get_vslice_by_name(dvar))
        
        #  union ptrs slice
        for ptr in vsp.Ptrs:
            re = re.union(self.get_vslice_by_name(ptr))

        # TODO
        #  union cfuncs slice
        # for cfunc in vsp.Cfuncs:
        #     re = re.union(self.get_vslice_by_name(cfunc))


        # before def
        max_s = min(vsp.Def) - 1
        before_def = set([i+1 for i in range(max_s)])
        # minus lines before definition
        re = re - before_def
        
        return re

    def __calc_vvector_by_name(self, var_name):
        CS = self.get_vslice_by_name(var_name)

        # right?
        w = max(self.get_slice())

        sp = self.get_vsp_by_name(var_name)

        # the number of slice profiles united to form the final slice.
        SC = 1 + len(sp.Dvars) + len(sp.Ptrs) + len(sp.Cfuncs)

        # the number of statements in a complete final slice.
        SZ = len(CS)

        # the slice size relative to the module size measured in LOC.
        SCvg = round(SZ/w,1)

        # the number of distinct identifiers within a slice.
        s = set()
        s = s.union(sp.Dvars)
        s = s.union(sp.Ptrs)
        s = s.union(sp.Cfuncs)
        SI = len(s)

        # the spatial distance in LOC between the first definition and the last use of the
        # slicing variable divided by the module size.
        Sl = max(CS)
        Sf = min(CS)
        SS = round((Sl-Sf)/w, 1)

        return Vector(SC, SCvg, SI, SS)

    def __calc_sp(self):
        Def, Use, Dvars, Ptrs,Cfuncs = set(),set(),set(),set(),set()
        
        for vsp in self.var_sp_dict.values():
            Def = Def.union(vsp.Def)
            Use = Use.union(vsp.Use)
            Dvars = Dvars.union(vsp.Dvars)
            Ptrs = Ptrs.union(vsp.Ptrs)
            Cfuncs = Cfuncs.union(vsp.Cfuncs)

        return SliceProfile(Def, Use, Dvars, Ptrs,Cfuncs)

    def __calc_slice(self):
        self.slice = set()
        for vslice_name in self.var_sp_dict: # iterate sp_dict, not slice_dict. sp_dict may lack some variables.
            vslice = self.get_vslice_by_name(vslice_name)
            self.slice = self.slice.union(vslice)

    def __calc_vector(self):
        CS = self.get_slice()

        SC = len(self.var_sp_dict)

        w = max(CS)
        SZ = len(CS)
        SCvg = round(SZ/w,1)

        s = set()
        sp = self.get_sp()
        s = s.union(sp.Dvars)
        s = s.union(sp.Ptrs)
        s = s.union(sp.Cfuncs)
        SI = len(s)

        Sl = max(CS)
        Sf = min(CS)
        SS = round((Sl-Sf)/w, 1)

        return Vector(SC, SCvg, SI, SS)


class FileSP:
    def __init__(self, name):
        self.name = name
        self.func_sp_dict = {}


    def add_function_sp(self, func_sp):
        self.func_sp_dict[func_sp.name] = func_sp

    def get_fsp_by_name(self, func_name):
        fsp = self.func_sp_dict.get(func_name)
        if fsp == None:
            fsp = FunctionSP(func_name)
            self.func_sp_dict[func_name] = fsp
        return fsp

class AllSP:
    def __init__(self):
        self.file_sp_dict = {}

    def add_file_sp(self, file_sp):
        self.file_sp_dict[file_sp.name] = file_sp

    def get_fsp_by_name(self, file_name):
        fsp = self.file_sp_dict.get(file_name)
        if fsp == None:
            fsp = FileSP(file_name)
            self.file_sp_dict[file_name] = fsp
        return fsp

class Vector:
    def __init__(self,SC, SCvg, SI, SS):
        self.SC = SC
        self.SCvg = SCvg
        self.SI = SI
        self.SS = SS
    
    def vec(self):
        return [self.SC, self.SCvg, self.SI, self.SS]