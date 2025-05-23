import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ChartBarIcon, TagIcon, EyeIcon } from '@heroicons/react/24/outline';
import Dashboard from './pages/Dashboard';
import Statistics from './pages/Statistics';
import Tags from './pages/Tags';
import Visits from './pages/Visits';
import './App.css';

const navigation = [
  { name: 'Dashboard', href: '/', icon: ChartBarIcon },
  { name: 'Statistics', href: '/statistics', icon: ChartBarIcon },
  { name: 'Visits', href: '/visits', icon: EyeIcon },
  { name: 'Tags', href: '/tags', icon: TagIcon },
];

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900">Analytics Dashboard</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  {navigation.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        className="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm inline-flex items-center"
                      >
                        <Icon className="h-5 w-5 mr-2" />
                        {item.name}
                      </Link>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/statistics" element={<Statistics />} />
              <Route path="/visits" element={<Visits />} />
              <Route path="/tags" element={<Tags />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
