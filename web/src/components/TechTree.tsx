import React from "react";

import { Separator } from "@radix-ui/themes";
import OptimizationButton from "./OptimizationButton";

// Define the TechTree interface
export interface TechTree {
  [key: string]: { label: string; key: string }[];
}

interface TechTreeComponentProps {
  techTree: TechTree | null;
  handleOptimize: (tech: string) => void;
  loading: boolean;
}

/**
 * A React component that renders a tech tree as a list of optimization buttons.
 * Each button, when clicked, will trigger the handleOptimize function with the
 * tech key as an argument.
 *
 * @param {TechTreeComponentProps} props Properties passed to the component.
 * @param {TechTree | null} props.techTree The tech tree to render. If null, a loading message is shown.
 * @param {(tech: string) => void} props.handleOptimize The function to call when an optimization button is clicked.
 * @param {boolean} props.loading Whether the component is loading. If true, the optimization buttons are disabled.
 * @returns {JSX.Element} The rendered component.
 */
const TechTreeComponent: React.FC<TechTreeComponentProps> = ({ techTree, handleOptimize, loading }: TechTreeComponentProps): JSX.Element => {
  return (
    <>
      {techTree ? (
        Object.entries(techTree).map(([type, technologies]) => (
          <div key={type} className="mb-4 sidebar__section">
            <h2 className="text-2xl sidebar__title" style={{ color: "var(--gray-12)" }}>
              {type.toUpperCase()}
            </h2>
            <Separator orientation="horizontal" size="4" className="mb-4 sidebar__separator" />
            {technologies.map((tech) => (
              <OptimizationButton key={tech.key} label={tech.label} onClick={() => handleOptimize(tech.key)} loading={loading} tech={tech.key} />
            ))}
          </div>
        ))
      ) : (
        <p className="sidebar__loading" style={{ color: "var(--gray-12)" }}>
          Loading tech tree...
        </p>
      )}
    </>
  );
};

export default TechTreeComponent;
