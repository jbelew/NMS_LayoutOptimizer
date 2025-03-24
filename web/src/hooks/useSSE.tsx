// src/hooks/useSSE.tsx
import { useState, useEffect } from "react";
import { SSE_URL } from "../constants";

interface SSEHookResult {
  messageQueue: string[];
  addMessage: (message: string) => void;
}

/**
 * Hook to use Server-Sent Events (SSE) to receive messages from a server.
 * The hook will create an EventSource object and listen for messages.
 * The messages are stored in a state variable and can be accessed as a queue.
 * The hook also provides a function to add a new message to the queue.
 *
 * @returns {SSEHookResult} An object with two properties: messageQueue and addMessage.
 *   messageQueue is an array of strings, where each string is a message received from the server.
 *   addMessage is a function that takes a string as an argument and adds it to the messageQueue.
 */
export const useSSE = (): SSEHookResult => {
  const [messageQueue, setMessageQueue] = useState<string[]>([]);

  useEffect(() => {
    console.log("useSSE: Creating EventSource");
    const eventSource = new EventSource(SSE_URL);
    console.log("useSSE: EventSource created:", eventSource);

    // Setup event handlers
    eventSource.onopen = () => {
      console.log("useSSE: EventSource opened");
    };

    eventSource.onmessage = (event) => {
      try {
        console.log("useSSE: Message received:", event.data);
        const newMessage = JSON.parse(event.data);
        addMessage(newMessage.message);
      } catch (error) {
        console.error("useSSE: Error parsing SSE message:", error);
      }
    };

    eventSource.onerror = (error) => {
      console.error("useSSE: EventSource failed:", error);
      eventSource.close();
    };

    // Cleanup when component is unmounted
    return () => {
      console.log("useSSE: Closing EventSource");
      eventSource.close();
    };
  }, []); // Empty dependency array - run only once

  const addMessage = (message: string) => {
    setMessageQueue((prevQueue) => [...prevQueue, message]);
  };

  return { messageQueue, addMessage };
};
