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
      <IconButton onClick={onClick} disabled={loading} variant="soft">
        {hasTechInGrid ? <UpdateIcon /> : <DoubleArrowLeftIcon />}
      </IconButton>
      <IconButton
        onClick={() => handleResetGridTech(tech)}
        disabled={!hasTechInGrid || loading}
        variant="soft"
      >
        <ResetIcon />
      </IconButton>
      <Text style={{ color: "var(--gray-12)" }}>{label}</Text>
    </Flex>
  );
};

export default OptimizationButton;
