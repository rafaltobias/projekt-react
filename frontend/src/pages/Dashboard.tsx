import React from 'react';
import { useDashboardStats } from '../hooks/useApi';
import { 
  ChartBarIcon, 
  EyeIcon, 
  UserGroupIcon, 
  CalendarIcon,
  ClockIcon,
  TagIcon
} from '@heroicons/react/24/outline';

const StatCard: React.FC<{
  title: string;
  value: number;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
}> = ({ title, value, icon: Icon, color }) => (
  <div className="bg-white overflow-hidden shadow rounded-lg">
    <div className="p-5">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <Icon className={`h-6 w-6 ${color}`} />
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd className="text-lg font-medium text-gray-900">{value.toLocaleString()}</dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
);

const Dashboard: React.FC = () => {
  const { stats, loading, error } = useDashboardStats();

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error loading dashboard</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your website analytics and visitor statistics
        </p>
      </div>

      {/* Today's Stats */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">Today</h2>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-2">
          <StatCard
            title="Visits Today"
            value={stats.today.visits}
            icon={EyeIcon}
            color="text-blue-600"
          />
          <StatCard
            title="Unique Visitors Today"
            value={stats.today.unique_visitors}
            icon={UserGroupIcon}
            color="text-green-600"
          />
        </div>
      </div>

      {/* This Week */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">This Week</h2>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-2">
          <StatCard
            title="Visits This Week"
            value={stats.week.visits}
            icon={CalendarIcon}
            color="text-purple-600"
          />
          <StatCard
            title="Unique Visitors This Week"
            value={stats.week.unique_visitors}
            icon={UserGroupIcon}
            color="text-indigo-600"
          />
        </div>
      </div>

      {/* This Month */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">This Month</h2>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-2">
          <StatCard
            title="Visits This Month"
            value={stats.month.visits}
            icon={ChartBarIcon}
            color="text-orange-600"
          />
          <StatCard
            title="Unique Visitors This Month"
            value={stats.month.unique_visitors}
            icon={UserGroupIcon}
            color="text-red-600"
          />
        </div>
      </div>

      {/* All Time */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">All Time</h2>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <StatCard
            title="Total Visits"
            value={stats.total.visits}
            icon={EyeIcon}
            color="text-gray-600"
          />
          <StatCard
            title="Total Unique Visitors"
            value={stats.total.unique_visitors}
            icon={UserGroupIcon}
            color="text-gray-600"
          />
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <TagIcon className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Most Popular Tag
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {stats.popular_tag.name || 'No tags yet'} 
                      {stats.popular_tag.name && (
                        <span className="text-sm text-gray-500 ml-2">
                          ({stats.popular_tag.visit_count} visits)
                        </span>
                      )}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Quick Actions</h3>
          <div className="mt-5">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <a
                href="/statistics"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200"
              >
                <ChartBarIcon className="h-4 w-4 mr-2" />
                View Statistics
              </a>
              <a
                href="/visits"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200"
              >
                <EyeIcon className="h-4 w-4 mr-2" />
                View Visits
              </a>
              <a
                href="/tags"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-purple-700 bg-purple-100 hover:bg-purple-200"
              >
                <TagIcon className="h-4 w-4 mr-2" />
                Manage Tags
              </a>
              <button
                onClick={() => window.location.reload()}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200"
              >
                <ClockIcon className="h-4 w-4 mr-2" />
                Refresh Data
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
