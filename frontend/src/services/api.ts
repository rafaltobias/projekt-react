import axios from 'axios';
import {
  Tag,
  StatsData,
  DashboardStats,
  ApiResponse,
  VisitsResponse,
  TrackVisitRequest,
  CreateTagRequest,
  UpdateTagRequest
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const analyticsApi = {
  // Visit tracking
  trackVisit: async (data: TrackVisitRequest): Promise<ApiResponse<any>> => {
    const response = await api.post('/track', data);
    return response.data;
  },

  getVisits: async (params?: {
    page?: number;
    per_page?: number;
    tag_id?: number;
    start_date?: string;
    end_date?: string;
  }): Promise<ApiResponse<VisitsResponse>> => {
    const response = await api.get('/visits', { params });
    return response.data;
  },

  // Statistics
  getStats: async (params?: {
    start_date?: string;
    end_date?: string;
    tag_id?: number;
  }): Promise<ApiResponse<StatsData>> => {
    const response = await api.get('/stats', { params });
    return response.data;
  },

  getDashboardStats: async (): Promise<ApiResponse<DashboardStats>> => {
    const response = await api.get('/stats/dashboard');
    return response.data;
  },

  exportStats: async (params?: {
    start_date?: string;
    end_date?: string;
    tag_id?: number;
    type?: string;
  }): Promise<Blob> => {
    const response = await api.get('/exportStats', {
      params,
      responseType: 'blob',
    });
    return response.data;
  },

  // Tags
  getTags: async (includeInactive?: boolean): Promise<ApiResponse<{ tags: Tag[] }>> => {
    const response = await api.get('/tags', {
      params: { include_inactive: includeInactive },
    });
    return response.data;
  },

  getTagById: async (id: number): Promise<ApiResponse<{ tag: Tag }>> => {
    const response = await api.get(`/tags/${id}`);
    return response.data;
  },

  createTag: async (data: CreateTagRequest): Promise<ApiResponse<{ tag: Tag }>> => {
    const response = await api.post('/tags', data);
    return response.data;
  },

  updateTag: async (id: number, data: UpdateTagRequest): Promise<ApiResponse<{ tag: Tag }>> => {
    const response = await api.put(`/tags/${id}`, data);
    return response.data;
  },

  deleteTag: async (id: number, force?: boolean): Promise<ApiResponse<any>> => {
    const response = await api.delete(`/tags/${id}`, {
      params: { force },
    });
    return response.data;
  },

  getTagStats: async (
    id: number,
    params?: {
      start_date?: string;
      end_date?: string;
    }
  ): Promise<ApiResponse<any>> => {
    const response = await api.get(`/tags/${id}/stats`, { params });
    return response.data;
  },
};

export default analyticsApi;
