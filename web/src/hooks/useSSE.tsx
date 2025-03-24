// src/hooks/useSSE.tsx
import { useState, useEffect, useRef, useCallback } from "react";
import { SSE_URL } from "../constants";
import { v4 as uuidv4 } from 'uuid';

interface SSEHookResult {
  isConnected: boolean;
  clientId: string;
  registerMessageHandler: (handler: (message: string) => void) => void;
}

/**
 * Hook to use Server-Sent Events (SSE) to receive messages from a server.
 * The hook will create an EventSource object and listen for messages.
 * The messages are filtered by clientId.
 * The hook also provides a function to register a message handler.
 *
 * @returns {SSEHookResult} An object with three properties: isConnected, clientId, and registerMessageHandler.
 *   isConnected is a boolean indicating whether the SSE connection is currently open.
 *   clientId is a unique identifier for this client.
 *   registerMessageHandler is a function that takes a callback function as an argument.
 */
export const useSSE = (): SSEHookResult => {
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const clientId = useRef<string>(uuidv4()).current; // Generate a unique client ID
  const messageHandlers = useRef<((message: string) => void)[]>([]); // Array of callback functions

  useEffect(() => {
    console.log(`useSSE: Creating EventSource for client: ${clientId}`);
    eventSourceRef.current = new EventSource(`${SSE_URL}?clientId=${clientId}`); // Append clientId to URL
    const eventSource = eventSourceRef.current;
    console.log("useSSE: EventSource created:", eventSource);

    // Setup event handlers
    eventSource.onopen = () => {
      console.log(`useSSE: EventSource opened for client: ${clientId}`);
      setIsConnected(true);
    };

    eventSource.onmessage = (event) => {
      try {
        console.log(`useSSE: Message received for client ${clientId}:`, event.data);
        const parsedData = JSON.parse(event.data);
        // Check if the message is for this client
        if (parsedData.clientId === clientId) {
          // Call all registered handlers
          messageHandlers.current.forEach((handler) => handler(parsedData.message));
        } else {
          console.log(`useSSE: Message not for this client ${clientId}, ignoring.`);
        }
      } catch (error) {
        console.error("useSSE: Error parsing SSE message:", error);
      }
    };

    eventSource.onerror = (error) => {
      console.error(`useSSE: EventSource failed for client: ${clientId}`, error);
      setIsConnected(false);
      eventSource.close();
    };

    // Cleanup when component is unmounted
    return () => {
      console.log(`useSSE: Closing EventSource for client: ${clientId}`);
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    };
  }, [clientId]); // Dependency array includes clientId

  // Function to register a message handler
  const registerMessageHandler = useCallback((handler: (message: string) => void) => {
    messageHandlers.current.push(handler);
  }, []);

  return { isConnected, clientId, registerMessageHandler };
};
