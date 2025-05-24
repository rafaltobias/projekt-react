import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Visit Tracker</h1>
        <p className="text-xl text-gray-600">Track and analyze website visits with ease</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-4">Track Visits</h2>
          <p className="text-gray-600 mb-6">Record visits to your websites. Add optional tags for better organization.</p>
          <Link 
            to="/track" 
            className="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Start Tracking
          </Link>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-4">View Statistics</h2>
          <p className="text-gray-600 mb-6">Visualize and analyze your visit data with interactive charts and graphs.</p>
          <Link 
            to="/stats" 
            className="inline-block bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            View Stats
          </Link>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
          <h2 className="text-2xl font-semibold mb-4">Manage Tags</h2>
          <p className="text-gray-600 mb-6">Create and organize tags to categorize and segment your visit data.</p>
          <Link 
            to="/tags" 
            className="inline-block bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
          >
            Manage Tags
          </Link>
        </div>
      </div>
      
      <div className="mt-16 text-center">
        <h2 className="text-2xl font-semibold mb-4">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 max-w-5xl mx-auto">
          <div className="bg-gray-50 p-4 rounded">
            <h3 className="font-bold mb-2">Visit Tracking</h3>
            <p className="text-sm text-gray-600">Record and store visit information</p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <h3 className="font-bold mb-2">Tag Management</h3>
            <p className="text-sm text-gray-600">Organize visits with custom tags</p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <h3 className="font-bold mb-2">Visual Analytics</h3>
            <p className="text-sm text-gray-600">Visualize data with charts</p>
          </div>
          <div className="bg-gray-50 p-4 rounded">
            <h3 className="font-bold mb-2">Data Export</h3>
            <p className="text-sm text-gray-600">Export statistics as CSV</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
