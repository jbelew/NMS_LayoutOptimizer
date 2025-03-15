import { TechTree } from "../components/TechTreeComponent";

type Resource<T> = {
  read: () => T;
};

/**
 * Creates a resource from a promise, which can be used with React Suspense.
 *
 * @template T - The type of the resource.
 * @param {Promise<T>} promise - The promise to create the resource from.
 * @returns {Resource<T>} An object with a read method that will throw the promise
 * if the resource is pending, or the error if it failed, or return the result if successful.
 */
const createResource = <T,>(promise: Promise<T>): Resource<T> => {
  let status: "pending" | "success" | "error" = "pending";
  let result: T;
  let error: Error;

  // Create a suspender by handling the promise
  const suspender = promise
    .then((res) => {
      status = "success";
      result = res;
    })
    .catch((err) => {
      status = "error";
      error = err;
    });

  return {
    /**
     * Reads the resource, throwing if it's still pending or errored, or returning the result.
     * 
     * @throws Will throw the promise if pending, or the error if there was an error.
     * @returns {T} The result of the promise if successful.
     */
    read() {
      if (status === "pending") throw suspender; // Throw the promise for suspense
      if (status === "error") throw error; // Throw the error if there was one
      return result!; // Return the result if successful
    },
  };
};

const cache = new Map<string, Resource<TechTree>>(); // Store successful fetches

/**
 * Fetches a tech tree by ship type and stores it in the cache.
 * If the resource is already in the cache, it will return the cached version.
 * @param {string} shipType - The type of ship to fetch the tech tree for. Defaults to "Exotic".
 * @returns {Resource<TechTree>} An object with a read method that can be used with React Suspense.
 */
function fetchTechTree(shipType: string = "Exotic"): Resource<TechTree> {
  // Check if the resource is already in the cache
  if (!cache.has(shipType)) {
    // Create a promise to fetch the tech tree
    const promise = fetch(`http://localhost:5000/tech_tree/${shipType}`)
      .then((res) => {
        // Check for HTTP errors
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        // Return the JSON response
        return res.json();
      })
      .then((data: TechTree) => data);

    // Store the promise in the cache
    cache.set(shipType, createResource(promise));
  }

  // Return the cached resource
  return cache.get(shipType)!;
}

/**
 * Custom React hook to fetch a tech tree for a given ship type using Suspense.
 *
 * @param {string} shipType - The type of ship to fetch the tech tree for. Defaults to "Exotic".
 * @returns {TechTree} The fetched tech tree data for the specified ship type.
 */
export function useFetchTechTreeSuspense(shipType: string = "Exotic"): TechTree {
  // Fetch the tech tree resource and use the read method to get the data
  return fetchTechTree(shipType).read();
}
