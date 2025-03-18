// gridCell.tsx
import React from "react";
import { Tooltip } from "@radix-ui/themes";
import { Grid } from "../../store/useGridStore";

interface gridCellProps {
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

/**
 * A single cell in the Grid component.
 *
 * @param {number} rowIndex The index of the row containing the cell
 * @param {number} columnIndex The index of the column containing the cell
 * @param {object} cell The cell data
 * @param {function} toggleCellState A function to toggle the state of the cell
 * @param {Grid} grid The grid data
 * @param {function} setShaking A function to set the shaking state of the cell
 */
const gridCell: React.FC<gridCellProps> = ({ rowIndex, columnIndex, cell, toggleCellState, grid, setShaking }) => {
  /**
   * Handles a click on the cell.
   * @param event The click event
   */
  const handleClick = (event: React.MouseEvent) => {
    // Prevent the default behavior of toggling the cell if the Ctrl key is
    // pressed and the cell is not supercharged
    if (!event.ctrlKey) {
      const totalSupercharged = grid.cells.flat().filter((cell) => cell.supercharged).length;
      const currentCellSupercharged = grid.cells[rowIndex][columnIndex]?.supercharged;

      if (totalSupercharged >= 4 && !currentCellSupercharged) {
        // If the cell is not supercharged and the total supercharged cells is 4,
        // set the shaking state to true and reset it after 500ms
        setShaking(true);
        setTimeout(() => setShaking(false), 500);
        return;
      }
    }
    // Call the toggleCellState function with the row and column index and the
    // event object
    toggleCellState(rowIndex, columnIndex, event);
  };

  /**
   * Renders the content of the cell.
   * @returns The rendered cell content
   */
  const renderCellContent = () => {
    /**
     * If the cell has a label, wrap it in a Tooltip.
     * This is useful for displaying the name of the module in the tooltip.
     */
    if (cell.label) {
      return (
        <Tooltip content={cell.label}>
          {/**
           * The outermost element of the cell.
           * This element is responsible for displaying the cell's background image.
           * The backgroundImage property is used to set the background image of the
           * element based on the cell's image property.
           * The backgroundSize and backgroundPosition properties are used to ensure
           * that the background image is centered and covers the entire element.
           */}
          <div
            role="gridCell"
            onClick={handleClick}
            className={`gridCell gridCell--interactive shadow-md border-2 rounded-lg transition-all
              ${cell.supercharged ? "gridCell--supercharged" : cell.active ? "gridCell--active" : "gridCell--inactive"}
              `}
            style={{
              backgroundImage: cell?.image ? `url(/src/assets/img/${cell.image})` : "none"
            }}
          ></div>
        </Tooltip>
      );
    }

    // If no label, render the cell without Tooltip
    return (
      <div role="gridCell"
        onClick={handleClick}
        className={`gridCell gridCell--interactive shadow-md border-2 rounded-lg transition-all
          ${cell.supercharged ? "gridCell--supercharged" : cell.active ? "gridCell--active" : "gridCell--inactive"}
          `}
        style={{
          backgroundImage: cell.image ? `url(/src/assets/img/${cell.image})` : "none"
        }}
      ></div>
    );
  };

  // Render the cell
  return <div style={{ gridColumn: columnIndex + 1, gridRow: rowIndex + 1 }}>{renderCellContent()}</div>;
};

export default gridCell;
