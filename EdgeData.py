
class EdgeData:

    def __init__(self, src, dest, w):
        self.src = src
        self.dest = dest
        self.w = w

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_weight(self):
        return self.w

