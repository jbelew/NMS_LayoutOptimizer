// GridCell.tsx
import React from "react";
import { Tooltip } from "@radix-ui/themes";
import { Grid } from "../store/useGridStore";

interface GridCellProps {
  rowIndex: number;
  columnIndex: number;
  cell: {
    label?: string;
    supercharged?: boolean;
    active?: boolean;
    image?: string;
  };
  grid: Grid;
  toggleCellState: (rowIndex: number, columnIndex: number, event: React.MouseEvent) => void;
  setShaking: React.Dispatch<React.SetStateAction<boolean>>;
}

const GridCell: React.FC<GridCellProps> = ({ rowIndex, columnIndex, cell, toggleCellState, grid, setShaking }) => {
  const handleClick = (event: React.MouseEvent) => {
    if (!event.ctrlKey) {
      const totalSupercharged = grid.cells.flat().filter((cell) => cell.supercharged).length;
      const currentCellSupercharged = grid.cells[rowIndex][columnIndex]?.supercharged;

      if (totalSupercharged >= 4 && !currentCellSupercharged) {
        setShaking(true);
        setTimeout(() => setShaking(false), 500);
        return;
      }
    }
    toggleCellState(rowIndex, columnIndex, event);
  };

  const renderCellContent = () => {
    // If the cell has a label, wrap it in a Tooltip
    if (cell.label) {
      return (
        <Tooltip content={cell.label}>
          <div
            onClick={handleClick}
            className={`cursor-pointer shadow-md border-2 p-2 rounded-lg transition-all 
              ${cell.supercharged ? "grid-supercharged" : cell.active ? "grid-active" : "grid-inactive"}
              grid-hover`}
            style={{
              backgroundImage: cell?.image ? `url(/src/assets/img/${cell.image})` : "none",
              backgroundSize: "cover",
              backgroundPosition: "center",
              width: "64px",
              height: "64px",
            }}
          ></div>
        </Tooltip>
      );
    }

    // If no label, render the cell without Tooltip
    return (
      <div
        onClick={handleClick}
        className={`cursor-pointer shadow-md border-2 p-2 rounded-lg transition-all 
          ${cell.supercharged ? "grid-supercharged" : "grid-active"}
          ${cell.active ? "grid-active" : "grid-inactive"}
          grid-hover`}
        style={{
          backgroundImage: cell.image ? `url(/src/assets/img/${cell.image})` : "none",
          backgroundSize: "cover",
          backgroundPosition: "center",
          width: "64px",
          height: "64px",
        }}
      ></div>
    );
  };

  return <div style={{ gridColumn: columnIndex + 1, gridRow: rowIndex + 1 }}>{renderCellContent()}</div>;
};

export default GridCell;
