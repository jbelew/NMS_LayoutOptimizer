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

  // Example request data
  const requestData: OptimizeRequest = {
    tech: "infra",
    grid: {
      cells: [
        [
          {
            adjacency: false,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            image: null,
            module: null,
            sc_eligible: false,
            supercharged: true,
            tech: null,
            total: 0.0,
            type: "",
            value: 0,
          },
          {
            adjacency: false,
            adjacency_bonus: 0.0,
            bonus: 0.0,
            image: null,
            module: null,
            sc_eligible: false,
            supercharged: true,
            tech: null,
            total: 0.0,
            type: "",
            value: 0,
          },
          {
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
          },
          {
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
          },
        ],
        [
          {
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
          },
          {
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
          },
          {
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
          },
          {
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
          },
        ],
        [
          {
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
          },
          {
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
          },
          {
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
          },
          {
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
          },
        ],
      ],
      height: 3,
      width: 4,
    },
    initial_temp: 5000,
    cooling_rate: 0.9995,
    max_iterations: 20000,
    patience: 500,
    decay_factor: 0.995,
  };

  // Function to handle the optimization request
  const handleOptimize = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/optimize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData), // Send the request data in JSON format
      });

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      const data: ApiResponse = await response.json();
      setResult(data);
      setLoading(false);
    } catch (error) {
      console.error("Error during optimization:", error);
      setResult(null);
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("Full result:", result);
    console.log("Optimized Grid:", result?.grid);
  }, [result]); // Log whenever the result state changes

  useEffect(() => {
    // Initialize result with grid data on page load
    setResult({
      grid: requestData.grid,
      max_bonus: 100, // Example value, can be dynamically set
    });
  }, []);

  // Function to render the table
  const renderTable = (): JSX.Element | null => {
    // Ensure that the result and grid are available before attempting to render
    if (!result || !result.grid || loading) {
      return <p>{loading ? "Optimizing..." : "No optimized grid data available."}</p>;
    }

    const { cells } = result.grid;

    return (
      <table className="bg-white border-separate border-spacing-2 rounded-lg">
        <tbody>
          {cells.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, columnIndex) => (
                <td
                  key={columnIndex}
                  className={`shadow-md border-2 px-2 py-2 rounded-lg ${cell.supercharged ? "border-yellow-500" : "border-gray-300"}`}
                  style={{
                    backgroundImage: cell.image ? `url(${cell.image})` : "none",
                    backgroundSize: "cover", // Ensures the image covers the whole cell
                    backgroundPosition: "center", // Centers the image within the cell
                    width: "72px", // Fix width
                    height: "72px", // Fix height
                  }}
                >
                  <span className="text-gray-50">{parseFloat(cell.total.toFixed(2))}</span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="App m-8">
      <h1 className="text-4xl font-bold">NMS Optimizer</h1>
      <button onClick={handleOptimize} disabled={loading}>
        {loading ? "Optimizing..." : "Optimize Grid"}
      </button>
      <div>{renderTable()}</div>
    </div>
  );
};

export default App;
