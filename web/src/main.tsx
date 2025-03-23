import { Theme } from "@radix-ui/themes";
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

// Main App CSS
import './index.css';

// Component CSS files
import './components/GridCell/GridCell.css'
import './components/GridShake/GridShake.css'

import App from './App';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Theme appearance="dark" accentColor="blue" className="!bg-transparent">
      <App />
    </Theme>
  </StrictMode>,
)
