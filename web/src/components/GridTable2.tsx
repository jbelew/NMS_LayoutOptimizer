// GridTable.tsx
import React from "react";
import { ApiResponse, Grid } from "../store/useGridStore";
import { Button } from "@radix-ui/themes";
import { ResetIcon } from "@radix-ui/react-icons";
import GridCell from "./GridCell";
import GridRowActions from "./GridRowActions";
import ShakingWrapper from "./GridShake";
import GridSpinner from "./GridSpinner";

interface GridTableProps {
  grid: Grid;
  resetGrid: () => void;
  solving: boolean;
  toggleCellState: (rowIndex: number, columnIndex: number, event: React.MouseEvent) => void;
  result: ApiResponse | null;
  activateRow: (rowIndex: number) => void;
  deActivateRow: (rowIndex: number) => void;
}

const GridTable: React.FC<GridTableProps> = ({ grid, solving, toggleCellState, activateRow, deActivateRow, result, resetGrid }) => {
  const [shaking, setShaking] = React.useState(false);

  const hasModulesInGrid = grid.cells.flat().some((cell) => cell.module !== null);

  return (
    <ShakingWrapper shaking={shaking}>
      <GridSpinner solving={solving} />
      <div className={`grid-container ${solving ? "opacity-50" : ""}`}>
        {grid.cells.map((row, rowIndex) => (
          <React.Fragment key={rowIndex}>
            {row.map((cell, columnIndex) => (
              <GridCell
                key={columnIndex}
                rowIndex={rowIndex}
                columnIndex={columnIndex}
                cell={{
                  label: cell.label,
                  supercharged: cell.supercharged,
                  active: cell.active,
                  image: cell.image || undefined,
                }}
                grid={grid}
                toggleCellState={toggleCellState}
                setShaking={setShaking}
              />
            ))}
            <GridRowActions
              rowIndex={rowIndex}
              activateRow={activateRow}
              deActivateRow={deActivateRow}
              hasModulesInGrid={hasModulesInGrid}
              isFirstInactiveRow={row.every((cell) => !cell.active) && rowIndex === grid.cells.findIndex((r) => r.every((cell) => !cell.active))}
              isLastActiveRow={
                rowIndex >= grid.cells.length - 3 &&
                row.some((cell) => cell.active) &&
                rowIndex === grid.cells.map((r) => r.some((cell) => cell.active)).lastIndexOf(true)
              }
            />
          </React.Fragment>
        ))}
        <div className="pt-2 grid-instructions">
          <ul className="list-disc list-inside " style={{ color: "var(--gray-12)" }}>
            <li>
              <strong>Click</strong> a cell to toggle its <em>Supercharged</em> state. No more than 4.
            </li>
            <li>
              <strong>Ctrl-Click</strong> on a cell to enable or disable it individually.
            </li>
            <li>
              Use the buttons on the right to <strong>Activate</strong> or <strong>Deactivate</strong> entire rows at once.
            </li>
          </ul>
        </div>
        <div className="grid-reset-button">
          <div className="flex justify-end pt-2">
            <Button variant="solid" onClick={resetGrid}>
              <ResetIcon />
              Reset Grid
            </Button>
          </div>
        </div>
        <div className="grid-result">
          {result && <p className="text-white">Max Bonus: {result.max_bonus.toFixed(2)}</p>}
        </div>
      </div>
    </ShakingWrapper>
  );
};

export default GridTable;
