import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const trackVisit = async (pageUrl, browser = null, os = null, device = null, country = null, sessionId = null, isEntryPage = false, isExitPage = false) => {
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

export const getStats = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/stats`);
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export const exportStats = async () => {
  try {
    window.open(`${API_URL}/api/exportStats`, '_blank');
    return true;
  } catch (error) {
    console.error('Error exporting stats:', error);
    throw error;
  }
};

export const createTag = async (name, description = '', type = null, trigger = null, config = null) => {
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

export const getTags = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/tags`);
    // Ensure we always return an array
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error fetching tags:', error);
    // Return empty array on error rather than throwing
    return [];
  }
};

export const getTagById = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/api/tags/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tag with id ${id}:`, error);
    throw error;
  }
};

export const deleteTag = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}/api/tags/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting tag with id ${id}:`, error);
    throw error;
  }
};
