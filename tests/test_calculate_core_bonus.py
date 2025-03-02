import unittest
import sys

sys.path.insert(0, '../')  # add parent directory to sys.path
from nms_optimizer import Grid, calculate_core_bonus, populate_module_bonuses,print_grid# type: ignore

class TestCalculateCoreBonus(unittest.TestCase):

    def test_core_and_bonus_same_tech(self):
        supercharged_slots = []  # Define the supercharged locations
        grid = Grid(2, 2)
        grid.set_type(0, 0, "core")
        grid.set_tech(0, 0, "shield")
        grid.set_type(1, 1, "bonus")
        grid.set_tech(1, 1, "shield")
        grid.set_total(1, 1, 10)
        self.assertEqual(calculate_core_bonus(grid, "shield"), 10)

    def test_core_and_bonus_different_techs(self):
        grid = Grid(2, 2)
        grid.set_type(0, 0, "core")
        grid.set_tech(0, 0, "shield")
        grid.set_type(1, 1, "bonus")
        grid.set_tech(1, 1, "infra")
        grid.set_total(1, 1, 10)
        self.assertEqual(calculate_core_bonus(grid, "shield"), 0)

    def test_no_core_cells(self):
        grid = Grid(2, 2)
        grid.set_type(0, 0, "bonus")
        grid.set_tech(0, 0, "shield")
        grid.set_total(0, 0, 10)
        self.assertEqual(calculate_core_bonus(grid, "shield"), 10)

    def test_no_bonus_cells(self):
        supercharged_slots = []  # Define the supercharged locations
        grid = Grid(2, 2)
        grid.set_type(0, 0, "core")
        grid.set_tech(0, 0, "shield")
        self.assertEqual(calculate_core_bonus(grid, "shield"), 0)

    def test_supercharged_bonus_cell(self):
        grid = Grid(2, 2)
        grid.set_type(0, 0, "core")
        grid.set_tech(0, 0, "shield")
        grid.set_type(1, 0, "bonus")
        grid.set_tech(1, 0, "shield")
        grid.set_bonus(1, 0, 10)
        grid.set_supercharged(1, 0, True)  # Set the cell to react to supercharged locations
        grid.set_sc_eligible(1, 0, True)
        populate_module_bonuses(grid, "shield")
        self.assertEqual(calculate_core_bonus(grid, "shield"), 12.5)


    def test_supercharged_nobonus_cell(self):
        grid = Grid(2, 2)
        grid.set_type(0, 0, "core")
        grid.set_tech(0, 0, "shield")
        grid.set_type(1, 0, "bonus")
        grid.set_tech(1, 0, "shield")
        grid.set_total(1, 0, 10)
        grid.set_supercharged(1, 0, False)  # Set the cell to react to supercharged locations
        self.assertEqual(calculate_core_bonus(grid, "shield"), 10)

if __name__ == '__main__':
    unittest.main()