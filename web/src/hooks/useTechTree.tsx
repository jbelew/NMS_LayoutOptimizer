import { TechTree } from "../components/TechTreeComponent";

type Resource<T> = {
  read: () => T;
};

const createResource = <T,>(promise: Promise<T>): Resource<T> => {
  let status: "pending" | "success" | "error" = "pending";
  let result: T;
  let error: Error;

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
    read() {
      if (status === "pending") throw suspender;
      if (status === "error") throw error;
      return result!;
    },
  };
};

const cache = new Map<string, Resource<TechTree>>(); // Store successful fetches

function fetchTechTree(shipType: string = "Exotic"): Resource<TechTree> {
  if (!cache.has(shipType)) {
    const promise = fetch(`http://localhost:5000/tech_tree/${shipType}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data: TechTree) => data);

    cache.set(shipType, createResource(promise));
  }

  return cache.get(shipType)!;
}

export function useFetchTechTreeSuspense(shipType: string = "Exotic"): TechTree {
  return fetchTechTree(shipType).read();
}
