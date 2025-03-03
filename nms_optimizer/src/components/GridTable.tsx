import React from "react";
import { Grid, ApiResponse } from "../store/useGridStore"; // Import the types from your store

interface GridTableProps {
  grid: Grid;
  loading: boolean;
  toggleCellState: (rowIndex: number, columnIndex: number, event: React.MouseEvent) => void;
  result: ApiResponse | null;
}

const GridTable: React.FC<GridTableProps> = ({ grid, loading, toggleCellState, result }) => {
  return (
    <div className="relative">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-50 rounded-lg">
          <div className="w-10 h-10 border-4 border-blue-500 rounded-full animate-spin border-t-transparent"></div>
        </div>
      )}
      <table className={`bg-white border-separate border-spacing-2 rounded-lg ${loading ? "opacity-50" : ""}`}>
        <tbody>
          {grid.cells.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, columnIndex) => (
                <td
                  key={columnIndex}
                  onClick={(event) => toggleCellState(rowIndex, columnIndex, event)}
                  className={`cursor-pointer shadow-md border-2 px-2 py-2 rounded-lg transition-colors
                    ${cell.supercharged ? "border-yellow-500" : "border-blue-500"}
                    ${cell.active ? "border-blue-500" : "border-gray-300"}`}
                  style={{
                    backgroundImage: cell.image ? `url(${cell.image})` : "none",
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    width: "72px",
                    height: "72px",
                  }}
                >
                  <span className="text-gray-50">{parseFloat(cell.total.toFixed(2))}</span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {result && (
        <div className="mt-4">
          <p>Max Bonus: {result.max_bonus.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
};

export default GridTable;
