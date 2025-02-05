import sys
import numpy
from collections import defaultdict, deque

def count_components(g):
    n = len(g)
    visited = set()
    k = 0
    for start in list(g.keys()):
        if start in visited:
            continue
        k += 1
        stack = [start]
        while stack:
            a = stack.pop()
            if a in visited:
                continue
            visited.add(a)
            for b, _, __ in g[a]:
                stack.append(b)
    return k

def find_cycles(graph, edge_count):

    def create_vector(cycle_path):
        """Create the vector representation of the cycle"""
        vector = [0] * edge_count
        for i, vertex in enumerate(cycle_path):
            next_vertex = cycle_path[(i + 1) % len(cycle_path)]
            for neighbor, direction, order in graph[vertex]:
                if neighbor == next_vertex:
                    vector[order] = direction
        return vector

    def bfs(start_vertex):
        """Performs BFS to detect cycles starting from a specific vertex."""
        queue = deque([(start_vertex, [start_vertex])])  # (current vertex, path taken)
        
        while queue:
            current_vertex, path = queue.popleft()
            
            for neighbor, direction, order in graph[current_vertex]:
                # Skip backtracking to the immediate parent
                previous_vertex = path[-2] if len(path) > 1 else None
                if neighbor == previous_vertex:
                    continue

                # Check if this neighbor completes a cycle
                if neighbor in path:
                    cycle_start_index = path.index(neighbor)
                    cycle_path = path[cycle_start_index:]

                    # Create the vector representation of the cycle
                    vector = tuple(create_vector(cycle_path))
                    inv_vector = tuple([-c for c in vector]) # Same cycle in opposite direction

                    if vector not in detected_cycles and inv_vector not in detected_cycles:
                        detected_cycles.add(vector)
                        result.append((cycle_path, vector))

                else:
                    queue.append((neighbor, path + [neighbor]))

    detected_cycles = set()
    result = []

    for vertex in graph.keys(): # Perform BFS from each vertex
        bfs(vertex)

    return sorted(result, key = lambda x: len(x[0]))

def main():
    """Main function to find the integral basis of the flow space of a graph."""
    edge_count = int(input("Enter number of edges in graph: "))

    if edge_count == 0:
        sys.exit()

    print("Enter edges (u v): ")
    graph = defaultdict(list) # (to, flow direction, edge order)
    vertices = set()
    for order in range(edge_count):
        u, v = map(int, input().split())
        graph[u].append((v, 1, order))   # Forward edge
        graph[v].append((u, -1, order))  # Backward edge
        vertices.add(u)
        vertices.add(v)

    # Find all cycles in the graph
    cycles = find_cycles(graph, edge_count)
    
    if not cycles:
        print("Graph is acyclic")
        sys.exit()
    
    """
    for cycle, vector in cycles:
        print(cycle, vector)
    """

    vertex_count = len(vertices)
    component_count = count_components(graph)
    dimension = edge_count - vertex_count + component_count

    # Construct basis
    basis = []
    for _, vector in cycles:
        # Test if adding this vector keeps the basis independent
        test_basis = basis + [vector]
        matrix = numpy.vstack(test_basis)
        rank = numpy.linalg.matrix_rank(matrix)
        
        if rank > len(basis):  # Adding this vector increases the rank
            basis.append(vector)
        
        if len(basis) == dimension:
            break

    assert len(basis) == dimension

    print("Integral basis of the flow space of the graph:")
    for vector in basis:
        print('[', *vector, ']', sep = ' ')

if __name__ == "__main__":
    main()
