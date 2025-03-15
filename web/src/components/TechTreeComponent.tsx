import { Separator } from "@radix-ui/themes";
import React, { Suspense, useMemo } from "react";
import { useFetchTechTreeSuspense } from "../hooks/useTechTree";
import OptimizationButton from "./OptimizationButton";

export interface TechTree {
  [key: string]: { label: string; key: string }[];
}

interface TechTreeComponentProps {
  handleOptimize: (tech: string) => void;
  solving: boolean;
}

/**
 * Renders the technology tree content with optimization buttons for each technology.
 * Uses memoization to optimize rendering performance and Suspense for data fetching.
 * 
 * @param {Object} props - The component properties.
 * @param {function} props.handleOptimize - Callback function to handle technology optimization.
 * @param {boolean} props.solving - Flag indicating whether optimization is in progress.
 * @returns {JSX.Element} The rendered technology tree with optimization buttons.
 */
const TechTreeContent: React.FC<TechTreeComponentProps> = React.memo(({ handleOptimize, solving }) => {
  const techTree = useFetchTechTreeSuspense(); // Fetch data using Suspense

  // Memoize the mapped elements to prevent unnecessary recalculations
  const renderedTechTree = useMemo(() => {
    return Object.entries(techTree).map(([type, technologies]) => (
      <div key={type} className="mb-4 sidebar__section">
        <h2 className="text-2xl sidebar__title" style={{ color: "var(--gray-12)" }}>
          {type.toUpperCase()}
        </h2>
        <Separator orientation="horizontal" size="4" className="mb-4 sidebar__separator" />
        {technologies.map((tech) => (
          <OptimizationButton key={tech.key} label={tech.label} onClick={() => handleOptimize(tech.key)} solving={solving} tech={tech.key} />
        ))}
      </div>
    ));
  }, [techTree, handleOptimize, solving]);

  return <>{renderedTechTree}</>;
});

/**
 * Renders the TechTreeComponent with a loading fallback using React Suspense.
 * Displays a loading message while the tech tree content is being fetched.
 * 
 * @param {TechTreeComponentProps} props - The component properties for tech tree optimization.
 * @returns {JSX.Element} A Suspense-wrapped component with tech tree content or loading state.
 */
const TechTreeComponent: React.FC<TechTreeComponentProps> = (props) => (
  <Suspense
    fallback={
      <p className="sidebar__loading" style={{ color: "var(--gray-12)" }}>
        Loading tech tree...
      </p>
    }
  >
    <TechTreeContent {...props} />
  </Suspense>
);

export default TechTreeComponent;
