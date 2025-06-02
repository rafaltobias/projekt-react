import React from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <Navbar />
      <main className="py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
      <footer className="bg-gradient-to-r from-gray-800 via-gray-900 to-black text-white">
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h3 className="text-lg font-semibold text-blue-400">Visit Tracker</h3>
              <p className="text-gray-400 text-sm">Professional website analytics solution</p>
            </div>
            <div className="text-gray-400 text-sm">
              © {new Date().getFullYear()} Visit Tracker. All rights reserved.
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-gray-700 text-center text-gray-500 text-xs">
            <p>Built with React • Powered by modern analytics</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
