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

/**
 * A button component that allows the user to activate or deactivate a row in
 * the grid. The button is only rendered if the row is either the first inactive
 * row or the last active row. The button is also disabled if there are any
 * modules in the grid.
 *
 * @param {number} rowIndex - The index of the row containing the button.
 * @param {function} activateRow - A function to activate an entire row.
 * @param {function} deActivateRow - A function to deactivate an entire row.
 * @param {boolean} hasModulesInGrid - Whether there are any modules in the grid.
 * @param {boolean} isFirstInactiveRow - Whether the row is the first inactive row.
 * @param {boolean} isLastActiveRow - Whether the row is the last active row.
 */
const RowControlButton: React.FC<RowControlButtonProps> = ({
  rowIndex,
  activateRow,
  deActivateRow,
  hasModulesInGrid,
  isFirstInactiveRow,
  isLastActiveRow,
}) => {
  return (
    <div style={{ gridColumn: 11, gridRow: rowIndex + 1 }} className="flex items-center justify-center">
      {isFirstInactiveRow && (
        <div className="align-middle">
          <Tooltip content="Activate Row">
            <IconButton
              variant="soft"
              className="mx-auto"
              onClick={() => activateRow(rowIndex)}
              disabled={hasModulesInGrid}
            >
              <PlusIcon />
            </IconButton>
          </Tooltip>
        </div>
      )}

      {isLastActiveRow && (
        <div className="align-middle">
          <Tooltip content="Deactivate Row">
            <IconButton
              variant="soft"
              className="mx-auto"
              onClick={() => deActivateRow(rowIndex)}
              disabled={hasModulesInGrid}
            >
              <MinusIcon />
            </IconButton>
          </Tooltip>
        </div>
      )}
    </div>
  );
};

export default RowControlButton;
