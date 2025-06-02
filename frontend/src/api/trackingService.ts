import axios from 'axios';
import { TrackingStats, RealtimeStats, TrackingEvents, SessionData, SessionAnalytics } from './types';

const API_URL = 'http://localhost:5000';

// Tracking API functions
export const getTrackingStats = async (days = 30): Promise<TrackingStats> => {
  try {
    const response = await axios.get<TrackingStats>(`${API_URL}/api/tracking/stats?days=${days}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tracking stats:', error);
    throw error;
  }
};

export const getRealtimeStats = async (): Promise<RealtimeStats> => {
  try {
    const response = await axios.get<RealtimeStats>(`${API_URL}/api/tracking/realtime`);
    return response.data;
  } catch (error) {
    console.error('Error fetching real-time stats:', error);
    throw error;
  }
};

export const getTrackingEvents = async (page = 1, perPage = 50, type = 'all'): Promise<TrackingEvents> => {
  try {
    const response = await axios.get<TrackingEvents>(`${API_URL}/api/tracking/events`, {
      params: { page, per_page: perPage, type }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching tracking events:', error);
    throw error;
  }
};

export const getSessionData = async (sessionId: string): Promise<SessionData> => {
  try {
    const response = await axios.get<SessionData>(`${API_URL}/api/tracking/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching session data:', error);
    throw error;
  }
};

export const getSessionAnalytics = async (): Promise<SessionAnalytics> => {
  try {
    const response = await axios.get<SessionAnalytics>(`${API_URL}/api/tracking/sessions`);
    return response.data;
  } catch (error) {
    console.error('Error fetching session analytics:', error);
    throw error;
  }
};

// Manual tracking function (for testing)
export interface EventData {
  session_id: string;
  page_url: string;
  referrer?: string;
  browser?: string;
  os?: string;
  device?: string;
  event_name?: string;
  event_data?: any;
}

export const trackEvent = async (eventData: EventData): Promise<any> => {
  try {
    const response = await axios.post(`${API_URL}/api/track`, eventData);
    return response.data;
  } catch (error) {
    console.error('Error tracking event:', error);
    throw error;
  }
};
