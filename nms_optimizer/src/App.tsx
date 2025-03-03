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

type OptimizeRequest = {
  tech: string;
  grid: Grid;
  initial_temp: number;
  cooling_rate: number;
  max_iterations: number;
  patience: number;
  decay_factor: number;
};

const App: React.FC = () => {
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [grid, setGrid] = useState<Grid>(createGrid(4, 3));

  // Create initial grid with default values
  function createGrid(width: number, height: number): Grid {
    return {
      cells: Array.from({ length: height }, () =>
        Array.from({ length: width }, () => ({
          adjacency: false,
          adjacency_bonus: 0.0,
          bonus: 0.0,
          image: null,
          module: null,
          sc_eligible: false,
          supercharged: false,
          tech: null,
          total: 0.0,
          type: "",
          value: 0,
        }))
      ),
      width,
      height,
    };
  }

  const handleOptimize = (tech: string) => async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(createRequestData(grid, tech), null, 2),
      });

      console.log(JSON.stringify(createRequestData(grid, tech), null, 2))

      if (!response.ok) throw new Error("Failed to fetch data");

      const data: ApiResponse = await response.json();
      setResult(data);
      setGrid(data.grid); // Update grid with result data
    } catch (error) {
      console.error("Error during optimization:", error);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  // Create request data for optimization
  const createRequestData = (grid: Grid, tech: string): OptimizeRequest => ({
    tech,
    grid,
    initial_temp: 5000,
    cooling_rate: 0.9995,
    max_iterations: 20000,
    patience: 500,
    decay_factor: 0.995,
  });

  // Toggle supercharged status of a cell
  const toggleSupercharged = (rowIndex: number, columnIndex: number) => {
    const updatedCells = grid.cells.map((row, rIdx) =>
      row.map((cell, cIdx) =>
        rIdx === rowIndex && cIdx === columnIndex
          ? { ...cell, supercharged: !cell.supercharged }
          : cell
      )
    );
    setGrid({ ...grid, cells: updatedCells });
  };

  // Render the table
  const renderTable = (): JSX.Element => {
    const { cells } = grid;
    return (
      <div className="relative">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 rounded-lg">
            <div className="w-10 h-10 border-4 border-blue-500 rounded-full animate-spin border-t-transparent"></div>
          </div>
        )}
        <table className={`bg-white border-separate border-spacing-2 rounded-lg ${loading ? "opacity-50" : ""}`}>
          <tbody>
            {cells.map((row, rowIndex) => (
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
  };

  useEffect(() => {
    // Initialize result with grid data on page load
    setResult({ grid, max_bonus: 0 });
  }, []);

  return (
    <div className="m-8 App">
      <h1 className="text-4xl font-bold">NMS Optimizer</h1>
      <button onClick={handleOptimize("infra")} disabled={loading}>
        {loading ? "Optimizing..." : "Optimize Infra"}
      </button>
      <button onClick={handleOptimize("shield")} disabled={loading}>
        {loading ? "Optimizing..." : "Optimize Sheild"}
      </button>
      {renderTable()}
    </div>
  );
};

export default App;
