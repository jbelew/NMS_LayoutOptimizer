import { useState, useEffect } from "react";
import { TechTree } from "../components/TechTree"; // Import the TechTree interface

/**
 * Custom hook to fetch and manage the technology tree data for a specified ship type.
 * 
 * This hook performs an asynchronous fetch request to retrieve the technology tree 
 * from a designated API endpoint based on the provided ship type. It manages the 
 * loading, error, and tech tree states, and automatically triggers a fetch request 
 * whenever the ship type changes.
 * 
 * @param {string} shipType - The type of ship to fetch the tech tree for. Defaults to "Exotic".
 * @returns {Object} An object containing the tech tree data, loading state, and error message (if any).
 * - techTree: The fetched technology tree data or null if not yet available.
 * - loading: Boolean indicating whether the fetch request is in progress.
 * - error: Error message if the fetch request fails, otherwise null.
 */

export const useFetchTechTree = (shipType: string = "Exotic"): { techTreeState: TechTree | null; loadingState: boolean; errorState: string | null } => {
  const [techTreeState, setTechTreeState] = useState<TechTree | null>(null);
  const [loadingState, setLoadingState] = useState<boolean>(true);
  const [errorState, setErrorState] = useState<string | null>(null);

  useEffect(() => {
    /**
     * Fetches the tech tree data from the API and updates the state accordingly.
     * @param {string} shipType - The type of ship to fetch the tech tree for.
     * @returns {Promise<void>} - A promise that resolves when the fetch operation is complete.
     */
    const fetchTechTreeData = async (shipType: string): Promise<void> => {
      setLoadingState(true);
      setErrorState(null);
      try {
        const response = await fetch(`http://localhost:5000/tech_tree/${shipType}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: TechTree = await response.json();
        setTechTreeState(data);
      } catch (error) {
        if (error instanceof Error) {
          setErrorState(error.message);
        } else {
          setErrorState("An unknown error occurred");
        }
      } finally {
        setLoadingState(false);
      }
    };

    fetchTechTreeData(shipType);
  }, [shipType]);

  return { techTreeState, loadingState, errorState };
};
