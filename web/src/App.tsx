import { UpdateIcon } from "@radix-ui/react-icons";
import { IconButton, Flex, ScrollArea, Separator, Box, Text } from "@radix-ui/themes";

import React from "react";
import GridTable from "./components/GridTable"; // Corrected import path
import { useGridStore } from "./store/useGridStore";
import { useState, useEffect } from "react";

import NMSLogo from "./assets/svg/nms_logo.svg";

const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState, activateRow, deActivateRow, resetGrid } = useGridStore();
  const [techTree, setTechTree] = useState<{ [key: string]: { label: string; key: string }[] } | null>(null);

  useEffect(() => {
    const fetchTechTree = async () => {
      try {
          const response = await fetch('http://localhost:5000/tech_tree/Exotic');
          const data = await response.json();
          setTechTree(data);
      } catch (error) {
        console.error("Error fetching tech tree:", error);
        // Optionally handle the error in the UI
      }
    };

    fetchTechTree();
  }, []); 

  return (
    <div className="flex justify-center min-h-screen">
      <div className="w-full max-w-6xl p-4 m-8 mx-auto border-2 rounded-lg shadow-lg bg-cyan-900 border-cyan-700">
        <img src={NMSLogo} alt="No Man's Sky Logo" className="max-w-6xl mt-2 mb-3 invert brightness-0 saturate-100 " />

        <h1 className="text-3xl">STARSHIP OPTIMIZER v0.2</h1>
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
                {techTree && (
                  Object.entries(techTree).map(([type, technologies]) => (
                    <React.Fragment key={type}>
                      <h2 className="text-2xl">{type.toUpperCase()}</h2>
                      <Separator orientation="horizontal" size="4" className="mb-4" />
                      {technologies.map((tech) => (
                        <OptimizationButton key={tech.key} label={tech.label} onClick={() => handleOptimize(tech.key)} loading={loading} />
                      ))}
                    </React.Fragment>
                  ))
                )}
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
