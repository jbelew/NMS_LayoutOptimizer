import { UpdateIcon } from "@radix-ui/react-icons";
import { IconButton, Flex } from "@radix-ui/themes";

import React from "react";
import GridTable from "./components/GridTable"; // Corrected import path
import { useGridStore } from "./store/useGridStore";

const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState, activateRow, deActivateRow, resetGrid } = useGridStore();

  return (
    <div className="flex justify-center min-h-screen">
      <div className="w-full max-w-6xl p-4 m-8 mx-auto border-2 rounded-lg shadow-lg bg-cyan-900 border-cyan-700">
        <h1 className="text-4xl font-bold">No Man's Sky Starship Optimizer</h1>
        <hr className="p-2 mt-2 border-cyan-500" />

        <div className="grid grid-cols-4 gap-4">
          {/* Main Grid Table */}
          <div className="col-span-3">
            <GridTable 
              grid={grid} 
              loading={loading} 
              toggleCellState={toggleCellState} 
              result={result}
              activateRow={activateRow}
              deActivateRow={deActivateRow}
              resetGrid={resetGrid}
            />
          </div>

          {/* Sidebar Actions */}
          <aside className="col-span-1 mt-2 space-y-4">
            <h2 className="text-2xl">WEAPONS</h2>
            <OptimizationButton label="Optimize Infraknife" onClick={() => handleOptimize("infra")} loading={loading} />
            <OptimizationButton label="Optimize Photon Cannons" onClick={() => handleOptimize("photon")} loading={loading} />

            <h2 className="text-2xl">MOBILITY</h2>
            <OptimizationButton label="Optimize Shields" onClick={() => handleOptimize("shield")} loading={loading} />

            <h2 className="text-2xl">ADDITIONAL TECHNOLOGY</h2>
          </aside>
        </div>
      </div>
    </div>
  );
};
// OptimizationButton component for reusability
const OptimizationButton: React.FC<{ label: string; onClick: () => void; loading: boolean }> = ({ label, onClick, loading }) => (
  <Flex gap="2" align="center">
    <IconButton onClick={onClick} disabled={loading}>
      <UpdateIcon />
    </IconButton>
    {label}
  </Flex>
);
export default App;
