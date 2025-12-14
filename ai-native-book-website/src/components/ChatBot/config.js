// API Configuration
const API_CONFIG = {
  // Base URL for the backend API
  BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',

  // API endpoints
  ENDPOINTS: {
    ASK: '/ask',
    HEALTH: '/health'
  },

  // Timeout settings (in milliseconds)
  TIMEOUT: 30000
};

// Helper function to get the full API URL
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

export default API_CONFIG;