import unittest
import numpy as np
import sys
sys.path.insert(0, '../')  # add parent directory to sys.path

# Import your code here
from service.generate_training_data import set_grid_state, preprocess_data, grid_to_input, modules
from service.optimizer import Grid

class TestSetGridState(unittest.TestCase):
    def test_set_grid_state_supercharged_count(self):
        """Tests that the number of supercharged cells is within the range of 0-4."""
        grid = Grid(4, 3)  # Example 4x3 grid
        set_grid_state(grid, 4, 3)
        supercharged_count = sum(1 for row in grid.cells for cell in row if cell.get("supercharged"))
        self.assertTrue(0 <= supercharged_count <= 4)

    def test_set_grid_state_supercharged_rows(self):
        """Tests that all supercharged cells are in the first three rows."""
        grid = Grid(4, 3)  # Example 4x3 grid
        set_grid_state(grid, 4, 3)
        for row_index, row in enumerate(grid.cells):
            for cell in row:
                if cell.get("supercharged"):
                    self.assertTrue(row_index < 3)

    def test_set_grid_state_no_supercharged_inactive(self):
      """Tests to make sure no cells are both inactive and supercharged"""
      grid = Grid(4, 3)  # Example 4x3 grid
      set_grid_state(grid, 4, 3)
      for row_index, row in enumerate(grid.cells):
        for cell in row:
          if cell.get("supercharged"):
            self.assertTrue(cell.get("active") == True)

class TestPreprocessData(unittest.TestCase):
    def test_preprocess_data_output_shape(self):
        """Tests that the preprocessed output has the correct shape."""
        grid = Grid(4, 3)
        
        # Example data: just one grid for now
        data = [(grid_to_input(grid), 0.0)]
        X_processed, y, _, _, _, _ = preprocess_data(data)

        # Expected X shape: (number of grids, num_features * number_of_cells)
        # Each grid has 4*3=12 cells, and each cell has 7 features
        expected_X_shape = (1, 12 * 7)  #one grid

        self.assertEqual(X_processed.shape, expected_X_shape)

    def test_preprocess_data_all_modules_represented(self):
        """Tests that all modules are represented in the encoding."""
        grid = Grid(4, 3)
        # Example data: just one grid for now
        data = [(grid_to_input(grid), 0.0)]
        _, _, module_encoder, _, _, _ = preprocess_data(data)
        all_modules = [module["name"] for module in modules]

        # Check that all categories are in the encoder
        for module in all_modules:
            found = False
            for category_list in module_encoder.categories_:
                for category in category_list:
                    if category == module:
                        found = True
            self.assertTrue(found, f"Module '{module}' not found in module_encoder categories")

    def test_preprocess_data_all_types_represented(self):
        """Tests that all types are represented in the encoding."""
        grid = Grid(4, 3)
        # Example data: just one grid for now
        data = [(grid_to_input(grid), 0.0)]
        _, _, _, _, type_encoder, _ = preprocess_data(data)
        all_types = [module["type"] for module in modules]

        # Check that all categories are in the encoder
        for type in all_types:
            found = False
            for category_list in type_encoder.categories_:
                for category in category_list:
                    if category == type:
                        found = True
            self.assertTrue(found, f"type '{type}' not found in type_encoder categories")

    def test_preprocess_data_all_techs_represented(self):
        """Tests that all techs are represented in the encoding."""
        grid = Grid(4, 3)
        # Example data: just one grid for now
        data = [(grid_to_input(grid), 0.0)]
        _, _, _, tech_encoder, _, _ = preprocess_data(data)
        all_techs = [module["tech"] for module in modules]

        # Check that all categories are in the encoder
        for tech in all_techs:
            found = False
            for category_list in tech_encoder.categories_:
                for category in category_list:
                    if category == tech:
                        found = True
            self.assertTrue(found, f"tech '{tech}' not found in tech_encoder categories")
