import React from 'react';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="py-4">
        {children}
      </main>
      <footer className="bg-gray-800 text-white text-center p-4 mt-12">
        <p>Visit Tracker © {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
};

export default Layout;
