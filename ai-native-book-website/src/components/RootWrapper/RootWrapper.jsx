import React from 'react';
import ChatBot from '../ChatBot';

// Docusaurus Root component - this wraps the entire app
function Root({ children }) {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}

export default Root;