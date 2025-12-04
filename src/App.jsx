import React from 'react';
import AppRouter from './AppRouter';
import { ThemeProvider } from './context/ThemeContext';
import { ChatProvider } from './context/ChatContext';
import './index.css';

function App() {
  return (
    <ThemeProvider>
      <ChatProvider>
        <AppRouter />
      </ChatProvider>
    </ThemeProvider>
  );
}

export default App;
