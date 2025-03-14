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
    <Flex className="items-start justify-center optimizer lg:pt-16 lg:items-top lg:p-4">
      {/* Container Box */}
      <Box
        className="optimizer__container relative min-w-[min-content] max-w-fit mx-auto overflow-hidden p-2 rounded-none shadow-lg lg:rounded-xl lg:border-1 lg:shadow-xl backdrop-blur-lg"
        style={{ borderColor: "var(--blue-1)" }}
      >
        {/* Background Overlay */}
        <Box className="absolute inset-0 z-0 bg-white rounded-none optimizer__overlay opacity-10"></Box>

        {/* Header */}
        <Box asChild className="p-4 optimizer__header text-custom-cyan-light">
          <Heading as="h1" className="optimizer__title" style={{ color: "var(--gray-12)" }}>
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
          <Box className="sidebar z-10 p-2 text-white flex-grow-0 flex-shrink-0 w-full lg:w-[300px]">
            {techTree ? (
              Object.entries(techTree).map(([type, technologies]) => (
                <div key={type} className="mb-4 sidebar__section">
                  <h2 className="text-2xl sidebar__title" style={{ color: "var(--gray-12)" }}>
                    {type.toUpperCase()}
                  </h2>
                  <Separator orientation="horizontal" size="4" className="mb-4 sidebar__separator" />
                  {technologies.map((tech) => (
                    <OptimizationButton
                      key={tech.key}
                      label={tech.label}
                      onClick={() => handleOptimize(tech.key)}
                      loading={loading}
                      tech={tech.key}
                      className="sidebar__button"
                    />
                  ))}
                </div>
              ))
            ) : (
              <p className="sidebar__loading" style={{ color: "var(--gray-12)" }}>
                Loading tech tree...
              </p>
            )}
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
