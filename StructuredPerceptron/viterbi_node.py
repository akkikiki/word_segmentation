
class Node(object):
    def __init__(self, substring):
        self.best_prev_node = None
        self.substring = substring
        self.score = 0