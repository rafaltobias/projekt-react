import React, { useState } from 'react';
import { trackVisit } from '../api/apiService';

const VisitTracker = ({ onVisitTracked }) => {
  const [pageUrl, setPageUrl] = useState('');
  const [browser, setBrowser] = useState('');
  const [os, setOs] = useState('');
  const [device, setDevice] = useState('');
  const [country, setCountry] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [isEntryPage, setIsEntryPage] = useState(false);
  const [isExitPage, setIsExitPage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!pageUrl.trim()) {
      setError('Page URL is required');
      return;
    }

    try {
      setIsLoading(true);
      setError('');
      setSuccess('');
      
      const result = await trackVisit(
        pageUrl,
        browser || null,
        os || null,
        device || null,
        country || null,
        sessionId || null,
        isEntryPage,
        isExitPage
      );
      
      setSuccess('Visit tracked successfully!');
      setPageUrl('');
      setBrowser('');
      setOs('');
      setDevice('');
      setCountry('');
      setSessionId('');
      setIsEntryPage(false);
      setIsExitPage(false);
      
      if (onVisitTracked) {
        onVisitTracked(result);
      }
    } catch (err) {
      setError('Failed to track visit');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Track Visit</h2>
      
      {error && <div className="bg-red-100 text-red-700 p-2 mb-4 rounded">{error}</div>}
      {success && <div className="bg-green-100 text-green-700 p-2 mb-4 rounded">{success}</div>}
        <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="pageUrl">
            Page URL*
          </label>
          <input
            id="pageUrl"
            type="url"
            value={pageUrl}
            onChange={(e) => setPageUrl(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="https://example.com"
            required
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="browser">
              Browser
            </label>
            <input
              id="browser"
              type="text"
              value={browser}
              onChange={(e) => setBrowser(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Chrome, Firefox, etc."
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="os">
              Operating System
            </label>
            <input
              id="os"
              type="text"
              value={os}
              onChange={(e) => setOs(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Windows, MacOS, etc."
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="device">
              Device
            </label>
            <input
              id="device"
              type="text"
              value={device}
              onChange={(e) => setDevice(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Desktop, Mobile, etc."
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="country">
              Country
            </label>
            <input
              id="country"
              type="text"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="US, UK, etc."
            />
          </div>
        </div>
          <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="sessionId">
            Session ID
          </label>
          <input
            id="sessionId"
            type="text"
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Unique session identifier"
          />
        </div>
        
        <div className="flex space-x-4 mb-4">
          <div className="flex items-center">
            <input
              id="isEntryPage"
              type="checkbox"
              checked={isEntryPage}
              onChange={(e) => setIsEntryPage(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="isEntryPage" className="ml-2 text-sm font-medium text-gray-700">
              Is Entry Page
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              id="isExitPage"
              type="checkbox"
              checked={isExitPage}
              onChange={(e) => setIsExitPage(e.target.checked)}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="isExitPage" className="ml-2 text-sm font-medium text-gray-700">
              Is Exit Page
            </label>
          </div>
        </div>
        
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${
            isLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? 'Tracking...' : 'Track Visit'}
        </button>
      </form>
    </div>
  );
};

export default VisitTracker;
