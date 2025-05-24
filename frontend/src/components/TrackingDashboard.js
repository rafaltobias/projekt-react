import React, { useState, useEffect } from 'react';
import { getTrackingStats, getRealtimeStats } from '../api/trackingService';

const TrackingDashboard = () => {
  const [stats, setStats] = useState(null);
  const [realtimeStats, setRealtimeStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timeframe, setTimeframe] = useState(30);

  useEffect(() => {
    fetchStats();
    fetchRealtimeStats();
    
    // Set up real-time updates every 30 seconds
    const interval = setInterval(fetchRealtimeStats, 30000);
    
    return () => clearInterval(interval);
  }, [timeframe]);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await getTrackingStats(timeframe);
      setStats(data);
    } catch (err) {
      setError('Failed to fetch tracking statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRealtimeStats = async () => {
    try {
      const data = await getRealtimeStats();
      setRealtimeStats(data);
    } catch (err) {
      console.error('Failed to fetch real-time stats:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Tracking Dashboard</h1>
        <div className="flex items-center space-x-4">
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(parseInt(e.target.value))}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value={1}>Last 24 hours</option>
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
          <button
            onClick={fetchStats}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Real-time Stats */}
      {realtimeStats && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-green-800 mb-2">Real-time Activity</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{realtimeStats.active_sessions}</div>
              <div className="text-sm text-green-700">Active Sessions (30m)</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{realtimeStats.hourly_views}</div>
              <div className="text-sm text-green-700">Page Views (1h)</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-green-600">
                {realtimeStats.popular_page ? realtimeStats.popular_page.page_url.split('/').pop() || 'Home' : 'N/A'}
              </div>
              <div className="text-sm text-green-700">Top Page (1h)</div>
            </div>
          </div>
        </div>
      )}

      {/* Main Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Page Views</h3>
            <div className="text-3xl font-bold text-blue-600">{stats.total_page_views}</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Unique Sessions</h3>
            <div className="text-3xl font-bold text-green-600">{stats.unique_sessions}</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Avg. Views/Session</h3>
            <div className="text-3xl font-bold text-purple-600">
              {stats.unique_sessions > 0 ? (stats.total_page_views / stats.unique_sessions).toFixed(1) : '0'}
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Custom Events</h3>
            <div className="text-3xl font-bold text-orange-600">
              {stats.events_stats ? stats.events_stats.reduce((total, event) => total + event.count, 0) : 0}
            </div>
          </div>
        </div>
      )}

      {/* Charts and Tables */}
      {stats && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top Pages */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Top Pages</h3>
            <div className="space-y-2">
              {stats.top_pages?.slice(0, 5).map((page, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600 truncate flex-1 mr-2">
                    {page.page_url.split('/').pop() || page.page_url}
                  </span>
                  <span className="font-semibold text-blue-600">{page.views}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Browser Stats */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Browsers</h3>
            <div className="space-y-2">
              {stats.browser_stats?.slice(0, 5).map((browser, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">{browser.browser}</span>
                  <span className="font-semibold text-green-600">{browser.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Operating Systems */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Operating Systems</h3>
            <div className="space-y-2">
              {stats.os_stats?.slice(0, 5).map((os, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">{os.os}</span>
                  <span className="font-semibold text-purple-600">{os.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Device Types */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Device Types</h3>
            <div className="space-y-2">
              {stats.device_stats?.map((device, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">{device.device}</span>
                  <span className="font-semibold text-orange-600">{device.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Countries */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Top Countries</h3>
            <div className="space-y-2">
              {stats.country_stats?.slice(0, 5).map((country, index) => (
                <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-sm text-gray-600">{country.country || 'Unknown'}</span>
                  <span className="font-semibold text-red-600">{country.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Custom Events */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Custom Events</h3>
            <div className="space-y-2">
              {stats.events_stats?.length > 0 ? (
                stats.events_stats.slice(0, 5).map((event, index) => (
                  <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-sm text-gray-600">{event.event_name}</span>
                    <span className="font-semibold text-indigo-600">{event.count}</span>
                  </div>
                ))
              ) : (
                <div className="text-gray-500 text-sm">No custom events tracked yet</div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Daily Stats Chart */}
      {stats && stats.daily_stats && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Daily Page Views</h3>
          <div className="h-64 flex items-end space-x-2">
            {stats.daily_stats.slice(0, 14).reverse().map((day, index) => {
              const maxViews = Math.max(...stats.daily_stats.map(d => d.page_views));
              const height = (day.page_views / maxViews) * 100;
              return (
                <div key={index} className="flex-1 flex flex-col items-center">
                  <div 
                    className="bg-blue-500 w-full rounded-t"
                    style={{ height: `${height}%` }}
                    title={`${day.date}: ${day.page_views} views`}
                  ></div>
                  <div className="text-xs text-gray-500 mt-2 transform rotate-45">
                    {new Date(day.date).toLocaleDateString()}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default TrackingDashboard;
