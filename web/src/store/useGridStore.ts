// src/store/useGridStore.ts
import { create } from "zustand";
import { useTechStore } from "./useTechStore"; // Import useTechStore

// Define types
export type Cell = {
  active: boolean;
  adjacency: boolean;
  adjacency_bonus: number;
  bonus: number;
  image: string | null;
  module: string | null;
  label: string;
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
const createEmptyCell = (supercharged = false, active = true): Cell => ({
  active,
  adjacency: false,
  adjacency_bonus: 0.0,
  bonus: 0.0,
  image: null,
  module: null,
  label: "",
  sc_eligible: false,
  supercharged: supercharged,
  tech: null,
  total: 0.0,
  type: "",
  value: 0,
});

const createGrid = (width: number, height: number): Grid => ({
  cells: Array.from(
    { length: height },
    () => Array.from({ length: width }, () => createEmptyCell(false, true))
    // cells: Array.from({ length: height }, (_, rowIndex) =>
    //   Array.from({ length: width }, () =>
    //     createEmptyCell(false, rowIndex >= height - 3 ? false : true)
    //   )
  ),
  width,
  height,
});

// Zustand Store
type GridStore = {
  grid: Grid;
  result: ApiResponse | null;
  solving: boolean; // Correct: Represents the grid optimization process
  setGrid: (grid: Grid) => void;
  resetGrid: () => void;
  setResult: (result: ApiResponse | null, tech: string) => void; // Add tech to setResult
  setSolving: (solving: boolean) => void;
  toggleCellState: (rowIndex: number, columnIndex: number, event: React.MouseEvent) => void;
  handleOptimize: (tech: string) => Promise<void>;
  activateRow: (rowIndex: number) => void;
  deActivateRow: (rowIndex: number) => void;
  hasTechInGrid: (tech: string) => boolean;
  resetGridTech: (tech: string) => void;
};

export const useGridStore = create<GridStore>((set, get) => ({
  grid: createGrid(10, 6),
  result: null,
  solving: false, // Correct: Represents the grid optimization process

  setGrid: (grid) => set({ grid }),
  setSolving: (solving) => set({ solving }),
  resetGrid: () => {
    set((state) => ({
      grid: createGrid(state.grid.width, state.grid.height),
      result: null,
    }));
    useTechStore.getState().clearResult(); // Clear the max_bonus when the grid is reset
  },

  setResult: (result, tech) => {
    // Add tech to setResult
    set({ result });
    if (result) {
      useTechStore.getState().setMaxBonus(tech, result.max_bonus); // Update max_bonus in useTechStore with tech
    }
  },

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
                return {
                  ...cell,
                  active: newActiveState,
                  supercharged: newActiveState ? cell.supercharged : false,
                };
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

  activateRow: (rowIndex: number) => {
    set((state) => ({
      grid: {
        ...state.grid,
        cells: state.grid.cells.map((row, rIdx) => (rIdx === rowIndex ? row.map((cell) => ({ ...cell, active: true })) : row)),
      },
    }));
  },

  deActivateRow: (rowIndex: number) => {
    set((state) => ({
      grid: {
        ...state.grid,
        cells: state.grid.cells.map((row, rIdx) => (rIdx === rowIndex ? row.map((cell) => ({ ...cell, active: false })) : row)),
      },
    }));
  },

  handleOptimize: async (tech) => {
    set({ solving: true }); // Correct: Setting the solving state
    const { grid, setGrid, setResult, setSolving } = get();

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
          ship: "Exotic",
          tech,
          grid: updatedGrid,
        }),
      });

      if (!response.ok) throw new Error("Failed to fetch data");

      const data: ApiResponse = await response.json();
      setResult(data, tech); // Pass tech to setResult
      setGrid(data.grid);
      console.log("Response from API:", data.grid);
    } catch (error) {
      console.error("Error during optimization:", error);
      setResult(null, tech); // Pass tech to setResult
    } finally {
      setSolving(false); // Correct: Setting the solving state
    }
  },

  hasTechInGrid: (tech: string): boolean => {
    const { grid } = get();
    return grid.cells.some((row) => row.some((cell) => cell.tech === tech));
  },

  resetGridTech: (tech: string) => {
    set((state) => ({
      grid: {
        ...state.grid,
        cells: state.grid.cells.map((row) =>
          row.map((cell) =>
            cell.tech === tech
              ? {
                  ...createEmptyCell(cell.supercharged, cell.active),
                  tech: null,
                } // Preserve supercharged state
              : cell
          )
        ),
      },
    }));
  },
}));
