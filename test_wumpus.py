import unittest
from wumpus_Final import generate_base_map

class TestWumpusGame(unittest.TestCase):
    def test_map_generation(self):
        base_map = generate_base_map()
        self.assertEqual(len(base_map), 20)

if __name__ == "__main__":
    unittest.main()