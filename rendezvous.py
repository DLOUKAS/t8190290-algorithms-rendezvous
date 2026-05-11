import sys
from collections import deque

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

def find_meeting_path(graph, start_a, start_b):
    # Κάνουμε BFS κρατώντας την κατάσταση (θέση Alice, θέση Bob)
    queue = deque([(start_a, start_b)])
    visited = {(start_a, start_b)}
    parent = {(start_a, start_b): None}
    
    meeting_state = None
    
    while queue:
        curr_a, curr_b = queue.popleft()
        
        # Αν έπεσαν στον ίδιο κόμβο, σταματάμε
        if curr_a == curr_b:
            meeting_state = (curr_a, curr_b)
            break
            
        # Βρίσκουμε τις επόμενες πιθανές θέσεις και για τους δύο
        for next_a in graph.adj[curr_a]:
            for next_b in graph.adj[curr_b]:
                next_state = (next_a, next_b)
                if next_state not in visited:
                    visited.add(next_state)
                    parent[next_state] = (curr_a, curr_b)
                    queue.append(next_state)
                    
    if meeting_state is None:
        return None
        
    # Φτιάχνουμε το μονοπάτι πηγαίνοντας προς τα πίσω
    path = []
    curr = meeting_state
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    
    return path

def print_path(path):
    for t, (a, b) in enumerate(path):
        print(f"{t}: Alice at {a}, Bob at {b}")
        
    meeting_node = path[-1][0]
    meeting_time = len(path) - 1
    print(f"Meeting at node {meeting_node} at time step {meeting_time}.")

if __name__ == "__main__":
    filename, is_directed = parse_arguments()
    graph, alice_start, bob_start = read_graph(filename, is_directed)
    
    path = find_meeting_path(graph, alice_start, bob_start)
    
    if path:
        print_path(path)
    else:
        print("No meeting is possible.")