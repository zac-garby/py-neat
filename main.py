from genome import Genome
from gene import Connection, Node, NodeType

def main():
    test_crossover()
    test_conn_mut()
    test_node_mut()

def test_crossover():
    a = Genome()
    for i in range(3):
        a.add_node(Node(NodeType.inp, i+1))
    a.add_node(Node(NodeType.out, 4))
    a.add_node(Node(NodeType.hidden, 5))
    a.add_connection(Connection(1, 4, 1.0, True, 1))
    a.add_connection(Connection(2, 4, 1.0, False, 2))
    a.add_connection(Connection(3, 4, 1.0, True, 3))
    a.add_connection(Connection(2, 5, 1.0, True, 4))
    a.add_connection(Connection(5, 4, 1.0, True, 5))
    a.add_connection(Connection(1, 5, 1.0, True, 8))

    b = Genome()
    for i in range(3):
        b.add_node(Node(NodeType.inp, i+1))
    b.add_node(Node(NodeType.out, 4))
    b.add_node(Node(NodeType.hidden, 5))
    b.add_node(Node(NodeType.hidden, 6))
    b.add_connection(Connection(1, 4, 1.0, True, 1))
    b.add_connection(Connection(2, 4, 1.0, False, 2))
    b.add_connection(Connection(3, 4, 1.0, True, 3))
    b.add_connection(Connection(2, 5, 1.0, True, 4))
    b.add_connection(Connection(5, 4, 1.0, False, 5))
    b.add_connection(Connection(5, 6, 1.0, True, 6))
    b.add_connection(Connection(6, 4, 1.0, True, 7))
    b.add_connection(Connection(3, 5, 1.0, True, 9))
    b.add_connection(Connection(1, 6, 1.0, True, 10))

    c = Genome.crossover(b, a)

    a.render("render/crossover_a.gv")
    b.render("render/crossover_b.gv")
    c.render("render/crossover_c.gv")

def test_conn_mut():
    a = Genome()
    a.add_node(Node(NodeType.inp, 1))
    a.add_node(Node(NodeType.inp, 2))
    a.add_node(Node(NodeType.out, 3))
    a.add_connection(Connection(1, 3, 1.0, True, 1))
    a.add_connection(Connection(2, 3, 1.0, True, 2))
    a.next_inno = 3

    a.render("render/conn_begin.gv")
    a.mutate_connection()
    a.render("render/conn_mutated.gv")

def test_node_mut():
    a = Genome()
    a.add_node(Node(NodeType.inp, 1))
    a.add_node(Node(NodeType.inp, 2))
    a.add_node(Node(NodeType.out, 3))
    a.add_connection(Connection(1, 3, 1.0, True, 1))
    a.add_connection(Connection(2, 3, 1.0, True, 2))
    a.next_inno = 3

    a.render("render/node_begin.gv")
    a.mutate_node()
    a.render("render/node_mutated.gv")

if __name__ == "__main__":
    main()