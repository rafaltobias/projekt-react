// Environment configuration
export const ENV = {
  API_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
} as const;

// Helper function to get full API endpoint
export const getApiEndpoint = (path: string = ''): string => {
  const baseUrl = ENV.API_URL.endsWith('/') ? ENV.API_URL.slice(0, -1) : ENV.API_URL;
  const endpoint = path.startsWith('/') ? path : `/${path}`;
  return `${baseUrl}${endpoint}`;
};

export default ENV;
