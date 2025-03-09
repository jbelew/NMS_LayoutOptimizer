import { UpdateIcon, ResetIcon, DoubleArrowLeftIcon } from "@radix-ui/react-icons";
import { Heading, IconButton, Flex, Box, Text, Separator } from "@radix-ui/themes";

import React from "react";
import GridTable from "./components/GridTable";
import { useGridStore } from "./store/useGridStore";
import { useState, useEffect } from "react";

const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState, activateRow, deActivateRow, resetGrid } = useGridStore();
  const [techTree, setTechTree] = useState<{ [key: string]: { label: string; key: string }[] } | null>(null);

  useEffect(() => {
    const fetchTechTree = async () => {
      try {
        const response = await fetch("http://localhost:5000/tech_tree/Exotic");
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
    <Flex className="justify-center p-0 md:pt-8 md:items-top md:p-4">
      {/* Container Box with content-driven height, Tint + Blur */}
      <Box
        className="relative w-full max-w-screen-xl p-2 mx-auto overflow-hidden rounded-none shadow-lg md:rounded-xl md:border-1 md:shadow-none backdrop-blur-lg"
        style={{ borderColor: "var(--blue-1)" }}
      >
        {/* Lighten the background with a transparent white overlay */}
        <Box className="absolute inset-0 z-0 bg-white rounded-none opacity-10"></Box>

        {/* Header */}
        <Box asChild className="p-4 text-custom-cyan-light">
          <header>
            <Heading as="h1" style={{ color: "var(--gray-12)" }}>
              No Man's Sky Starship Optimizer v0.3
            </Heading>
          </header>
        </Box>

        <Flex className="flex-col md:flex-row bg-custom-cyan-dark">
          {/* Main Content */}
          <Box className="p-2 md:flex-shrink-0">
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

          {/* Sidebar - 1/4 width */}
          <Box className="z-10 w-full p-2 text-white md:flex-shrink-0 md:flex-grow-0 md:w-1/4 md:mr-4">
            {techTree &&
              Object.entries(techTree).map(([type, technologies]) => (
                <React.Fragment key={type}>
                  <h2 className="text-2xl" style={{ color: "var(--gray-12)" }}>
                    {type.toUpperCase()}
                  </h2>
                  <Separator orientation="horizontal" size="4" className="mb-4" />
                  {technologies.map((tech) => (
                    <OptimizationButton key={tech.key} label={tech.label} onClick={() => handleOptimize(tech.key)} loading={loading} tech={tech.key} />
                  ))}
                </React.Fragment>
              ))}
          </Box>
        </Flex>
      </Box>
    </Flex>
  );
};

const OptimizationButton: React.FC<{
  label: string;
  onClick: () => void;
  loading: boolean;
  tech: string;
}> = ({ label, onClick, loading, tech }) => {
  const hasTechInGrid = useGridStore((state) => state.hasTechInGrid(tech));
  const handleResetGridTech = useGridStore((state) => state.resetGridTech);

  return (
    <Flex className="items-center gap-2 mt-2 mb-2">
      <IconButton onClick={onClick} disabled={loading} variant="soft">
        {hasTechInGrid ? <UpdateIcon /> : <DoubleArrowLeftIcon />}
      </IconButton>
      <IconButton onClick={() => handleResetGridTech(tech)} disabled={!hasTechInGrid || loading} variant="soft">
        <ResetIcon />
      </IconButton>
      <Text style={{ color: "var(--gray-12)" }}>{label}</Text>
    </Flex>
  );
};
export default App;
