import { Theme } from "@radix-ui/themes";
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import "@radix-ui/themes/styles.css";
import './index.css';

import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Theme appearance="dark" accentColor="cyan" className="!bg-transparent">
      <App />
    </Theme>
  </StrictMode>,
)
