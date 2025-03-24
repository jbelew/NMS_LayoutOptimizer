// src/App.tsx
import { Box, Flex, Heading } from "@radix-ui/themes";
import React, { useEffect } from "react";
import GridContainer from "./components/GridContainer/GridContainer"; // Import GridContainer
import { useSSE } from "./hooks/useSSE";

const App: React.FC = () => {
  const { registerMessageHandler } = useSSE();

  useEffect(() => {
    const messageHandler = (message: string) => {
      console.log("App: Message received:", message);
    };
    registerMessageHandler(messageHandler);

    // Cleanup: remove the handler when the component unmounts
    return () => {
      // In a more complex scenario, you might need to remove the handler from the array.
      // For this simple example, it's sufficient to just not call it anymore.
    };
  }, [registerMessageHandler]);

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
            No Man's Sky Starship Optimizer v0.8
          </Heading>
        </Box>

        {/* Main Layout */}
        <GridContainer /> {/* Render GridContainer */}
      </Box>
    </Flex>
  );
};

export default App;
