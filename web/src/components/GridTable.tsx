import React from "react";
import { ApiResponse, Grid } from "../store/useGridStore";
import { IconButton } from "@radix-ui/themes";
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

const GridTable: React.FC<GridTableProps> = ({ grid, loading, toggleCellState, activateRow, deActivateRow, result, resetGrid }) => {
  return (
    <div className="relative">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-opacity-50 rounded-lg">
          <div className="w-10 h-10 border-4 rounded-full border-t-cyan-500 border-slate-500 animate-spin"></div>
        </div>
      )}
      <table className={`border-separate border-spacing-2 rounded-lg ${loading ? "opacity-50" : ""}`}>
        <tbody>
          {grid.cells.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, columnIndex) => (
                <td
                  key={columnIndex}
                  onClick={(event) => toggleCellState(rowIndex, columnIndex, event)}
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
                  <IconButton variant="soft" className="mx-auto" onClick={() => activateRow(rowIndex)}>
                    <PlusIcon />
                  </IconButton>
                </td>
              )}

              {/* MinusIcon - shows only on the last row with active cells */}
              {rowIndex >= grid.cells.length - 3 &&
                row.some((cell) => cell.active) &&
                rowIndex === grid.cells.map((r) => r.some((cell) => cell.active)).lastIndexOf(true) && (
                  <td className="align-middle">
                    <IconButton variant="soft" className="mx-auto" onClick={() => deActivateRow(rowIndex)}>
                      <MinusIcon />
                    </IconButton>
                  </td>
                )}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex justify-end mt-4">
        <IconButton variant="soft" color="gray" onClick={() => resetGrid()}>
          <ResetIcon />
          <span className="ml-2">Reset Grid</span>
        </IconButton>
      </div>

      {result && <p className="text-white">Max Bonus: {result.max_bonus.toFixed(2)}</p>}
    </div>
  );
};
export default GridTable;
