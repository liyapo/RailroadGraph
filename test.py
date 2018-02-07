import unittest
from main import * 

class TestRailroad(unittest.TestCase):

    def setUp(self):
        # count is responsible for all routes possible 
        # with (maximum number of stops) = 2^(count) 
        # which are included in all_trips dictionary

        # max num of stops = 16 when count = 4
        count = 4
        self.TestGraph = RailroadGraph()
        self.TestGraph.build("AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7", count)
        
    def test_calculate_distance(self):
        self.assertEqual(self.TestGraph.calculate_distance("A-B-C"), 9.0)
        self.assertEqual(self.TestGraph.calculate_distance("A-D"), 5.0)
        self.assertEqual(self.TestGraph.calculate_distance("A-D-C"), 13.0)
        self.assertEqual(self.TestGraph.calculate_distance("A-E-B-C-D"), 22.0)
        self.assertEqual(self.TestGraph.calculate_distance("A-E-D"), "NO SUCH ROUTE")

    def test_calculate_trips_max_stops(self):
        self.assertEqual(self.TestGraph.calculate_trips_max_stops("C-C", 3), 2)

    def test_calculate_trips_exact_number_stops(self):
        self.assertEqual(self.TestGraph.calculate_trips_exact_number_stops("A-C", 4), 3)

    def test_calculate_shortest_route(self):
        self.assertEqual(self.TestGraph.calculate_shortest_route("A-C"), 9)
        self.assertEqual(self.TestGraph.calculate_shortest_route("B-B"), 9)

    def test_calculate_number_diff_routes(self):
        self.assertEqual(self.TestGraph.calculate_number_diff_routes("C-C", 30), 7)
        
if __name__ == 'main':
    unittest.main()
