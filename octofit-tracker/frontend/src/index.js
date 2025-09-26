
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Make REACT_APP_CODESPACE_NAME available from window for debugging
window.REACT_APP_CODESPACE_NAME = process.env.REACT_APP_CODESPACE_NAME;

const root = createRoot(document.getElementById('root'));
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);

reportWebVitals();
