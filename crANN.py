import lshash


class CRANN(object):
    def __init__(self, vectors1, vectors2=None):
        if vectors2 is None:
            self.v2 = False
        else:
            self.v2 = True
        if self.v2:
            self.vectors = vectors1 + vectors2
        else:
            self.vectors = vectors1
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
                if distance > distance_i:
                    distance = distance_i
                if distance <= 0:
                    return 0
        return distance

    def query2(self, query_point):
        match_num = 0
        result = self.lsh.query(query_point, distance_func="hamming")
        if len(result) >= 1:
            for i in result:
                count = 0
                for j in range(len(query_point)):
                    if query_point[j] == i[0][j]:
                        count += 1
                distance = len(query_point) - count
                if distance <= 1:
                    match_num += 1
        return match_num

    def query_bool(self, query_point):
        if self.query(query_point) > 1:
            return False
        else:
            return True

    def count_probability(self, vectors2=None):
        if vectors2 is None:
            count = 0
            for v in self.vectors:
                match_num = self.query2(v)
                if match_num > 1:
                    count += 1
            return float(count) / float(len(self.vectors))
        else:
            match_num = 0
            for vector in vectors2:
                if self.query_bool(vector):
                    match_num += 1
            return float(match_num) / float(len(vectors2))