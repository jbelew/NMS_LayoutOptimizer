// src/hooks/useClientUUID.tsx
import { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

export const useClientUUID = () => {
  const [clientUUID, setClientUUID] = useState<string | null>(null);

  useEffect(() => {
    let storedUUID = localStorage.getItem("clientUUID");
    if (!storedUUID) {
      storedUUID = uuidv4();
      localStorage.setItem("clientUUID", storedUUID);
    }
    setClientUUID(storedUUID);
  }, []);

  return clientUUID;
};
