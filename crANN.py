import lshash


class CRANN(object):
    def __init__(self, vectors):
        self.vectors = vectors
        self.lsh = lshash.LSHash(8, len(self.vectors) * len(self.vectors[0])*2)
        self.init()

    def init(self):
        for i in self.vectors:
            self.lsh.index(i)

    def insert(self, vector):
        self.lsh.index(vector)

    def query(self, query_point):
        return self.lsh.query(query_point, distance_func="hamming")

    def query_bool(self, query_point):
        if self.lsh.query(query_point, distance_func="hamming") >= 1:
            return False
        else:
            return True
