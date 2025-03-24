// src/App.tsx
import { Box, Flex, Heading } from "@radix-ui/themes";
import React from "react";
import GridContainer from "./components/GridContainer/GridContainer";
import { useOptimize } from "./hooks/useOptimize";

const App: React.FC = () => {
  const { setMessagesReceived } = useOptimize();

  return (
    <Flex className="items-start justify-center optimizer lg:pt-16 lg:items-top lg:p-4">
      <Box
        className="optimizer__container relative min-w-[min-content] max-w-fit mx-auto overflow-hidden p-8 rounded-none shadow-lg lg:rounded-xl lg:border-1 lg:shadow-xl backdrop-blur-lg"
        style={{ borderColor: "var(--blue-1)" }}
      >
        <Box className="absolute inset-0 z-0 bg-white rounded-none optimizer__overlay opacity-10"></Box>
        <Box asChild className="pb-4 optimizer__header text-custom-cyan-light">
          <Heading as="h1" size="7" className="font-black shadow-md optimizer__title" style={{ color: "var(--gray-12)" }}>
            No Man's Sky Starship Optimizer v0.8
          </Heading>
        </Box>
        <GridContainer />
      </Box>
    </Flex>
  );
};

export default App;
