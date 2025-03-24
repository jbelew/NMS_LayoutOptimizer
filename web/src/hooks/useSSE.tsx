// src/hooks/useSSE.tsx
import { useState, useEffect, useRef } from "react";
import { SSE_URL } from "../constants";
import { useClientUUID } from "./useClientUUID";

export interface SSEMessage {
  status: "info" | "success" | "error";
  message: string;
  clientUUID: string;
}

interface SSEHookResult {
  clearMessages: () => void;
}

export const useSSE = (setMessagesReceived: (value: boolean) => void, setMessageQueue: (value: SSEMessage[]) => void): SSEHookResult => {
  const eventSourceRef = useRef<EventSource | null>(null);
  const clientUUID = useClientUUID();

  useEffect(() => {
    console.log("useSSE: useEffect called");
    eventSourceRef.current = new EventSource(SSE_URL);
    const eventSource = eventSourceRef.current;

    if (!eventSource) {
      console.error("useSSE: EventSource is null");
      return;
    }

    console.log("useSSE: Adding Event Listeners");

    eventSource.onopen = () => {
      console.log("useSSE: EventSource opened");
    };

    eventSource.onmessage = (event) => {
      try {
        console.log("useSSE: Message received:", event.data);
        const newMessage: SSEMessage = JSON.parse(event.data);

        if (newMessage.clientUUID === clientUUID) {
          console.log("useSSE: Message matches clientUUID:", newMessage);
          setMessageQueue((prevMessages) => [...prevMessages, newMessage]);
          setMessagesReceived(true);
        } else {
          console.log("useSSE: Message does not match clientUUID:", newMessage);
        }
      } catch (error) {
        console.error("useSSE: Error parsing SSE message:", error);
        setMessageQueue((prevMessages) => [
          ...prevMessages,
          { status: "error", message: "Error parsing server message.", clientUUID: "" },
        ]);
      }
    };

    eventSource.onerror = (error) => {
      console.error("useSSE: EventSource failed:", error);
      clearMessages();
      setMessageQueue((prevMessages) => [
        ...prevMessages,
        { status: "error", message: "Connection to server failed.", clientUUID: "" },
      ]);
      eventSource.close();
    };

    return () => {
      if (eventSourceRef.current) {
        console.log("useSSE: Closing EventSource");
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    };
  }, [clientUUID, setMessagesReceived, setMessageQueue]);

  const clearMessages = () => {
    console.log("useSSE: clearMessages called");
    setMessageQueue([]);
  };

  return { clearMessages };
};
