import sys
import numpy
from collections import defaultdict, deque

def count_components(graph):
    n = len(graph)
    visited = set()
    k = 0
    for start in graph.keys():
        if start in visited:
            continue
        k += 1
        stack = [start]
        while stack:
            a = stack.pop()
            if a in visited:
                continue
            visited.add(a)
            for b in graph[a]:
                stack.append(b)
    return k

def find_shortest_cycles(graph, edges):

    def bfs(src, avoid):
        visited = defaultdict(bool)
        visited[src] = True
        parent = defaultdict(lambda: -1)
        parent[src] = src
        q = deque([src])
        while q:
            u = q.pop()
            for v in graph[u]:
                if not visited[v] and v != avoid:
                    parent[v] = u
                    visited[v] = True
                    q.append(v)
        return parent

    cycles = []
    for a, b in edges:
        for v in graph.keys():
            if v == a or v == b:
                continue
            parent = bfs(a, b)
            if parent[v] == -1:
                continue
            va = []
            cur = v
            while cur != a:
                cur = parent[cur]
                va.append(cur)
            parent = bfs(b, a)
            if parent[v] == -1:
                continue
            vb = []
            cur = v
            while cur != b:
                cur = parent[cur]
                vb.append(cur)
            if len(set(va) & set(vb)):
                # Common vertex -> not a cycle
                continue
            vb.reverse()
            vab = va + vb + [v]
            cycles.append(vab)

    return cycles

def main():

    def make_vector(cycle):
        # Create the vector representation of the cycle
        vector = [0] * edge_count
        for i, vertex in enumerate(cycle):
            next_vertex = cycle[(i + 1) % len(cycle)]
            if (vertex, next_vertex) in edges:
                vector[order[(vertex, next_vertex)]] = 1
            else:
                vector[order[(next_vertex, vertex)]] = -1
        return vector

    edge_count = int(input("Enter number of edges in graph: "))

    if edge_count == 0:
        sys.exit()

    print("Enter edges (u v): ")
    graph = defaultdict(list)
    edges = set()
    order = defaultdict(int)
    for o in range(edge_count):
        u, v = map(int, input().split())
        graph[u].append(v)  # Forward edge
        graph[v].append(u)  # Backward edge
        edges.add((u, v))
        order[(u, v)] = o

    cycles = find_shortest_cycles(graph, edges)
    cycles.sort(key = len) # from shortest cycles
    basis = []

    component_count = count_components(graph)
    vertex_count = len(graph)
    dimension = edge_count - vertex_count + component_count

    for cycle in cycles:
        vector = make_vector(cycle)
        test_basis = basis + [vector]
        matrix = numpy.vstack(test_basis)
        rank = numpy.linalg.matrix_rank(matrix)

        if rank > len(basis):
            print(cycle)
            basis.append(vector)

        if len(basis) == dimension:
            break

    assert len(basis) == dimension

    print("Integral basis of the flow space of the graph:")
    for vector in basis:
        print('[', *vector, ']', sep = ' ')

if __name__ == "__main__":
    main()
