// /home/jbelew/projects/nms/web/src/hooks/useTechTree.tsx

import { useState, useEffect } from "react";
import { TechTree } from "../components/TechTreeComponent"; // Import the TechTree interface

/**
 * Custom hook to fetch and manage the technology tree data for a specified ship type.
 *
 * This hook performs an asynchronous fetch request to retrieve the technology tree
 * from a designated API endpoint based on the provided ship type. It manages the
 * loading, error, and tech tree states, and automatically triggers a fetch request
 * whenever the ship type changes.
 *
 * @param {string} shipType - The type of ship to fetch the tech tree for. Defaults to "Exotic".
 * @returns {[TechTree | null, boolean, string | null]} A tuple containing the tech tree data, loading state, and error message (if any).
 */
export const useFetchTechTree = (shipType: string = "Exotic"): [TechTree | null, boolean, string | null] => {
  const [techTree, setTechTree] = useState<TechTree | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    /**
     * Fetches the tech tree data from the API and updates the state accordingly.
     * @param {string} shipType - The type of ship to fetch the tech tree for.
     * @returns {Promise<void>} - A promise that resolves when the fetch operation is complete.
     */
    const fetchTechTreeData = async (shipType: string): Promise<void> => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://localhost:5000/tech_tree/${shipType}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: TechTree = await response.json();
        setTechTree(data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
          console.error(err.message);
        } else {
          setError("An unknown error occurred");
          console.error("An unknown error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTechTreeData(shipType);
  }, [shipType]);

  return [techTree, loading, error]; // Return as a tuple
};
