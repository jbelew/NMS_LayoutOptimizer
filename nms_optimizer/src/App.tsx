import { UpdateIcon } from "@radix-ui/react-icons";
import { IconButton, Strong, Text } from "@radix-ui/themes";

import React from "react";
import GridTable from "../src/components/GridTable"; // Import the GridTable component
import { useGridStore } from "./store/useGridStore";

const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState } = useGridStore();

  return (
    <div className="flex justify-center min-h-screen">
    <div className="w-full max-w-6xl p-4 m-8 mx-auto border-2 rounded-lg shadow-lg bg-cyan-900 border-cyan-700">
      <h1 className="p-2 text-4xl font-bold">No Man's Sky Starship Optimizer</h1>
      <hr className="p-2 mt-2 border-cyan-500" />
  
      <div className="grid grid-cols-4 gap-4">
        {/* Main Grid Table */}
        <div className="col-span-3">
          <GridTable
            grid={grid}
            loading={loading}
            toggleCellState={toggleCellState}
            result={result}
          />
        </div>
  
        {/* Sidebar Actions */}
        <div className="col-span-1 mt-2 space-y-4">
          <h2 className="text-2xl">WEAPONS</h2>
          {/* Icon Button with Label */}
          <div className="flex items-center w-full">
            <IconButton onClick={() => handleOptimize("infra")} loading={loading}>
              <UpdateIcon width="18" height="18" />
            </IconButton>
            <Text className="!ml-2"><Strong>Optimize Infraknife</Strong></Text>
          </div>
          <div className="flex items-center w-full">
            <IconButton onClick={() => handleOptimize("photon")} loading={loading}>
              <UpdateIcon width="18" height="18" />
            </IconButton>
            <Text className="!ml-2"><Strong>Optimize Photon Cannons</Strong></Text>
          </div>

          <h2 className="text-2xl">MOBILITY</h2>
          {/* Icon Button with Label */}
          <div className="flex items-center w-full">
            <IconButton onClick={() => handleOptimize("shield")} loading={loading}>
              <UpdateIcon width="18" height="18" />
            </IconButton>
            <Text className="!ml-2"><Strong>Optimize Shields</Strong></Text>
          </div>

          <h2 className="text-2xl">ADDITIONAL TECHNOLOGY</h2>
          
        </div>
      </div>
    </div>
  </div>
  
  );
};

export default App;
