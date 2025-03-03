import React from "react";
import { useGridStore } from "./store/useGridStore";
import GridTable from "../src/components/GridTable"; // Import the GridTable component
import { Button, Spinner} from "@radix-ui/themes";

const App: React.FC = () => {
  const { grid, result, loading, handleOptimize, toggleCellState } = useGridStore();

  return (
    <div className="m-8 App">
      <h1 className="text-4xl font-bold">No Man's Sky Starship Optimizer</h1>
      <Button onClick={() => handleOptimize("infra")} disabled={loading}>
        <Spinner loading={loading}>
        </Spinner>
        {loading ? "Optimizing..." : "Optimize Infra"}
      </Button>
      <button onClick={() => handleOptimize("shield")} disabled={loading}>
        {loading ? "Optimizing..." : "Optimize Shield"}
      </button>
      <GridTable grid={grid} loading={loading} toggleCellState={toggleCellState} result={result} />
    </div>
  );
};

export default App;
