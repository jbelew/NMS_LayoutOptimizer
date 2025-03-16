// GridSpinner.tsx
import React from "react";
import { Text } from "@radix-ui/themes";

interface GridSpinnerProps {
  solving: boolean;
  message?: string; // Optional message prop
}

/**
 * GridSpinner component that displays a loading spinner overlay when solving is true.
 *
 * @param {GridSpinnerProps} props - The properties passed to the component.
 * @param {boolean} props.solving - Determines whether the spinner is visible.
 * @param {string} [props.message] - An optional message to display alongside the spinner.
 * @returns {JSX.Element | null} The rendered spinner element or null.
 */
const GridSpinner: React.FC<GridSpinnerProps> = ({ solving, message }) => {
  return (
    solving && (
      <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-opacity-50 rounded-lg">
        <div className="w-16 h-16 border-8 rounded-full border-t-cyan-500 border-slate-600 animate-spin"></div>
        {message && (
          <Text className="pt-4">{message}</Text>
        )}
      </div>
    )
  );
};

export default GridSpinner;
