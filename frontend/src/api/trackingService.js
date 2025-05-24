import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Tracking API functions
export const getTrackingStats = async (days = 30) => {
  try {
    const response = await axios.get(`${API_URL}/api/tracking/stats?days=${days}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tracking stats:', error);
    throw error;
  }
};

export const getRealtimeStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/tracking/realtime`);
    return response.data;
  } catch (error) {
    console.error('Error fetching real-time stats:', error);
    throw error;
  }
};

export const getTrackingEvents = async (page = 1, perPage = 50, type = 'all') => {
  try {
    const response = await axios.get(`${API_URL}/api/tracking/events`, {
      params: { page, per_page: perPage, type }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching tracking events:', error);
    throw error;
  }
};

export const getSessionData = async (sessionId) => {
  try {
    const response = await axios.get(`${API_URL}/api/tracking/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching session data:', error);
    throw error;
  }
};

export const getSessionAnalytics = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/tracking/sessions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching session analytics:', error);
    throw error;
  }
};

// Manual tracking function (for testing)
export const trackEvent = async (eventData) => {
  try {
    const response = await axios.post(`${API_URL}/api/track`, eventData);
    return response.data;
  } catch (error) {
    console.error('Error tracking event:', error);
    throw error;
  }
};
