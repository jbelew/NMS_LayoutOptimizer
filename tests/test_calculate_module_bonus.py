import unittest
import sys

sys.path.insert(0, '../')  # add parent directory to sys.path
from nms_optimizer import Grid, calculate_module_bonus, print_grid # type: ignore

class TestCalculateModuleBonus(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(1, 1)
        self.grid.set_module(0, 0, "module") # type: ignore
        self.grid.set_tech(0, 0, "tech") # type: ignore
        self.grid.set_type(0, 0, "bonus") # type: ignore
        self.grid.set_sc_eligible(0, 0, True) # type: ignore
        self.grid.set_bonus(0, 0, 1.0) # type: ignore
        self.grid.set_adjacency(0, 0, True) # type: ignore
        self.grid.set_adjacency_bonus(0, 0, 1.0)
        self.grid.set_supercharged(0, 0, True)

    def test_supercharged_slot_supercharge_enabled(self):
        total_bonus = calculate_module_bonus(self.grid, 0, 0)
        self.assertAlmostEqual(total_bonus, 2.5)

    def test_supercharged_slot_supercharge_disabled(self):
        self.grid.set_supercharged(0, 0, False)
        total_bonus = calculate_module_bonus(self.grid, 0, 0)
        self.assertAlmostEqual(total_bonus, 2.0)

    def test_non_supercharged_slot(self):
        self.grid.set_supercharged(0, 0, False)
        total_bonus = calculate_module_bonus(self.grid, 0, 0)
        self.assertAlmostEqual(total_bonus, 2.0)

    def test_zero_bonus_adjacency_bonus(self):
        self.grid.set_bonus(0, 0, 0.0)
        self.grid.set_adjacency_bonus(0, 0, 0.0)
        total_bonus = calculate_module_bonus(self.grid, 0, 0)
        self.assertAlmostEqual(total_bonus, 0)

if __name__ == '__main__':
    unittest.main()
