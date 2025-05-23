import { useState, useEffect, useCallback } from 'react';
import analyticsApi from '../services/api';
import { StatsData, DashboardStats, Tag, Visit } from '../types';

export const useStats = (startDate?: string, endDate?: string, tagId?: number) => {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await analyticsApi.getStats({
        start_date: startDate,
        end_date: endDate,
        tag_id: tagId,
      });
      
      if (response.success) {
        setStats(response.data!);
      } else {
        setError(response.message || 'Failed to fetch statistics');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate, tagId]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return { stats, loading, error, refetch: fetchStats };
};

export const useDashboardStats = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await analyticsApi.getDashboardStats();
        
        if (response.success) {
          setStats(response.data!);
        } else {
          setError(response.message || 'Failed to fetch dashboard statistics');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardStats();
  }, []);

  return { stats, loading, error };
};

export const useTags = (includeInactive = false) => {
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTags = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await analyticsApi.getTags(includeInactive);
      
      if (response.success) {
        setTags(response.tags);
      } else {
        setError(response.message || 'Failed to fetch tags');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [includeInactive]);

  useEffect(() => {
    fetchTags();
  }, [fetchTags]);

  const createTag = async (tagData: any) => {
    try {
      const response = await analyticsApi.createTag(tagData);
      if (response.success) {
        await fetchTags(); // Refresh the tags list
        return response.tag;
      } else {
        throw new Error(response.message || 'Failed to create tag');
      }
    } catch (err) {
      throw err;
    }
  };

  const updateTag = async (id: number, tagData: any) => {
    try {
      const response = await analyticsApi.updateTag(id, tagData);
      if (response.success) {
        await fetchTags(); // Refresh the tags list
        return response.tag;
      } else {
        throw new Error(response.message || 'Failed to update tag');
      }
    } catch (err) {
      throw err;
    }
  };

  const deleteTag = async (id: number, force = false) => {
    try {
      const response = await analyticsApi.deleteTag(id, force);
      if (response.success) {
        await fetchTags(); // Refresh the tags list
        return response;
      } else {
        throw new Error(response.message || 'Failed to delete tag');
      }
    } catch (err) {
      throw err;
    }
  };

  return {
    tags,
    loading,
    error,
    refetch: fetchTags,
    createTag,
    updateTag,
    deleteTag,
  };
};

export const useVisits = (
  page = 1,
  perPage = 50,
  tagId?: number,
  startDate?: string,
  endDate?: string
) => {
  const [visits, setVisits] = useState<Visit[]>([]);
  const [pagination, setPagination] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVisits = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await analyticsApi.getVisits({
          page,
          per_page: perPage,
          tag_id: tagId,
          start_date: startDate,
          end_date: endDate,
        });
        
        if (response.success) {
          const data = response as any; // Type assertion for complex response structure
          setVisits(data.visits);
          setPagination(data.pagination);
        } else {
          setError(response.message || 'Failed to fetch visits');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchVisits();
  }, [page, perPage, tagId, startDate, endDate]);

  return { visits, pagination, loading, error };
};
