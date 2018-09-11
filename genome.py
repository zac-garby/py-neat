from random import randrange, random, choice
from gene import Connection, Node, NodeType
from graphviz import Digraph

class Genome(object):
    def __init__(self):
        self.connections = {}
        self.nodes = {}
        self.conn_innovation = 0
        self.node_innovation = 0
        self.perturb_prob = 0.9
    
    def conn_inno(self):
        val = self.conn_innovation
        self.conn_innovation += 1
        return val
    
    def node_inno(self):
        val = self.node_innovation
        self.node_innovation += 1
        return val

    def add_connection(self, conn):
        self.connections[conn.innovation] = conn

    def add_node(self, node):
        self.nodes[node.id] = node
    
    def mutate_connection(self):
        if len(self.nodes) == 1:
            return
        
        index_1 = choice(list(self.nodes.keys()))
        index_2 = choice(list(self.nodes.keys()))

        while index_1 == index_2:
            index_2 = choice(list(self.nodes.keys()))
        
        node_1 = self.nodes[index_1]
        node_2 = self.nodes[index_2]

        if (node_1.type == NodeType.hidden and node_2.type == NodeType.inp) or (node_1.type == NodeType.out and node_2.type == NodeType.hidden) or (node_1.type == NodeType.out and node_2.type == NodeType.inp):
            node_1, node_2 = node_2, node_1

        for (_, conn) in self.connections.items():
            # Already connected
            if (conn.inp == node_1.id and conn.out == node_2.id) or (conn.inp == node_2.id and conn.out == node_1.id):
                self.mutate_connection()
                return

        self.add_connection(Connection(
            index_1,
            index_2,
            random() * 2.0 - 1.0,
            True,
            self.conn_inno(),
        ))
    
    def mutate_node(self):
        conn = choice(list(self.connections.values()))
        inp = self.nodes[conn.inp]
        out = self.nodes[conn.out]

        conn.expressed = False

        new = Node(NodeType.hidden, self.node_inno())
        in_to_new = Connection(inp.id, new.id, 1.0, True, self.conn_inno())
        new_to_out = Connection(new.id, out.id, conn.weight, True, self.conn_inno())

        self.add_node(new)
        self.add_connection(in_to_new)
        self.add_connection(new_to_out)
    
    def mutate_weights(self):
        for conn in self.connections.values():
            if random() < self.perturb_prob:
                conn.weight = conn.weight * (random() * 4.0 - 2.0)
            else:
                conn.weight = random() * 4.0 - 2.0
    
    def render(self, filename):
        dot = Digraph()

        for (i, node) in self.nodes.items():
            dot.node(str(i))
        
        for (i, conn) in self.connections.items():
            if conn.expressed:
                dot.edge(str(conn.inp), str(conn.out), "{:.0f}, {:.2f}".format(conn.innovation, conn.weight))
        
        dot.render(filename, view=True)
    
    @staticmethod
    def crossover(a, b):
        child = Genome()

        for (_, parent_node) in a.nodes.items():
            child.add_node(parent_node.copy())
        
        for (_, parent_conn) in a.connections.items():
            if parent_conn.innovation in b.connections:
                # Matching gene
                if random() < 0.5:
                    child_conn = parent_conn.copy()
                else:
                    child_conn = b.connections[parent_conn.innovation].copy()
                child.add_connection(child_conn)
            else:
                # Disjoint/excess gene
                child.add_connection(parent_conn.copy())
        
        return child

    @staticmethod
    def matching_genes(a, b):
        return _matching_genes(a.nodes, b.nodes) + _matching_genes(a.connections, b.connections)
    
    @staticmethod
    def disjoint_genes(a, b):
        return _disjoint_genes(a.nodes, b.nodes) + _disjoint_genes(a.connections, b.connections)
    
    @staticmethod
    def excess_genes(a, b):
        return _excess_genes(a.nodes, b.nodes) + _disjoint_genes(a.connections, b.connections)
    
    @staticmethod
    def max_gene_num(a, b):
        nodes = max(len(a.nodes), len(b.nodes))
        connections = max(len(a.connections), len(b.connections))
        return nodes + connections
    
    @staticmethod
    def avg_weight_diff(a, b):
        matching_genes = 0
        weight_diff = 0

        max_a = max(a_dict.keys())
        max_b = max(b_dict.keys())
        indices = max(max_a, max_b)

        for i in range(indices+1):
            if i in a_dict and i in b_dict:
                matching_genes += 1
                weight_diff += abs(a_dict[i].weight - b_dict[i].weight)
        
        return weight_diff / matching_genes
    
    @staticmethod
    def compatability_distance(a, b, c1, c2, c3):
        N = Genome.max_gene_num(a, b)
        E = Genome.excess_genes(a, b)
        D = Genome.disjoint_genes(a, b)
        W = Genome.avg_weight_diff(a, b)

        return (c1 * E + c2 * D) / N + c3 * W

def _matching_genes(a_dict, b_dict):
    matching_genes = 0

    max_a = max(a_dict.keys())
    max_b = max(b_dict.keys())
    indices = max(max_a, max_b)

    for i in range(indices+1):
        if i in a_dict and i in b_dict:
            matching_genes += 1
    
    return matching_genes

def _disjoint_genes(a_dict, b_dict):
    disjoint_genes = 0

    max_a = max(a_dict.keys())
    max_b = max(b_dict.keys())
    indices = max(max_a, max_b)

    for i in range(indices+1):
        if (i not in a_dict and i in b_dict and max_a > i) or (i in a_dict and i not in b_dict and max_b > i):
            disjoint_genes += 1
    
    return disjoint_genes

def _excess_genes(a_dict, b_dict):
    excess_genes = 0

    max_a = max(a_dict.keys())
    max_b = max(b_dict.keys())
    indices = max(max_a, max_b)

    for i in range(indices+1):
        if (i not in a_dict and i in b_dict and max_a < i) or (i in a_dict and i not in b_dict and max_b < i):
            excess_genes += 1
    
    return excess_genes
