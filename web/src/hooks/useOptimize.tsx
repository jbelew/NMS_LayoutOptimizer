// src/hooks/useOptimize.tsx
import { useState, useCallback } from "react";
import { useGridStore, Grid, ApiResponse } from "../store/useGridStore";
import { useClientUUID } from "./useClientUUID";

export const useOptimize = () => {
  const { setGrid, setResult, grid } = useGridStore();
  const [solving, setSolving] = useState<boolean>(false);
  const clientUUID = useClientUUID();

  const handleOptimize = useCallback(
    async (tech: string) => {
      if (!clientUUID) return;
      setSolving(true);
      try {
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
            ship: "Exotic",
            tech,
            grid: updatedGrid,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to fetch data");
        }

        const data: ApiResponse = await response.json();
        setResult(data, tech);
        setGrid(data.grid);
        console.log("Response from API:", data.grid);
      } catch (error) {
        console.error("Error during optimization:", error);
        setResult(null, tech);
      } finally {
        console.log("useOptimize: finally block called");
        setSolving(false);
      }
    },
    [grid, setGrid, setResult, clientUUID]
  );

  return { solving, handleOptimize };
};
