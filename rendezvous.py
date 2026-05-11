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
    queue = deque([(start_a, start_b)])
    visited = {(start_a, start_b)}
    parent = {(start_a, start_b): None}
    meeting_state = None
    
    while queue:
        curr_a, curr_b = queue.popleft()
        if curr_a == curr_b:
            meeting_state = (curr_a, curr_b)
            break
            
        for next_a in sorted(graph.adj[curr_a]):
            for next_b in sorted(graph.adj[curr_b]):
                next_state = (next_a, next_b)
                if next_state not in visited:
                    visited.add(next_state)
                    parent[next_state] = (curr_a, curr_b)
                    queue.append(next_state)
                    
    if meeting_state is None:
        return None
        
    path = []
    curr = meeting_state
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path

def find_shortest_path(graph, start, target):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        curr = queue.popleft()
        if curr == target:
            break
        for neighbor in sorted(graph.adj[curr]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)
                
    if target not in visited:
        return None
        
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path

def get_distances(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        curr = queue.popleft()
        for nbr in sorted(graph.adj[curr]):
            if nbr not in dist:
                dist[nbr] = dist[curr] + 1
                queue.append(nbr)
    return dist

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
        
        if not is_directed:
            sp = find_shortest_path(graph, alice_start, bob_start)
            if sp:
                if len(sp) > 2:
                    mid_idx = len(sp) // 2
                    mid_node = sp[mid_idx]
                    prev_node = sp[mid_idx - 2]
                    graph.add_edge(prev_node, mid_node)
                    print("Adding 1 edge.")
                    print(f"Adding {prev_node} {mid_node}.")
                elif len(sp) == 2:
                    candidates = []
                    for nbr in sorted(graph.adj[alice_start]):
                        if nbr != bob_start:
                            candidates.append((nbr, alice_start, bob_start))
                    for nbr in sorted(graph.adj[bob_start]):
                        if nbr != alice_start:
                            candidates.append((nbr, bob_start, alice_start))
                    if candidates:
                        candidates.sort(key=lambda x: x[0])
                        best_nbr, owner, other = candidates[0]
                        graph.add_edge(other, best_nbr)
                        print("Adding 1 edge.")
                        print(f"Adding {other} {best_nbr}.")
                    else:
                        print("Could not establish a rendezvous by adding edges.")
                        sys.exit(0)
                else:
                    print("Could not establish a rendezvous by adding edges.")
                    sys.exit(0)
                    
                new_path = find_meeting_path(graph, alice_start, bob_start)
                if new_path:
                    print_path(new_path)
                else:
                    print("Could not establish a rendezvous by adding edges.")
            else:
                print("Could not establish a rendezvous by adding edges.")
        else:
            dist_a = get_distances(graph, alice_start)
            dist_b = get_distances(graph, bob_start)
            
            common_nodes = set(dist_a.keys()).intersection(set(dist_b.keys()))
            
            if not common_nodes:
                print("Could not establish a rendezvous by adding edges.")
                sys.exit(0)
                
            best_u = None
            min_sum = float('inf')
            
            for u in common_nodes:
                curr_sum = dist_a[u] + dist_b[u]
                if curr_sum < min_sum:
                    min_sum = curr_sum
                    best_u = u
                elif curr_sum == min_sum:
                    if best_u is None or u < best_u:
                        best_u = u