import { Box, Flex, Heading } from "@radix-ui/themes";
import React from "react";
import GridTable from "./components/GridTable";
import TechTreeComponent from "./components/TechTree"; // Import TechTreeComponent
import { useGridStore } from "./store/useGridStore";

/**
 * The main app component, which is responsible for rendering the entire user interface.
 */
const App: React.FC = () => {
  const {
    // The grid of cells to display
    grid,
    // The result of the optimization calculation
    result,
    // A boolean indicating whether or not the app is currently solving
    solving,
    // A function that starts the optimization calculation
    handleOptimize,
    // A function that toggles the state of a cell in the grid
    toggleCellState,
    // A function that activates an entire row in the grid
    activateRow,
    // A function that deactivates an entire row in the grid
    deActivateRow,
    // A function that resets the grid to its initial state
    resetGrid
  } = useGridStore();

  return (
    // The main container of the app
    <Flex className="items-start justify-center optimizer lg:pt-16 lg:items-top lg:p-4">
      {/* Container Box */}
      <Box
        className="optimizer__container relative min-w-[min-content] max-w-fit mx-auto overflow-hidden p-8 rounded-none shadow-lg lg:rounded-xl lg:border-1 lg:shadow-xl backdrop-blur-lg"
        style={{ borderColor: "var(--blue-1)" }}
      >
        {/* Background Overlay */}
        <Box className="absolute inset-0 z-0 bg-white rounded-none optimizer__overlay opacity-10"></Box>

        {/* Header */}
        <Box asChild className="pb-4 optimizer__header text-custom-cyan-light">
          <Heading as="h1" size="7" className="font-black shadow-md optimizer__title" style={{ color: "var(--gray-12)" }}>
            No Man's Sky Starship Optimizer v0.4
          </Heading>
        </Box>

        {/* Main Layout */}
        <Flex className="flex-col items-start optimizer__layout lg:flex-row">
          {/* Main Content */}
          <Box className="flex-grow pt-2 optimizer__grid lg:flex-shrink-0">
            <GridTable
              // Pass the grid, solving state, and various functions to the GridTable component
              grid={grid}
              solving={solving}
              toggleCellState={toggleCellState}
              result={result}
              activateRow={activateRow}
              deActivateRow={deActivateRow}
              resetGrid={resetGrid}
            />
          </Box>

          {/* Sidebar */}
          <Box className="sidebar z-10 flex-grow-0 lg:pl-8 lg:pt-0 pt-4 flex-shrink-0 w-full lg:w-[300px] items-start" style={{ color: "var(--gray-12)" }}>
            <TechTreeComponent
              // Pass the handleOptimize function and the solving state to the TechTreeComponent
              handleOptimize={handleOptimize}
              solving={solving}
            />
          </Box>
        </Flex>
      </Box>
    </Flex>
  );
};

export default App;
