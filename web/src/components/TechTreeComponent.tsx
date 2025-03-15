// /home/jbelew/projects/nms/web/src/components/TechTreeComponent.tsx

import React from "react";
import { Separator } from "@radix-ui/themes";
import OptimizationButton from "./OptimizationButton";
import { useFetchTechTree } from "../hooks/useTechTree"; // Import the hook

// Define the TechTree interface
export interface TechTree {
  [key: string]: { label: string; key: string }[];
}

interface TechTreeComponentProps {
  handleOptimize: (tech: string) => void;
  solving: boolean; // Correctly named prop for grid optimization state
}

/**
 * A React component that renders a tech tree as a list of optimization buttons.
 * Each button, when clicked, will trigger the handleOptimize function with the
 * tech key as an argument.
 *
 * This component now fetches its own tech tree data using the useFetchTechTree hook.
 *
 * @param {TechTreeComponentProps} props Properties passed to the component.
 * @param {(tech: string) => void} props.handleOptimize The function to call when an optimization button is clicked.
 * @param {boolean} props.solving Whether the grid is solving. If true, the optimization buttons are disabled.
 * @returns {JSX.Element} The rendered component.
 */
const TechTreeComponent: React.FC<TechTreeComponentProps> = ({
  handleOptimize,
  solving, // Correctly named prop for grid optimization state
}: TechTreeComponentProps): JSX.Element => {
  const [techTree, techTreeLoading, error] = useFetchTechTree(); // Fetch the tech tree data here

  if (techTreeLoading) {
    return (
      <p className="sidebar__loading" style={{ color: "var(--gray-12)" }}>
        Loading tech tree...
      </p>
    );
  }

  if (error) {
    return (
      <p className="sidebar__error" style={{ color: "var(--gray-12)" }}>
        Error: {error}
      </p>
    );
  }

  if (!techTree) {
    return (
      <p className="sidebar__error" style={{ color: "var(--gray-12)" }}>
        Error: No Tech Tree
      </p>
    );
  }

  return (
    <>
      {Object.entries(techTree).map(([type, technologies]) => (
        <div key={type} className="mb-4 sidebar__section">
          <h2
            className="text-2xl sidebar__title"
            style={{ color: "var(--gray-12)" }}
          >
            {type.toUpperCase()}
          </h2>
          <Separator
            orientation="horizontal"
            size="4"
            className="mb-4 sidebar__separator"
          />
          {technologies.map((tech) => (
            <OptimizationButton
              key={tech.key}
              label={tech.label}
              onClick={() => handleOptimize(tech.key)}
              solving={solving} // Correct: Now passing the solving prop
              tech={tech.key}
            />
          ))}
        </div>
      ))}
    </>
  );
};

export default TechTreeComponent;
