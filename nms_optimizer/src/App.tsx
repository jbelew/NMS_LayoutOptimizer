import React, { useState, useEffect } from "react";

// Define the types for the grid and request body
type Cell = {
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

type Grid = {
  cells: Cell[][];
  height: number;
  width: number;
};

type ApiResponse = {
  grid: Grid;
  max_bonus: number;
};

// Utility functions
const createEmptyCell = (supercharged = false): Cell => ({
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

const App: React.FC = () => {
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [grid, setGrid] = useState<Grid>(createGrid(4, 3));

  /**
   * Handles optimization request
   * @param {string} tech The technology to optimize
   */
  const handleOptimize = (tech: string) => async () => {
    setLoading(true);
  
    // Create a new grid without modifying state immediately
    const updatedGrid: Grid = {
      ...grid,
      cells: grid.cells.map(row =>
        row.map(cell => (cell.tech === tech ? createEmptyCell(cell.supercharged) : cell))
      ),
    };
  
    try {
      const response = await fetch("http://localhost:5000/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tech,
          grid: updatedGrid, // Send the cleaned-up grid to the API
          initial_temp: 5000,
          cooling_rate: 0.9995,
          max_iterations: 20000,
          patience: 500,
          decay_factor: 0.995,
        }),
      });
  
      if (!response.ok) throw new Error("Failed to fetch data");
  
      const data: ApiResponse = await response.json();
      setResult(data);
      setGrid(data.grid); // Update grid **only after** getting new data
    } catch (error) {
      console.error("Error during optimization:", error);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };
  
  
  /**
   * Toggles the supercharged status of a specific cell in the grid.
   * @param {number} rowIndex - The index of the row containing the cell.
   * @param {number} columnIndex - The index of the column containing the cell.
   */
  const toggleSupercharged = (rowIndex: number, columnIndex: number) => {
    setGrid(prevGrid => ({
      ...prevGrid,
      cells: prevGrid.cells.map((row, rIdx) =>
        row.map((cell, cIdx) =>
          // Check if the current cell matches the specified row and column indices
          rIdx === rowIndex && cIdx === columnIndex
            // Toggle the supercharged property of the cell
            ? { ...cell, supercharged: !cell.supercharged }
            // Return the cell unchanged if it doesn't match
            : cell
        )
      ),
    }));
  };

  // Renders the grid table
  const renderTable = () => (
    <div className="relative">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 rounded-lg">
          <div className="w-10 h-10 border-4 border-blue-500 rounded-full animate-spin border-t-transparent"></div>
        </div>
      )}
      <table className={`bg-white border-separate border-spacing-2 rounded-lg ${loading ? "opacity-50" : ""}`}>
        <tbody>
          {grid.cells.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, columnIndex) => (
                <td
                  key={columnIndex}
                  onClick={() => toggleSupercharged(rowIndex, columnIndex)}
                  className={`cursor-pointer shadow-md border-2 px-2 py-2 rounded-lg transition-colors ${
                    cell.supercharged ? "border-yellow-500" : "border-gray-300"
                  }`}
                  style={{
                    backgroundImage: cell.image ? `url(${cell.image})` : "none",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    width: "72px",
                    height: "72px",
                  }}
                >
                  <span className="text-gray-50">{parseFloat(cell.total.toFixed(2))}</span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {result && (
        <div className="mt-4">
          <p>Max Bonus: {result.max_bonus.toFixed(2)}</p>
        </div>
      )}
    </div>
  );

  useEffect(() => {
    setResult({ grid, max_bonus: 0 });
  }, [grid]);

  return (
    <div className="m-8 App">
      <h1 className="text-4xl font-bold">NMS Optimizer</h1>
      <button onClick={handleOptimize("infra")} disabled={loading}>
        {loading ? "Optimizing..." : "Optimize Infra"}
      </button>
      <button onClick={handleOptimize("shield")} disabled={loading}>
        {loading ? "Optimizing..." : "Optimize Shield"}
      </button>
      {renderTable()}
    </div>
  );
};

export default App;
