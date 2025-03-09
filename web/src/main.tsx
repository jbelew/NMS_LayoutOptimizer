import { Theme } from "@radix-ui/themes";
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import './index.css';

import App from './App_new.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Theme appearance="dark" accentColor="blue" className="!bg-transparent">
      <App />
    </Theme>
  </StrictMode>,
)
