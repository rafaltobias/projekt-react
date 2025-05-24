import React from 'react';
import StatsDisplay from '../components/StatsDisplay';

const StatsPage = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Visit Statistics</h1>
      <StatsDisplay />
    </div>
  );
};

export default StatsPage;
