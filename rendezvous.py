import sys
from collections import deque

class Graph:
    def __init__(self, num_nodes, is_directed=False):
        self.num_nodes = num_nodes
        self.is_directed = is_directed
        self.adj = {}
        self.rev_adj = {}
        for i in range(num_nodes):
            self.adj[i] = []
            self.rev_adj[i] = []

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
        lines = []
        for line in f:
            if line.strip() != "":
                lines.append(line.strip())

    parts = lines[0].split()
    n = int(parts[0])
    m = int(parts[1])
    
    graph = Graph(n, is_directed)

    for i in range(1, m + 1):
        edge_parts = lines[i].split()
        u = int(edge_parts[0])
        v = int(edge_parts[1])
        graph.add_edge(u, v)

    start_parts = lines[-1].split()
    alice_start = int(start_parts[0])
    bob_start = int(start_parts[1])

    return graph, alice_start, bob_start

def find_meeting_path(graph, start_a, start_b):
    queue = deque()
    queue.append((start_a, start_b))
    
    visited = []
    visited.append((start_a, start_b))
    
    parent = {}
    parent[(start_a, start_b)] = None
    
    meeting_state = None
    
    while len(queue) > 0:
        curr = queue.popleft()
        curr_a = curr[0]
        curr_b = curr[1]
        
        if curr_a == curr_b:
            meeting_state = (curr_a, curr_b)
            break
            
        adj_a = sorted(graph.adj[curr_a])
        adj_b = sorted(graph.adj[curr_b])
        
        for next_a in adj_a:
            for next_b in adj_b:
                next_state = (next_a, next_b)
                if next_state not in visited:
                    visited.append(next_state)
                    parent[next_state] = (curr_a, curr_b)
                    queue.append(next_state)
                    
    if meeting_state is None:
        return None
        
    path = []
    curr = meeting_state
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    
    reversed_path = []
    for i in range(len(path) - 1, -1, -1):
        reversed_path.append(path[i])
        
    return reversed_path

def find_shortest_path(graph, start, target):
    queue = deque()
    queue.append(start)
    
    visited = []
    visited.append(start)
    
    parent = {}
    parent[start] = None
    
    while len(queue) > 0:
        curr = queue.popleft()
        if curr == target:
            break
            
        adj_curr = sorted(graph.adj[curr])
        for neighbor in adj_curr:
            if neighbor not in visited:
                visited.append(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)
                
    if target not in visited:
        return None
        
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
        
    reversed_path = []
    for i in range(len(path) - 1, -1, -1):
        reversed_path.append(path[i])
        
    return reversed_path

def get_distances(graph, start):
    dist = {}
    dist[start] = 0
    
    queue = deque()
    queue.append(start)
    
    while len(queue) > 0:
        curr = queue.popleft()
        adj_curr = sorted(graph.adj[curr])
        for nbr in adj_curr:
            if nbr not in dist:
                dist[nbr] = dist[curr] + 1
                queue.append(nbr)
    return dist

def print_path(path):
    t = 0
    for state in path:
        a = state[0]
        b = state[1]
        print(str(t) + ": Alice at " + str(a) + ", Bob at " + str(b))
        t = t + 1
        
    meeting_node = path[-1][0]
    meeting_time = len(path) - 1
    print("Meeting at node " + str(meeting_node) + " at time step " + str(meeting_time) + ".")

if __name__ == "__main__":
    filename, is_directed = parse_arguments()
    graph, alice_start, bob_start = read_graph(filename, is_directed)
    
    path = find_meeting_path(graph, alice_start, bob_start)
    
    if path is not None:
        print_path(path)
    else:
        print("No meeting is possible.")
        
        if is_directed == False:
            sp = find_shortest_path(graph, alice_start, bob_start)
            if sp is not None:
                if len(sp) > 2:
                    mid_idx = len(sp) // 2
                    mid_node = sp[mid_idx]
                    prev_node = sp[mid_idx - 2]
                    graph.add_edge(prev_node, mid_node)
                    print("Adding 1 edge.")
                    print("Adding " + str(prev_node) + " " + str(mid_node) + ".")
                elif len(sp) == 2:
                    candidates = []
                    adj_a = sorted(graph.adj[alice_start])
                    for nbr in adj_a:
                        if nbr != bob_start:
                            candidates.append((nbr, alice_start, bob_start))
                            
                    adj_b = sorted(graph.adj[bob_start])
                    for nbr in adj_b:
                        if nbr != alice_start:
                            candidates.append((nbr, bob_start, alice_start))
                            
                    if len(candidates) > 0:
                        candidates.sort(key=lambda x: x[0])
                        best_nbr = candidates[0][0]
                        other = candidates[0][2]
                        graph.add_edge(other, best_nbr)
                        print("Adding 1 edge.")
                        print("Adding " + str(other) + " " + str(best_nbr) + ".")
                    else:
                        print("Could not establish a rendezvous by adding edges.")
                        sys.exit(0)
                else:
                    print("Could not establish a rendezvous by adding edges.")
                    sys.exit(0)
                    
                new_path = find_meeting_path(graph, alice_start, bob_start)
                if new_path is not None:
                    print_path(new_path)
                else:
                    print("Could not establish a rendezvous by adding edges.")
            else:
                print("Could not establish a rendezvous by adding edges.")
                
        else:
            dist_a = get_distances(graph, alice_start)
            dist_b = get_distances(graph, bob_start)
            
            common_nodes = []
            for node in dist_a:
                if node in dist_b:
                    common_nodes.append(node)
            
            if len(common_nodes) == 0:
                print("Could not establish a rendezvous by adding edges.")
                sys.exit(0)
                
            best_u = -1
            min_sum = 999999
            
            for u in common_nodes:
                curr_sum = dist_a[u] + dist_b[u]
                if curr_sum < min_sum:
                    min_sum = curr_sum
                    best_u = u
                elif curr_sum == min_sum:
                    if best_u == -1 or u < best_u:
                        best_u = u
                        
            available = []
            for i in range(graph.num_nodes):
                if i != best_u:
                    available.append(i)
                
            if len(available) == 0:
                print("Could not establish a rendezvous by adding edges.")
                sys.exit(0)
                
            v1 = available[0]
            if len(available) > 1:
                v2 = available[1]
            else:
                v2 = v1
            
            to_add = []
            
            adj_u = graph.adj[best_u]
            adj_v1 = graph.adj[v1]
            
            if v1 not in adj_u:
                to_add.append((best_u, v1))
            if best_u not in adj_v1:
                to_add.append((v1, best_u))
                
            if len(available) > 1:
                adj_v2 = graph.adj[v2]
                if v2 not in adj_u:
                    to_add.append((best_u, v2))
                if v1 not in adj_v2:
                    to_add.append((v2, v1))
                    
            final_edges = []
            for e in to_add:
                if e not in final_edges:
                    final_edges.append(e)
                    
            if len(final_edges) > 0:
                print("Adding " + str(len(final_edges)) + " edges.")
                for e in final_edges:
                    graph.add_edge(e[0], e[1])
                    print("Adding " + str(e[0]) + " " + str(e[1]) + ".")
                    
            new_path = find_meeting_path(graph, alice_start, bob_start)
            if new_path is not None:
                print_path(new_path)
            else:
                print("Could not establish a rendezvous by adding edges.")