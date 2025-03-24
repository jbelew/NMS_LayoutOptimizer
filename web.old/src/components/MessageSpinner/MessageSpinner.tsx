// MessageSpinner.tsx
import React, { useEffect, useState } from "react";
import { Text } from "@radix-ui/themes";

interface SSEMessage {
  status: "info" | "success" | "error";
  message: string;
}

interface MessageSpinnerProps {
  solving: boolean;
  messageHistory: SSEMessage[]; // Receive messageHistory
}

/**
 * MessageSpinner component that displays a loading spinner overlay when solving is true,
 * along with a history of messages.
 *
 * @param {MessageSpinnerProps} props - The properties passed to the component.
 * @param {boolean} props.solving - Determines whether the spinner is visible.
 * @param {SSEMessage[]} props.messageHistory - An array of messages to display alongside the spinner.
 * @returns {JSX.Element | null} The rendered spinner element or null.
 */
const MessageSpinner: React.FC<MessageSpinnerProps> = ({ solving, messageHistory }) => {
  const [displayedMessages, setDisplayedMessages] = useState<SSEMessage[]>([]);

  useEffect(() => {
    setDisplayedMessages([...messageHistory]); // Update displayedMessages whenever messageHistory changes
  }, [messageHistory]);

  useEffect(() => {
    return () => {
      setDisplayedMessages([]);
    };
  }, []);

  return (
    solving && (
      <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-opacity-75 rounded-lg">
        <div className="w-16 h-16 border-8 rounded-full border-slate-600 animate-spin" style={{ borderTopColor: "var(--blue-9)" }}></div>
        {displayedMessages.map((msg, index) => (
          <Text key={index} className="pt-4">
            {`${msg.status}: ${msg.message}`}
          </Text>
        ))}
      </div>
    )
  );
};

export default MessageSpinner;
