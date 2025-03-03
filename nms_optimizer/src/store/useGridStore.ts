import { create } from "zustand";

// Define types
export type Cell = {
  active: boolean;
  adjacency: boolean;
  adjacency_bonus: number;
  bonus: number;
  image: string | null;
  module: string | null;
  sc_eligible: boolean;
  supercharged: boolean;
  tech: string | null;
  total: number;
  type: string;
  value: number;
};

export type Grid = {
  cells: Cell[][];
  height: number;
  width: number;
};

export type ApiResponse = {
  grid: Grid;
  max_bonus: number;
};

// Utility functions
const createEmptyCell = (supercharged = false): Cell => ({
  active: true, 
  adjacency: false,
  adjacency_bonus: 0.0,
  bonus: 0.0,
  image: null,
  module: null,
  sc_eligible: false,
  supercharged: supercharged,
  tech: null,
  total: 0.0,
  type: "",
  value: 0,
});

const createGrid = (width: number, height: number): Grid => ({
  cells: Array.from({ length: height }, () => Array.from({ length: width }, createEmptyCell)),
  width,
  height,
});

// Zustand Store
type GridStore = {
  grid: Grid;
  result: ApiResponse | null;
  loading: boolean;
  setGrid: (grid: Grid) => void;
  setResult: (result: ApiResponse | null) => void;
  setLoading: (loading: boolean) => void;
  toggleCellState: (rowIndex: number, columnIndex: number, event: React.MouseEvent) => void;
  handleOptimize: (tech: string) => Promise<void>;
};

export const useGridStore = create<GridStore>((set, get) => ({
  grid: createGrid(10, 3),
  result: null,
  loading: false,

  setGrid: (grid) => set({ grid }),
  setResult: (result) => set({ result }),
  setLoading: (loading) => set({ loading }),

  /**
   * Toggles the active or supercharged state based on Ctrl+Click.
   */
  toggleCellState: (rowIndex, columnIndex, event) => {
	set((state) => ({
	  grid: {
		...state.grid,
		cells: state.grid.cells.map((row, rIdx) =>
		  row.map((cell, cIdx) => {
			if (rIdx === rowIndex && cIdx === columnIndex) {
			  if (event.ctrlKey) {
				// Toggle active, and force supercharged to false if becoming inactive
				const newActiveState = !cell.active;
				return { ...cell, active: newActiveState, supercharged: newActiveState ? cell.supercharged : false };
			  } else if (cell.active) {
				// Toggle supercharged only if active
				return { ...cell, supercharged: !cell.supercharged };
			  }
			}
			return cell;
		  })
		),
	  },
	}));
  },

  handleOptimize: async (tech) => {
    set({ loading: true });

    const { grid, setGrid, setResult, setLoading } = get();

    // Create a new grid without modifying state immediately
    const updatedGrid: Grid = {
      ...grid,
      cells: grid.cells.map((row) => row.map((cell) => (cell.tech === tech ? createEmptyCell(cell.supercharged) : cell))),
    };

    try {
      const response = await fetch("http://localhost:5000/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tech,
          grid: updatedGrid,
          initial_temp: 10000,
          cooling_rate: 0.9997,
          max_iterations: 20000,
          patience: 500,
          decay_factor: 0.995,
        }),
      });

      if (!response.ok) throw new Error("Failed to fetch data");

      const data: ApiResponse = await response.json();
      setResult(data);
      setGrid(data.grid);
    } catch (error) {
      console.error("Error during optimization:", error);
      setResult(null);
    } finally {
      setLoading(false);
    }
  },
}));