import unittest
import numpy as np
from wumpus_Final import (generate_base_map, place_wumpus, is_near_pit, is_near_bats,
                          is_near_wumpus, base_map, pits, bats, wumpus_x, wumpus_y,
                          size, player_x, player_y)

class TestWumpusGame(unittest.TestCase):
    def setUp(self):
        generate_base_map()
        place_wumpus()

    def test_base_map_generated(self):
        self.assertIsInstance(base_map, np.ndarray)
        self.assertEqual(base_map.shape, (size, size))
        self.assertIn(0, base_map)
        self.assertIn(1, base_map)

    def test_pits_and_bats_generated(self):
        self.assertGreater(len(pits), 0)
        self.assertGreater(len(bats), 0)
        for pit in pits:
            self.assertNotEqual(pit, (player_x, player_y))
        for bat in bats:
            self.assertNotEqual(bat, (player_x, player_y))

    def test_wumpus_placement(self):
        self.assertIsNotNone(wumpus_x)
        self.assertIsNotNone(wumpus_y)
        self.assertNotEqual((wumpus_x, wumpus_y), (player_x, player_y))
        self.assertEqual(base_map[wumpus_y][wumpus_x], 1)

    def test_proximity_detection(self):
        if pits:
            pit_x, pit_y = pits[0]
            near_x = pit_x + 1 if pit_x + 1 < size else pit_x - 1
            self.assertTrue(is_near_pit(near_x, pit_y))

        if bats:
            bat_x, bat_y = bats[0]
            near_x = bat_x + 1 if bat_x + 1 < size else bat_x - 1
            self.assertTrue(is_near_bats(near_x, bat_y))

        if wumpus_x is not None and wumpus_y is not None:
            near_x = wumpus_x + 1 if wumpus_x + 1 < size else wumpus_x - 1
            self.assertTrue(is_near_wumpus(near_x, wumpus_y))

if __name__ == "__main__":
    unittest.main()
