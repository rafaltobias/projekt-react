import React, { useState, useEffect } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { getStats, exportStats } from '../api/apiService';

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const StatsDisplay = () => {
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setIsLoading(true);
        const data = await getStats();
        setStats(data);
      } catch (err) {
        setError('Failed to load statistics');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  const handleExport = async () => {
    try {
      await exportStats();
    } catch (err) {
      console.error('Export failed:', err);
      alert('Failed to export statistics');
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Loading statistics...</div>;
  }

  if (error) {
    return <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>;
  }

  if (!stats) {
    return <div className="text-center py-8 text-gray-500">No statistics available</div>;
  }
  // Prepare chart data
  const dateLabels = stats.by_date?.map(item => new Date(item.date).toLocaleDateString()) || [];
  const dateCounts = stats.by_date?.map(item => item.count) || [];

  const visitsByDateData = {
    labels: dateLabels,
    datasets: [
      {
        label: 'Visits',
        data: dateCounts,
        fill: false,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
        tension: 0.1
      }
    ]
  };

  const topUrlsData = {
    labels: stats.top_urls?.map(item => item.page_url) || [],
    datasets: [
      {
        label: 'Visits',
        data: stats.top_urls?.map(item => item.count) || [],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
        ]
      }
    ]
  };

  const browsersData = {
    labels: stats.top_browsers?.map(item => item.browser) || [],
    datasets: [
      {
        label: 'Browser Usage',
        data: stats.top_browsers?.map(item => item.count) || [],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderWidth: 1
      }
    ]
  };
  
  const osData = {
    labels: stats.top_os?.map(item => item.os) || [],
    datasets: [
      {
        label: 'OS Usage',
        data: stats.top_os?.map(item => item.count) || [],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
        borderWidth: 1
      }
    ]
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Visit Statistics</h2>
        <button
          onClick={handleExport}
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        >
          Export CSV
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Total Visits</h3>
          <p className="text-4xl font-bold text-blue-600">{stats.total}</p>
        </div>
      </div>

      <div className="mb-8">
        <h3 className="text-xl font-semibold mb-4">Visits by Date (Last 30 days)</h3>
        <div className="h-80">
          <Line 
            data={visitsByDateData} 
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                y: {
                  beginAtZero: true,
                  ticks: {
                    precision: 0
                  }
                }
              }
            }} 
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-xl font-semibold mb-4">Top URLs</h3>
          <div className="h-80">
            <Bar 
              data={topUrlsData} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                scales: {
                  x: {
                    beginAtZero: true,
                    ticks: {
                      precision: 0
                    }
                  }
                },
                plugins: {
                  tooltip: {
                    callbacks: {
                      title: function(context) {
                        const title = context[0].label || '';
                        return title.length > 30 ? title.substr(0, 30) + '...' : title;
                      }
                    }
                  }
                }
              }} 
            />
          </div>
        </div>        <div>
            <h3 className="text-xl font-semibold mb-4">Top Browsers</h3>
            <div className="h-80">
              <Pie 
                data={browsersData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                }} 
              />
            </div>
          </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <div>
          <h3 className="text-xl font-semibold mb-4">Operating Systems</h3>
          <div className="h-80">
            <Pie 
              data={osData}
              options={{
                responsive: true,
                maintainAspectRatio: false,
              }} 
            />
          </div>
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-4">Top Countries</h3>
          <div className="bg-gray-50 p-4 rounded-lg">
            <ul className="divide-y divide-gray-200">
              {stats.top_countries?.map((item, index) => (
                <li key={index} className="py-2 flex justify-between">
                  <span>{item.country || 'Unknown'}</span>
                  <span className="font-semibold">{item.count}</span>
                </li>
              )) || <li className="py-2">No data available</li>}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsDisplay;
