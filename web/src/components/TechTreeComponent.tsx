import { Separator } from "@radix-ui/themes";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";
import React, { Suspense, useEffect, useMemo, useState } from "react";
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
const TechTreeComponent: React.FC<TechTreeComponentProps> = (props) => {
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setError(null); // Reset error when component mounts or props change
  }, [props]);

  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center h-full">
          <p className="text-center sidebar__loading" style={{ color: "var(--gray-12)" }}>
            Loading tech tree...
          </p>
        </div>
      }
    >
      {error ? (
        <div className="flex flex-col items-center justify-center h-full">
          <ExclamationTriangleIcon className="w-8 h-8" style={{ color: "#C44A34" }} />
          <h2 className="text-2xl text-center" style={{ color: "#e6c133" }}>
            -kzzkt- Error! -kzzkt-
          </h2>
          <p className="text-center sidebar__error" style={{ color: "var(--gray-12)" }}>
            Problem connecting to the server!<br />
            {error.message}
          </p>
        </div>
      ) : (
        <ErrorBoundary onError={setError}>
          <TechTreeContent {...props} />
        </ErrorBoundary>
      )}
    </Suspense>
  );
};

interface ErrorBoundaryProps {
  onError: (error: Error) => void;
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.props.onError(error);
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.error) {
      return null; // Render nothing, error is handled by parent
    }
    return this.props.children;
  }
}

export default TechTreeComponent;
