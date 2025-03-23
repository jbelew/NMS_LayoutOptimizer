// src/App.tsx
import { Box, Flex, Heading, ScrollArea } from "@radix-ui/themes";
import React, { useEffect, useState } from "react";
import GridTable from "./components/GridTable";
import TechTreeComponent from "./components/TechTree"; // Import TechTreeComponent
import { useGridStore } from "./store/useGridStore";
import { useOptimize } from "./hooks/useOptimize"; // Import useOptimize

const useBreakpoint = (breakpoint: string) => {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(`(min-width: ${breakpoint})`);
    const handler = (event: MediaQueryListEvent) => setMatches(event.matches);

    setMatches(mediaQuery.matches);
    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, [breakpoint]);

  return matches;
};

const App: React.FC = () => {
  const { solving, handleOptimize } = useOptimize(); // Call useOptimize here
  const {
    grid,
    result,
    toggleCellState,
    activateRow,
    deActivateRow,
    resetGrid,
  } = useGridStore();

  const [gridHeight, setGridHeight] = useState<number | null>(null);
  const isLarge = useBreakpoint("1024px"); // lg breakpoint in Tailwind

  useEffect(() => {
    const updateGridHeight = () => {
      const gridElement = document.querySelector(".optimizer__grid");
      if (gridElement) {
        setGridHeight(gridElement.getBoundingClientRect().height);
      }
    };

    updateGridHeight(); // Initial calculation
    window.addEventListener("resize", updateGridHeight);
    return () => window.removeEventListener("resize", updateGridHeight);
  }, [grid]);

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
            No Man's Sky Starship Optimizer v0.7
          </Heading>
        </Box>

        {/* Main Layout */}
        <Flex className="flex-col items-start optimizer__layout lg:flex-row">
          {/* Main Content */}
          <Box className="flex-grow w-auto pt-2 optimizer__grid lg:flex-shrink-0">
            <GridTable
              // Pass the grid, solving state, and various functions to the GridTable component
              grid={grid}
              solving={solving} // Pass solving as a prop
              toggleCellState={toggleCellState}
              result={result}
              activateRow={activateRow}
              deActivateRow={deActivateRow}
              resetGrid={resetGrid}
            />
          </Box>

          {/* Sidebar */}

          {isLarge ? (
            <ScrollArea
              className="p-4 ml-4 rounded-xl optimizer__sidebar"
              style={{
                height: gridHeight !== null ? `${gridHeight}px` : "auto",
                backgroundColor: "var(--gray-a3)",
                width: "300px"
              }}
            >
              <TechTreeComponent
                // Pass the handleOptimize function and the solving state to the TechTreeComponent
                handleOptimize={handleOptimize} // Pass handleOptimize
                solving={solving} // Pass solving
              />
            </ScrollArea>
          ) : (
            <Box className="z-10 items-start flex-grow-0 flex-shrink-0 w-full pt-4 sidebar">
              <TechTreeComponent
                // Pass the handleOptimize function and the solving state to the TechTreeComponent
                handleOptimize={handleOptimize} // Pass handleOptimize
                solving={solving} // Pass solving
              />
            </Box>
          )}
        </Flex>
      </Box>
    </Flex>
  );
};

export default App;
