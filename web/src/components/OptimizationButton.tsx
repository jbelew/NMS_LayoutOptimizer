import React from "react";

import { useGridStore } from "../store/useGridStore";
import { IconButton, Flex, Text } from "@radix-ui/themes";
import { UpdateIcon, ResetIcon, DoubleArrowLeftIcon } from "@radix-ui/react-icons";

interface OptimizationButtonProps {
  label: string;
  onClick: () => void;
  loading: boolean;
  tech: string;
}

/**
 * A button component designed to handle optimization actions for a specific tech.
 * The component displays different icons based on whether the tech is present in the grid.
 * It also provides functionality to reset the tech in the grid.
 *
 * @param {OptimizationButtonProps} props - The properties passed to the component.
 * @param {string} props.label - The label to display next to the button.
 * @param {() => void} props.onClick - The function to call when the button is clicked.
 * @param {boolean} props.loading - Whether the button should appear in a loading state.
 * @param {string} props.tech - The tech key associated with the button.
 * @returns {JSX.Element} The rendered button component.
 */
const OptimizationButton: React.FC<OptimizationButtonProps> = ({
  label,
  onClick,
  loading,
  tech,
}) => {
  const hasTechInGrid = useGridStore((state) => state.hasTechInGrid(tech));
  const handleResetGridTech = useGridStore((state) => state.resetGridTech);

  return (
    <Flex className="items-center gap-2 mt-2 mb-2">
      {/* Main icon button for triggering optimization */}
      <IconButton onClick={onClick} disabled={loading} variant="soft">
        {hasTechInGrid ? <UpdateIcon /> : <DoubleArrowLeftIcon />}
      </IconButton>
      {/* Button to reset the specific tech in the grid */}
      <IconButton
        onClick={() => handleResetGridTech(tech)}
        disabled={!hasTechInGrid || loading}
        variant="soft"
      >
        <ResetIcon />
      </IconButton>
      {/* Display the label next to the buttons */}
      <Text style={{ color: "var(--gray-12)" }}>{label}</Text>
    </Flex>
  );
};

export default OptimizationButton;
