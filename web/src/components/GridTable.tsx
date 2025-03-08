import React from "react";
import { ApiResponse, Grid } from "../store/useGridStore";
import { IconButton, Button, Tooltip } from "@radix-ui/themes";
import { PlusIcon, MinusIcon, ResetIcon } from "@radix-ui/react-icons";

interface GridTableProps {
  grid: Grid;
  resetGrid: () => void;
  loading: boolean;
  toggleCellState: (rowIndex: number, columnIndex: number, event: React.MouseEvent) => void;
  result: ApiResponse | null;
  activateRow: (rowIndex: number) => void;
  deActivateRow: (rowIndex: number) => void;
}

/**
 * A simple wrapper component that adds a CSS class to shake the children when
 * the "shaking" prop is true.
 *
 * @param {boolean} shaking - Whether to shake the children
 * @param {React.ReactNode} children - The children to shake
 * @returns {React.ReactElement} A div with the children
 */
const Wrapper: React.FC<{ shaking: boolean; children: React.ReactNode }> = ({ shaking, children }) => {
  return shaking ? <div className="relative shake">{children}</div> : <div className="relative">{children}</div>;
};

/**
 * A table component that displays a grid of cells, where each cell can be in
 * one of three states: normal, active, or supercharged. The component also
 * renders a set of buttons to activate or deactivate entire rows at once.
 *
 * @param {Grid} grid - The grid to display
 * @param {boolean} loading - Whether the component is currently loading
 * @param {function} toggleCellState - A function to toggle the state of a cell
 * @param {function} activateRow - A function to activate an entire row
 * @param {function} deActivateRow - A function to deactivate an entire row
 * @param {ApiResponse | null} result - The result of an optimization calculation,
 *   or null if no calculation has been done.
 * @param {function} resetGrid - A function to reset the grid
 */
const GridTable: React.FC<GridTableProps> = ({ grid, loading, toggleCellState, activateRow, deActivateRow, result, resetGrid }) => {
  const [shaking, setShaking] = React.useState(false);

  /**
   * Handles the click event for a cell in the grid. Toggles the state of the cell
   * between active and supercharged based on user interaction. If the cell is to
   * be supercharged and the maximum allowed supercharged cells are already
   * active, triggers a shaking animation to indicate the action is not allowed.
   *
   * @param {number} rowIndex - The index of the row containing the cell.
   * @param {number} columnIndex - The index of the column containing the cell.
   * @param {React.MouseEvent} event - The click event object.
   */
  const handleCellClick = (rowIndex: number, columnIndex: number, event: React.MouseEvent) => {
    if (!event.ctrlKey) {
      const totalSupercharged = grid.cells.flat().filter(cell => cell.supercharged).length;
      const currentCellSupercharged = grid.cells[rowIndex][columnIndex]?.supercharged;

      if (totalSupercharged >= 4 && !currentCellSupercharged) {
        setShaking(true);
        setTimeout(() => setShaking(false), 500);
        return;
      }
    }
    toggleCellState(rowIndex, columnIndex, event);
  };

  const hasModulesInGrid = grid.cells.flat().some((cell) => cell.module !== null);

  return (
    <Wrapper shaking={shaking}>
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-opacity-50 rounded-lg">
          <div className="w-16 h-16 border-8 rounded-full border-t-cyan-500 border-slate-500 animate-spin"></div>
        </div>
      )}
      <table className={`border-separate border-spacing-2 rounded-lg ${loading ? "opacity-50" : ""}`}>
        <tbody>
          {grid.cells.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, columnIndex) => (
                <td
                  key={columnIndex}
                  onClick={(event) => handleCellClick(rowIndex, columnIndex, event)}
                  className={`cursor-pointer shadow-md border-2 p-2 rounded-lg transition-all hover:bg-opacity-50 hover:bg-cyan-700
                      ${cell.supercharged ? "border-yellow-500" : "border-cyan-500"}
                      ${cell.active ? "border-cyan-500" : "border-cyan-700"}`}
                  style={{
                    backgroundImage: cell.image ? `url(${cell.image})` : "none",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    width: "72px",
                    height: "72px",
                  }}
                />
              ))}

              {/* First IconButton - shows on first inactive row */}
              {row.every((cell) => !cell.active) && rowIndex === grid.cells.findIndex((r) => r.every((cell) => !cell.active)) && (
                <td className="align-middle">
                  <Tooltip content="Activate Row">
                    <IconButton variant="soft" className="mx-auto" onClick={() => activateRow(rowIndex)} disabled={hasModulesInGrid}>
                      <PlusIcon />
                    </IconButton>
                  </Tooltip>
                </td>
              )}

              {/* MinusIcon - shows only on the last row with active cells */}
              {rowIndex >= grid.cells.length - 3 &&
                row.some((cell) => cell.active) &&
                rowIndex === grid.cells.map((r) => r.some((cell) => cell.active)).lastIndexOf(true) && (
                  <td className="align-middle">
                    <Tooltip content="Deactivate Row">
                      <IconButton variant="soft" className="mx-auto" onClick={() => deActivateRow(rowIndex)} disabled={hasModulesInGrid}>
                        <MinusIcon />
                      </IconButton>
                    </Tooltip>
                  </td>
                )}
            </tr>
          ))}
          <tr>
            <td colSpan={8}>
              <ul className="mt-2 list-disc list-inside">
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
            </td>
            <td colSpan={2} className="align-top">
              <div className="flex justify-end mt-2">
                <Button variant="solid" onClick={() => resetGrid()}>
                  <ResetIcon />
                  Reset Grid
                </Button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      {result && <p className="text-white">Max Bonus: {result.max_bonus.toFixed(2)}</p>}
    </Wrapper>
  );
};

export default GridTable;