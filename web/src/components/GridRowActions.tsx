// RowControlButton.tsx
import React from "react";
import { IconButton, Tooltip } from "@radix-ui/themes";
import { PlusIcon, MinusIcon } from "@radix-ui/react-icons";

interface RowControlButtonProps {
  rowIndex: number;
  activateRow: (rowIndex: number) => void;
  deActivateRow: (rowIndex: number) => void;
  hasModulesInGrid: boolean;
  isFirstInactiveRow: boolean;
  isLastActiveRow: boolean;
}

const RowControlButton: React.FC<RowControlButtonProps> = ({
  rowIndex,
  activateRow,
  deActivateRow,
  hasModulesInGrid,
  isFirstInactiveRow,
  isLastActiveRow,
}) => {
  return (
    <>
      {isFirstInactiveRow && (
        <td className="align-middle">
          <Tooltip content="Activate Row">
            <IconButton variant="soft" className="mx-auto" onClick={() => activateRow(rowIndex)} disabled={hasModulesInGrid}>
              <PlusIcon />
            </IconButton>
          </Tooltip>
        </td>
      )}

      {isLastActiveRow && (
        <td className="align-middle">
          <Tooltip content="Deactivate Row">
            <IconButton variant="soft" className="mx-auto" onClick={() => deActivateRow(rowIndex)} disabled={hasModulesInGrid}>
              <MinusIcon />
            </IconButton>
          </Tooltip>
        </td>
      )}
    </>
  );
};

export default RowControlButton;
