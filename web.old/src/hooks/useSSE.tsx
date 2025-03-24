// src/hooks/useSSE.tsx
import { useState, useEffect, useRef } from "react";
import { SSE_URL } from "../constants";

interface SSEMessage {
  status: "info" | "success" | "error";
  message: string;
}

interface SSEHookResult {
  messages: SSEMessage[];
  clearMessages: () => void;
}

/**
 * Hook to use Server-Sent Events (SSE) to receive messages from a server.
 * Handles different message types and provides a function to clear the message queue.
 */
export const useSSE = (): SSEHookResult => {
  const [messages, setMessages] = useState<SSEMessage[]>([]);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    console.log("useSSE: Creating EventSource");
    eventSourceRef.current = new EventSource(SSE_URL);
    const eventSource = eventSourceRef.current;
    console.log("useSSE: EventSource created:", eventSource);

    eventSource.onopen = () => {
      console.log("useSSE: EventSource opened");
    };

    eventSource.onmessage = (event) => {
      try {
        console.log("useSSE: Message received:", event.data);
        const newMessage: SSEMessage = JSON.parse(event.data);
        setMessages((prevMessages) => [...prevMessages, newMessage]);
      } catch (error) {
        console.error("useSSE: Error parsing SSE message:", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          { status: "error", message: "Error parsing server message." },
        ]);
      }
    };

    eventSource.onerror = (error) => {
      console.error("useSSE: EventSource failed:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { status: "error", message: "Connection to server failed." },
      ]);
      eventSource.close();
    };

    return () => {
      console.log("useSSE: Closing EventSource");
      eventSource.close();
      setMessages([]); // Clear messages on unmount
    };
  }, []);

  const clearMessages = () => {
    setMessages([]);
  };

  return { messages, clearMessages };
};
