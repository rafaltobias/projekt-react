import axios from 'axios';
import { Stats, Tag } from './types';

const API_URL = 'http://localhost:5000';

export const trackVisit = async (
  pageUrl: string, 
  browser: string | null = null, 
  os: string | null = null, 
  device: string | null = null, 
  country: string | null = null, 
  sessionId: string | null = null, 
  isEntryPage: boolean = false, 
  isExitPage: boolean = false
): Promise<any> => {
  try {
    const response = await axios.post(`${API_URL}/api/track`, {
      page_url: pageUrl,
      browser,
      os,
      device,
      country,
      session_id: sessionId,
      is_entry_page: isEntryPage,
      is_exit_page: isExitPage
    });
    return response.data;
  } catch (error) {
    console.error('Error tracking visit:', error);
    throw error;
  }
};

export const getStats = async (): Promise<Stats> => {
  try {
    const response = await axios.get(`${API_URL}/api/stats`);
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export const exportStats = async (): Promise<boolean> => {
  try {
    window.open(`${API_URL}/api/exportStats`, '_blank');
    return true;
  } catch (error) {
    console.error('Error exporting stats:', error);
    throw error;
  }
};

export const createTag = async (
  name: string, 
  description: string = '', 
  type: string | null = null, 
  trigger: string | null = null, 
  config: any = null
): Promise<Tag> => {
  try {
    const response = await axios.post(`${API_URL}/api/tags`, { 
      name, 
      description, 
      type, 
      trigger, 
      config 
    });
    return response.data;
  } catch (error) {
    console.error('Error creating tag:', error);
    throw error;
  }
};

export const getTags = async (): Promise<Tag[]> => {
  try {
    const response = await axios.get(`${API_URL}/api/tags`);
    // Handle the response format { tags: [...] }
    if (response.data && Array.isArray(response.data.tags)) {
      return response.data.tags;
    }
    // Fallback: if it's a direct array
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching tags:', error);
    // Return empty array on error rather than throwing
    return [];
  }
};

export const getTagById = async (id: number): Promise<Tag> => {
  try {
    const response = await axios.get(`${API_URL}/api/tags/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tag with id ${id}:`, error);
    throw error;
  }
};

export const deleteTag = async (id: number): Promise<any> => {
  try {
    const response = await axios.delete(`${API_URL}/api/tags/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting tag with id ${id}:`, error);
    throw error;
  }
};
