import lshash


class CRANN(object):
    def __init__(self, vectors):
        self.vectors = vectors
        self.MAX = len(self.vectors[0])
        self.lsh = lshash.LSHash(6, len(self.vectors[0]))
        self.init()

    def init(self):
        for i in self.vectors:
            self.lsh.index(i)

    def insert(self, vector):
        self.lsh.index(vector)

    def query(self, query_point):
        result = self.lsh.query(query_point, distance_func="hamming")
        distance = self.MAX
        if len(result) >= 1:
            for i in result:
                count = 0
                for j in range(len(query_point)):
                    if query_point[j] == i[0][j]:
                        count += 1
                distance_i = len(query_point) - count
                if distance < distance_i:
                    distance = distance_i
                if distance <= 0:
                    return 0
        return distance

    def query_bool(self, query_point):
        if self.query(query_point) > 1:
            return False
        else:
            return True
