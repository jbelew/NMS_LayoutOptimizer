// src/components/GridContainer/GridContainer.tsx
import React from "react";
import GridTable from "./../GridTable";
import TechTreeComponent from "../TechTree/TechTree";
import { useGridStore } from "../../store/useGridStore";
import { useOptimize } from "../../hooks/useOptimize";
import { Box, Flex, ScrollArea } from "@radix-ui/themes";
import { useBreakpoint } from "../../hooks/useBreakpoint";

interface GridContainerProps {}

const GridContainer: React.FC<GridContainerProps> = () => {
  const { solving, handleOptimize } = useOptimize();
  const {
    grid,
    result,
    toggleCellState,
    activateRow,
    deActivateRow,
    resetGrid,
  } = useGridStore();

  const [gridHeight, setGridHeight] = React.useState<number | null>(null);
  const isLarge = useBreakpoint("1024px");

  React.useEffect(() => {
    const updateGridHeight = () => {
      const gridElement = document.querySelector(".optimizer__grid");
      if (gridElement) {
        setGridHeight(gridElement.getBoundingClientRect().height);
      }
    };

    updateGridHeight();
    window.addEventListener("resize", updateGridHeight);
    return () => window.removeEventListener("resize", updateGridHeight);
  }, [grid]);

  return (
    <Flex className="flex-col items-start optimizer__layout lg:flex-row">
      <Box className="flex-grow w-auto pt-2 optimizer__grid lg:flex-shrink-0">
        <GridTable
          grid={grid}
          solving={solving}
          toggleCellState={toggleCellState}
          result={result}
          activateRow={activateRow}
          deActivateRow={deActivateRow}
          resetGrid={resetGrid}
        />
      </Box>

      {isLarge ? (
        <ScrollArea
          className="p-4 ml-4 rounded-xl optimizer__sidebar"
          style={{
            height: gridHeight !== null ? `${gridHeight}px` : "auto",
            backgroundColor: "var(--gray-a3)",
            width: "300px",
          }}
        >
          <TechTreeComponent
            handleOptimize={handleOptimize}
            solving={solving}
          />
        </ScrollArea>
      ) : (
        <Box className="z-10 items-start flex-grow-0 flex-shrink-0 w-full pt-4 sidebar">
          <TechTreeComponent
            handleOptimize={handleOptimize}
            solving={solving}
          />
        </Box>
      )}
    </Flex>
  );
};

export default GridContainer;
