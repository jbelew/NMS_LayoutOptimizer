import unittest
import sys

sys.path.insert(0, '../')  # add parent directory to sys.path
from service.optimizer import Grid, calculate_adjacency_bonus

class TestCalculateAdjacencyBonus(unittest.TestCase):
    def test_adjacent_one_module(self):
        grid = Grid(4, 4)
        grid.set_module(1, 1, "1")
        grid.set_tech(1, 1, "tech1")
        x, y = 1, 1
        supercharged_slots = []
        self.assertAlmostEqual(calculate_adjacency_bonus(grid, x, y), 0.0)

    def test_adjacent_empty(self):
        grid = Grid(4, 4)
        x, y = 1, 1
        supercharged_slots = []
        self.assertAlmostEqual(calculate_adjacency_bonus(grid, x, y), 0.0)

    def test_adjacent_two_modules(self):
        grid = Grid(4, 4)
        grid.set_module(0, 0, "1")
        grid.set_tech(0, 0, "tech1")
        grid.set_module(0, 1, "2")
        grid.set_tech(0, 1, "tech1")
        grid.set_adjacency(0, 0, True)
        grid.set_adjacency(0, 1, True)
        x, y = 0, 0
        supercharged_slots = []
        self.assertAlmostEqual(calculate_adjacency_bonus(grid, x, y), 0.1)

    def test_adjacent_two_modules_different_tech(self):
        grid = Grid(4, 4)
        grid.set_module(0, 0, "1")
        grid.set_tech(0, 0, "tech1")
        grid.set_module(0, 1, "2")
        grid.set_tech(0, 1, "tech2")
        grid.set_adjacency(0, 0, True)
        grid.set_adjacency(0, 1, True)
        x, y = 0, 0
        supercharged_slots = []
        self.assertAlmostEqual(calculate_adjacency_bonus(grid, x, y), 0.0)

    def test_adjacent_two_modules_no_adjacency(self):
        grid = Grid(4, 4)
        grid.set_module(0, 0, "1")
        grid.set_tech(0, 0, "tech1")
        grid.set_module(0, 1, "2")
        grid.set_tech(0, 1, "tech1")
        grid.set_adjacency(0, 0, False)
        grid.set_adjacency(0, 1, True)
        x, y = 0, 0
        supercharged_slots = []
        self.assertAlmostEqual(calculate_adjacency_bonus(grid, x, y), 0.0)

if __name__ == '__main__':
    unittest.main()