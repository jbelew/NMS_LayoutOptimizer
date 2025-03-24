// src/hooks/useOptimize.tsx
import { useState, useCallback } from "react";
import { useGridStore, Grid, ApiResponse } from "../store/useGridStore";
import { useSSE } from "./useSSE"; // Import useSSE

export const useOptimize = () => {
  const { setGrid, setResult, grid } = useGridStore();
  const [solving, setSolving] = useState<boolean>(false);
  const { clientId } = useSSE(); // Get clientId from useSSE

  const handleOptimize = useCallback(
    async (tech: string) => {
      setSolving(true); // Set solving to true here
      try {
        // Create a new grid without modifying state immediately
        const updatedGrid: Grid = {
          ...grid,
          cells: grid.cells.map((row) =>
            row.map((cell) =>
              cell.tech === tech
                ? {
                    ...cell,
                    module: null,
                    label: "",
                    type: "",
                    bonus: 0.0,
                    adjacency_bonus: 0.0,
                    total: 0.0,
                    value: 0,
                    image: null,
                    adjacency: false,
                    sc_eligible: false,
                    tech: null,
                  }
                : cell
            )
          ),
        };

        const response = await fetch("http://localhost:5000/optimize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            clientId: clientId, // Include clientId in the request body
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
        setResult(null, tech);
      } finally {
        console.log("useOptimize: finally block called"); // Add this log
        setSolving(false); // Set solving to false here, in the finally block
      }
    },
    [grid, setGrid, setResult, clientId] // Add clientId to the dependency array
  );

  return { solving, handleOptimize };
};
