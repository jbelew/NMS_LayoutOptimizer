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
 * Renders a section of the tech tree with a title and optimization buttons.
 *
 * @param {Object} props - Component properties.
 * @param {string} props.type - The tech category name.
 * @param {Array} props.technologies - List of technologies in this section.
 * @param {function} props.handleOptimize - Callback for optimization.
 * @param {boolean} props.solving - Whether optimization is in progress.
 * @returns {JSX.Element} Rendered section of the tech tree.
 */
const TechTreeSection: React.FC<{
  type: string;
  technologies: { label: string; key: string }[];
  handleOptimize: (tech: string) => void;
  solving: boolean;
}> = ({ type, technologies, handleOptimize, solving }) => (
  <div className="mb-4 sidebar__section">
    <h2 className="text-2xl sidebar__title" style={{ color: "var(--gray-12)" }}>
      {type.toUpperCase()}
    </h2>
    <Separator orientation="horizontal" size="4" className="mb-4 sidebar__separator" />
    {technologies.map((tech) => (
      <OptimizationButton key={tech.key} label={tech.label} onClick={() => handleOptimize(tech.key)} solving={solving} tech={tech.key} />
    ))}
  </div>
);

/**
 * Provides tech tree data via Suspense and renders it using TechTreeSection.
 *
 * @param {TechTreeComponentProps} props - Component properties.
 * @returns {JSX.Element} The rendered technology tree.
 */
const TechTreeContent: React.FC<TechTreeComponentProps> = React.memo(({ handleOptimize, solving }) => {
  const techTree = useFetchTechTreeSuspense(); // Fetch data using Suspense

  const renderedTechTree = useMemo(
    () =>
      Object.entries(techTree).map(([type, technologies]) => (
        <TechTreeSection key={type} type={type} technologies={technologies} handleOptimize={handleOptimize} solving={solving} />
      )),
    [techTree, handleOptimize, solving]
  );

  return <>{renderedTechTree}</>;
});

/**
 * Wraps TechTreeContent with React Suspense for lazy data fetching.
 *
 * @param {TechTreeComponentProps} props - Component properties.
 * @returns {JSX.Element} Suspense-wrapped tech tree content or loading state.
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