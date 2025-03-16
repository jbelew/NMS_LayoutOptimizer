// GridSpinner.tsx
import React from "react";

interface GridSpinnerProps {
  solving: boolean;
}

/**
 * GridSpinner component that displays a loading spinner overlay when solving is true.
 *
 * @param {GridSpinnerProps} props - The properties passed to the component.
 * @param {boolean} props.solving - Determines whether the spinner is visible.
 * @returns {JSX.Element | null} The rendered spinner element or null.
 */
const GridSpinner: React.FC<GridSpinnerProps> = ({ solving }) => {
  return (
    solving && (
      <div className="absolute inset-0 flex items-center justify-center bg-opacity-50 rounded-lg">
        <div className="w-16 h-16 border-8 rounded-full border-t-cyan-500 border-slate-600 animate-spin"></div>
      </div>
    )
  );
};

export default GridSpinner;