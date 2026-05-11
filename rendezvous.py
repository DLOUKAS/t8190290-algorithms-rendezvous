import sys

class Graph:
    def __init__(self, num_nodes, is_directed=False):
        self.num_nodes = num_nodes
        self.is_directed = is_directed
        self.adj = {i: [] for i in range(num_nodes)}
        self.rev_adj = {i: [] for i in range(num_nodes)}

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.rev_adj[v].append(u)
        if not self.is_directed:
            self.adj[v].append(u)
            self.rev_adj[u].append(v)

def parse_arguments():
    args = sys.argv[1:]
    is_directed = False
    
    if "-d" in args:
        is_directed = True
        args.remove("-d")
        
    if len(args) != 1:
        sys.exit(1)
        
    filename = args[0]
    return filename, is_directed

def read_graph(filename, is_directed):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n, m = map(int, lines[0].split())
    graph = Graph(n, is_directed)

    for i in range(1, m + 1):
        u, v = map(int, lines[i].split())
        graph.add_edge(u, v)

    alice_start, bob_start = map(int, lines[-1].split())

    return graph, alice_start, bob_start

if __name__ == "__main__":
    filename, is_directed = parse_arguments()
    graph, alice_start, bob_start = read_graph(filename, is_directed)