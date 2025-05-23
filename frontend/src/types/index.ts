export interface Visit {
  id: number;
  page_url: string;
  referrer?: string;
  user_agent?: string;
  ip_address?: string;
  timestamp: string;
  session_id?: string;
  tag_id?: number;
  tag?: Tag;
}

export interface Tag {
  id: number;
  name: string;
  description?: string;
  color: string;
  created_at: string;
  is_active: boolean;
  visit_count: number;
}

export interface StatsData {
  total_visits: number;
  unique_visitors: number;
  date_range: {
    start: string;
    end: string;
  };
  top_pages: Array<{
    page_url: string;
    visit_count: number;
  }>;
  top_referrers: Array<{
    referrer: string;
    visit_count: number;
  }>;
  daily_visits: Array<{
    date: string;
    visit_count: number;
    unique_visitors: number;
  }>;
  recent_visits: Visit[];
}

export interface DashboardStats {
  today: {
    visits: number;
    unique_visitors: number;
  };
  week: {
    visits: number;
    unique_visitors: number;
  };
  month: {
    visits: number;
    unique_visitors: number;
  };
  total: {
    visits: number;
    unique_visitors: number;
  };
  popular_tag: {
    name: string | null;
    visit_count: number;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  [key: string]: any;
}

export interface PaginationInfo {
  page: number;
  pages: number;
  per_page: number;
  total: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface VisitsResponse {
  visits: Visit[];
  pagination: PaginationInfo;
}

export interface TrackVisitRequest {
  page_url?: string;
  referrer?: string;
  session_id?: string;
  tag?: string;
}

export interface CreateTagRequest {
  name: string;
  description?: string;
  color?: string;
  is_active?: boolean;
}

export interface UpdateTagRequest {
  name?: string;
  description?: string;
  color?: string;
  is_active?: boolean;
}
