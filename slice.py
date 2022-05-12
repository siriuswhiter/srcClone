

class SliceProfile:
    def __init__(self ,file, func, var, Def, Use, Dvars, Ptrs,Cfuncs):
        self.file = file
        self.func = func
        self.var = var
        self.Def = Def
        self.Use = Use
        self.Dvars = Dvars
        self.Ptrs = Ptrs
        self.Cfuncs = Cfuncs

class Vector:
    def __init__(self,SC, SCvg, SI, SS):
        self.SC = SC
        self.SCvg = SCvg
        self.SI = SI
        self.SS = SS