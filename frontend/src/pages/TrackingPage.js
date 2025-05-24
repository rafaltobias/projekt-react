import React, { useState } from 'react';
import VisitTracker from '../components/VisitTracker';

const TrackingPage = () => {
  const [visitCount, setVisitCount] = useState(0);

  const handleVisitTracked = () => {
    setVisitCount(prev => prev + 1);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Track Visits</h1>
      
      {visitCount > 0 && (
        <div className="bg-green-100 text-green-800 p-4 mb-6 rounded-md">
          <p className="font-medium">You've tracked {visitCount} visit{visitCount !== 1 ? 's' : ''} in this session!</p>
        </div>
      )}
      
      <div className="max-w-md mx-auto">
        <VisitTracker onVisitTracked={handleVisitTracked} />
      </div>
    </div>
  );
};

export default TrackingPage;
