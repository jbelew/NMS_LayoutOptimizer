// ShakingWrapper.tsx
import React from "react";

interface ShakingWrapperProps {
  shaking: boolean;
  children: React.ReactNode;
}

const ShakingWrapper: React.FC<ShakingWrapperProps> = ({ shaking, children }) => {
  return <div className={`relative ${shaking ? "shake" : ""}`}>{children}</div>;
};

export default ShakingWrapper;
