import hashlib

from server_config import NODES

import mmh3

class NodeRing():

    def __init__(self, nodes, seed=0):
        assert len(nodes) > 0
        self.nodes = nodes
        self.seed = seed
        self.hash_function = lambda x: mmh3.hash(x, seed)
    
    def get_node(self, key_hex):
        high_score = -1
        winner = None
        for node in self.nodes:
            score = self.hash_function("%s-%s" % (str(node), key_hex))
            if score > high_score:
                (high_score, winner) = (score, node)
            elif score == high_score:
                (high_score, winner) = (score, max(str(node), str(winner)))
        return winner

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
        else:
            raise ValueError("No such node %s to remove" % (node))


def test():
    ring = NodeRing(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


# Uncomment to run the above local test via: python3 node_ring.py
test()