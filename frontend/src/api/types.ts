// Define interfaces for API responses
export interface PageInfo {
  page_url: string;
  count: number;
}

export interface RealtimeStats {
  active_sessions: number;
  page_views_last_hour: number;
  top_pages_today: PageInfo[];
  recent_events: any[];
}

export interface TrackingStats {
  total_page_views: number;
  total_custom_events: number;
  unique_sessions: number;
  top_pages: PageInfo[];
  top_events: any[];
  hourly_stats: { hour: number; count: number }[];
  daily_stats: { date: string; count: number }[];
}

export interface TrackingEvents {
  events: any[];
  page: number;
  per_page: number;
  type: string;
  total: number;
  has_next: boolean;
}

export interface SessionData {
  session_id: string;
  events: any[];
  total_events: number;
  duration: number;
  entry_page: string;
  exit_page: string;
}

export interface SessionAnalytics {
  total_sessions: number;
  average_session_duration: number;
  bounce_rate: number;
  top_entry_pages: PageInfo[];
  top_exit_pages: PageInfo[];
}

// Stats interfaces
export interface DateVisit {
  date: string;
  count: number;
}

export interface BrowserStat {
  browser: string;
  count: number;
}

export interface OperatingSystemStat {
  os: string;
  count: number;
}

export interface CountryStat {
  country: string;
  count: number;
}

export interface Stats {
  daily_visits: DateVisit[];
  top_pages: PageInfo[];
  browsers: BrowserStat[];
  operating_systems: OperatingSystemStat[];
  countries: CountryStat[];
  total_visits: number;
}

// Chart.js data types
export interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string;
  borderWidth?: number;
  tension?: number;
  fill?: boolean;
}

export interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

// Common types
export interface Tag {
  id: number;
  name: string;
  description: string;
  type: string;
  trigger: string;
  config: any;
  created_at: string;
}
