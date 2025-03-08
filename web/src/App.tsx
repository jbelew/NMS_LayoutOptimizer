import { UpdateIcon } from "@radix-ui/react-icons";
import { IconButton, Flex, ScrollArea, Separator, Box, Text } from "@radix-ui/themes";

import React from "react";
import GridTable from "./components/GridTable"; // Corrected import path
import { useGridStore } from "./store/useGridStore";

import NMSLogo from "./assets/svg/nms_logo.svg";


const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState, activateRow, deActivateRow, resetGrid } = useGridStore();

  return (
    <div className="flex justify-center min-h-screen">
      <div className="w-full max-w-6xl p-4 m-8 mx-auto border-2 rounded-lg shadow-lg bg-cyan-900 border-cyan-700">
        <img src={NMSLogo} alt="No Man's Sky Logo" className="max-w-6xl mt-2 mb-3 invert brightness-0 saturate-100 " />

        <h1 className="text-3xl">STARSHIP OPTIMIZER v0.1</h1>
        <hr className="p-2 mt-2 border-cyan-700" />

        <div className="grid grid-cols-4 height-full">
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

          <div className="max-h-full col-span-1">
            <h2 className="pb-2 text-2xl">TECHNOLOGY SELECTION</h2>
            <ScrollArea type="always" scrollbars="vertical" className="rounded-md bg-cyan-950">
              <Box p="4">
                <h2 className="text-2xl">WEAPONS</h2>
                <Separator orientation="horizontal" size="4" className="mb-4" />
                <OptimizationButton label="Infraknife Accelerator" onClick={() => handleOptimize("infra")} loading={loading} />
                <OptimizationButton label="Photon Cannons" onClick={() => handleOptimize("photon")} loading={loading} />
                <OptimizationButton label="Missile Launchers" onClick={() => handleOptimize("missile")} loading={loading} />
                <h2 className="mt-4 text-2xl">MOBILITY</h2>
                <Separator orientation="horizontal" size="4" className="mb-4" />
                <OptimizationButton label="Starships Shields" onClick={() => handleOptimize("shield")} loading={loading} />

                <h2 className="mt-4 text-2xl">ADDITIONAL TECHNOLOGY</h2>
              </Box>
            </ScrollArea>
          </div>
        </div>
      </div>
    </div>
  );
};

// OptimizationButton component for reusability
const OptimizationButton: React.FC<{ label: string; onClick: () => void; loading: boolean }> = ({ label, onClick, loading }) => (
  <Flex gap="2" align="center" className="mt-2 mb-2">
    <IconButton onClick={onClick} disabled={loading} variant="soft">
      <UpdateIcon />
    </IconButton>
    <Text>{label}</Text>
  </Flex>
);
export default App;
