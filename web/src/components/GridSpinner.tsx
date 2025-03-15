// GridSpinner.tsx
import React from "react";

interface GridSpinnerProps {
  solving: boolean;
}

const GridSpinner: React.FC<GridSpinnerProps> = ({ solving }) => {
  return (
    solving && (
      <div className="absolute inset-0 flex items-center justify-center bg-opacity-50 rounded-lg">
        <div className="w-16 h-16 border-8 rounded-full border-t-cyan-500 border-slate-500 animate-spin"></div>
      </div>
    )
  );
};

export default GridSpinner;