class DisjointSet:
    def __init__(self, elems):
        self.elems = elems
        self.parent = {}
        self.rank = {}
        self.size = {}
        self.max_size = 0
        for x in elems:
            self.make_set(x)
    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0
        self.size[x] = 1
        self.max_size = 1

    def union(self, x, y):
        root_x = self.find_set(x)
        root_y = self.find_set(y)
        return self.link(root_x, root_y)

    def link(self, x, y):
        if self.rank[x] > self.rank[y]:
            self.parent[y] = x
            self.size[x] += self.size[y]
            self.max_size = max(self.max_size, self.size[x])
        else:
            self.parent[x] = y
            self.size[y] += self.size[x]
            self.max_size = max(self.max_size, self.size[y])
        if self.rank[x] == self.rank[y]:
            self.rank[y] += 1

    def find_set(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find_set(self.parent[x])
            return self.parent[x]
        return x