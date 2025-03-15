import { Heading, Flex, Box } from "@radix-ui/themes";

import React from "react";
import GridTable from "./components/GridTable";
import TechTreeComponent from "./components/TechTree";
import { useGridStore } from "./store/useGridStore";
import { useFetchTechTree } from "./hooks/useTechTree";

const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState, activateRow, deActivateRow, resetGrid } = useGridStore();
  const { techTreeState: techTree } = useFetchTechTree();

  return (
    <Flex className="items-start justify-center optimizer lg:pt-16 lg:items-top lg:p-4">
      {/* Container Box */}
      <Box
        className="optimizer__container relative min-w-[min-content] max-w-fit mx-auto overflow-hidden p-2 rounded-none shadow-lg lg:rounded-xl lg:border-1 lg:shadow-xl backdrop-blur-lg"
        style={{ borderColor: "var(--blue-1)" }}
      >
        {/* Background Overlay */}
        <Box className="absolute inset-0 z-0 bg-white rounded-none optimizer__overlay opacity-10"></Box>

        {/* Header */}
        <Box asChild className="p-4 pb-2 optimizer__header text-custom-cyan-light">
          <Heading as="h1" size="7" className="shadow-md optimizer__title" style={{ color: "var(--gray-12)" }}>
            No Man's Sky Starship Optimizer v0.3
          </Heading>

        </Box>

        {/* Main Layout */}
        <Flex className="flex-col items-start optimizer__layout lg:flex-row">
          {/* Main Content */}
          <Box className="flex-grow p-2 optimizer__grid lg:flex-shrink-0">
            <GridTable
              grid={grid}
              loading={loading}
              toggleCellState={toggleCellState}
              result={result}
              activateRow={activateRow}
              deActivateRow={deActivateRow}
              resetGrid={resetGrid}
            />
          </Box>

          {/* Sidebar */}
          <Box className="sidebar z-10 p-2  flex-grow-0 flex-shrink-0 w-full lg:w-[300px]" style={{ color: "var(--gray-12)" }}>
            <TechTreeComponent techTree={techTree} handleOptimize={handleOptimize} loading={loading} />
          </Box>
        </Flex>
      </Box>
    </Flex>
  );
};
export default App;
