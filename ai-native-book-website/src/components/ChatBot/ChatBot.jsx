import React, { useState, useRef, useEffect } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import './ChatBot.css';

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const { colorMode } = useColorMode();

  // Function to get selected text
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText.length > 0) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 100);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { type: 'user', content: inputValue, timestamp: new Date() };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get selected text if any
      const currentSelectedText = window.getSelection().toString().trim();

      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputValue,
          selected_text: currentSelectedText || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        type: 'bot',
        content: data.answer,
        sources: data.sources || [],
        selectedTextUsed: data.selected_text_used,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          className={`chatbot-button ${colorMode}`}
          onClick={toggleChat}
          aria-label="Open chat"
        >
          💬 AI Book Assistant
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={`chatbot-container ${colorMode}`}>
          <div className="chatbot-header">
            <div className="chatbot-title">AI Book Assistant</div>
            <div className="chatbot-controls">
              <button
                onClick={clearChat}
                className="chatbot-clear-btn"
                title="Clear chat"
                disabled={messages.length === 0}
              >
                🗑️
              </button>
              <button
                onClick={toggleChat}
                className="chatbot-close-btn"
                title="Close chat"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your AI assistant for the AI Native Book.</p>
                <p>Ask me anything about the book content, or select text and ask questions about it specifically.</p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`chatbot-message ${message.type}`}
                >
                  <div className="message-content">
                    {message.content}
                  </div>
                  {message.type === 'bot' && message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <details>
                        <summary>Sources ({message.sources.length})</summary>
                        {message.sources.map((source, idx) => (
                          <div key={idx} className="source-item">
                            <small>
                              <strong>From:</strong> {source.source}
                              {source.page && ` (${source.page})`}
                              {source.relevance_score && ` [Relevance: ${(source.relevance_score * 100).toFixed(1)}%]`}
                            </small>
                            <p><em>{source.content}</em></p>
                          </div>
                        ))}
                      </details>
                    </div>
                  )}
                  {message.selectedTextUsed && (
                    <div className="message-info">
                      <small>🔍 Answer based on selected text</small>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message bot">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input-area">
            {selectedText && (
              <div className="selected-text-preview">
                <small>Selected text: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
              </div>
            )}
            <div className="chatbot-input-container">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about the book..."
                className="chatbot-input"
                rows="1"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                className="chatbot-send-btn"
                disabled={!inputValue.trim() || isLoading}
              >
                {isLoading ? '⏳' : '➤'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatBot;