import unittest
from main import count_components, find_cycles
from collections import defaultdict

class TestGraphFunctions(unittest.TestCase):

    def setUp(self):
        self.graph1 = defaultdict(list, {
            1: [(2, 1, 0), (4, 1, 2)],
            2: [(1, -1, 0), (4, 1, 1), (3, 1, 3)],
            4: [(2, -1, 1), (1, -1, 2), (3, 1, 4)],
            3: [(2, -1, 3), (4, -1, 4)]
        })

        self.graph2 = defaultdict(list, {
            1: [(3, 1, 0), (2, -1, 1)],
            2: [(1, 1, 1), (4, 1, 2), (3, 1, 4)],
            4: [(2, -1, 2), (3, -1, 5), (1, -1, 3)],
            3: [(1, -1, 0), (4, 1, 5), (2, -1, 4)]
        })

        self.acyclic_graph = defaultdict(list, {
            1: [(2, 1, 0)],
            2: [(1, -1, 0), (3, 1, 1)],
            3: [(2, -1, 1)]
        })

        self.disconnected_graph = defaultdict(list, {
            1: [(2, 1, 0)],
            2: [(1, -1, 0)],
            3: [(4, 1, 1)],
            4: [(3, -1, 1)]
        })

    def test_count_components(self):
        self.assertEqual(count_components(self.graph1), 1)
        self.assertEqual(count_components(self.disconnected_graph), 2)

    def test_find_cycles(self):
        result = find_cycles(self.graph1, 5)
        expected_cycles = [
            ([1, 2, 4], [1, 1, -1, 0, 0]),
            ([2, 4, 3], [0, 1, 0, -1, 1]),
            ([1, 2, 3, 4], [1, 0, -1, 1, -1])
        ]

        self.assertEqual(result, expected_cycles)

        result = find_cycles(self.acyclic_graph, 2)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
