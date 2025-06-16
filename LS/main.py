import sys
from collections import defaultdict

def find_spanning_forest(graph):

    def dfs(current_vertex):
        """Performs DFS to find spanning tree of component"""
        for neighbor in graph[current_vertex]:
            if not visited[neighbor]:
                forest_edges.append((current_vertex, neighbor))
                visited[neighbor] = True
                dfs(neighbor)

    visited = defaultdict(bool)
    forest_edges = []

    for vertex in graph.keys():
        if not visited[vertex]:
            visited[vertex] = True
            dfs(vertex)

    return forest_edges

def main():
    """Main function to find the integral basis of the flow space of a graph."""
    edge_count = int(input("Enter number of edges in graph: "))

    if edge_count == 0:
        sys.exit()

    print("Enter edges (u v): ")
    graph = defaultdict(list)
    edges = set()
    order = defaultdict(int)
    for o in range(edge_count):
        u, v = map(int, input().split())
        graph[u].append(v)   # Forward edge
        graph[v].append(u)  # Backward edge
        edges.add((u, v))
        order[(u, v)] = o

    FE = find_spanning_forest(graph)
    basis = []

    for u, v in edges:
        if (u, v) not in FE and (v, u) not in FE:
            # Adding an edge (u, v) to forest creates a fundamental cycle
            stack = [v]
            visited = defaultdict(bool)
            parent = defaultdict(int)
            visited[v] = True
            parent[v] = -1
            while stack:
                node = stack.pop()
                if node == u:
                    break
                for neighbor in graph[node]:
                    if visited[neighbor]: continue
                    if (node, neighbor) in FE or (neighbor, node) in FE:
                        visited[neighbor] = True
                        parent[neighbor] = node
                        stack.append(neighbor)
            current = u
            cycle = [u]
            while (current != v):
                current = parent[current]
                cycle.append(current)
            cycle.reverse()

            """Create the vector representation of the cycle"""
            vector = [0] * edge_count
            for i, vertex in enumerate(cycle):
                next_vertex = cycle[(i + 1) % len(cycle)]
                if (vertex, next_vertex) in edges:
                    vector[order[(vertex, next_vertex)]] = 1
                else:
                    vector[order[(next_vertex, vertex)]] = -1
            basis.append(vector)

    print("Integral basis of the flow space of the graph:")
    for vector in basis:
        print('[', *vector, ']', sep = ' ')

if __name__ == "__main__":
    main()
