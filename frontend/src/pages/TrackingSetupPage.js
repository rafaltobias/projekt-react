import React, { useState, useEffect } from 'react';

const TrackingSetupPage = () => {
  const [copySuccess, setCopySuccess] = useState('');

  const trackingCode = `<script async src="http://localhost:5000/static/tracker.min.js"></script>`;
  
  const customEventExample = `// Track custom events
VisitTracker.trackEvent('button_click', { 
  id: 'signup-button', 
  label: 'Sign Up',
  timestamp: new Date().toISOString()
});`;

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopySuccess('Copied!');
      setTimeout(() => setCopySuccess(''), 2000);
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-6">
              Automatic Website Tracking Setup
            </h1>
            
            <div className="prose max-w-none">
              <p className="text-lg text-gray-600 mb-8">
                Set up automatic visitor tracking on your website similar to Google Analytics. 
                Our tracking script automatically collects visitor data including browser information, 
                device type, location, and user behavior.
              </p>

              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-8">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-blue-700">
                      <strong>Features:</strong> Automatic pageview tracking, session management, 
                      browser/OS/device detection, entry/exit page tracking, custom event tracking, 
                      and real-time analytics.
                    </p>
                  </div>
                </div>
              </div>

              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Quick Setup</h2>
              
              <p className="mb-4">
                Add the following tracking code to the <code>&lt;head&gt;</code> section of your website:
              </p>

              <div className="relative">
                <pre className="bg-gray-800 text-white p-4 rounded-lg overflow-x-auto">
                  <code>{trackingCode}</code>
                </pre>
                <button
                  onClick={() => copyToClipboard(trackingCode)}
                  className="absolute top-2 right-2 bg-gray-600 hover:bg-gray-500 text-white px-3 py-1 rounded text-sm"
                >
                  Copy
                </button>
                {copySuccess && (
                  <span className="absolute top-2 right-20 text-green-400 text-sm">
                    {copySuccess}
                  </span>
                )}
              </div>

              <h2 className="text-2xl font-semibold text-gray-900 mb-4 mt-8">What Gets Tracked</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">Automatic Data Collection</h3>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Page URLs and titles</li>
                    <li>• Referrer information</li>
                    <li>• Browser type and version</li>
                    <li>• Operating system</li>
                    <li>• Device type (desktop/mobile/tablet)</li>
                    <li>• Session management</li>
                    <li>• Entry and exit pages</li>
                    <li>• Geographic location (IP-based)</li>
                  </ul>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">Privacy Features</h3>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• No cookies required</li>
                    <li>• Session-based tracking only</li>
                    <li>• No personal data collection</li>
                    <li>• GDPR compliant</li>
                    <li>• Lightweight script (&lt;5KB)</li>
                    <li>• Non-blocking async loading</li>
                  </ul>
                </div>
              </div>

              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Custom Event Tracking</h2>
              
              <p className="mb-4">
                Track custom user interactions and events:
              </p>

              <div className="relative">
                <pre className="bg-gray-800 text-white p-4 rounded-lg overflow-x-auto">
                  <code>{customEventExample}</code>
                </pre>
                <button
                  onClick={() => copyToClipboard(customEventExample)}
                  className="absolute top-2 right-2 bg-gray-600 hover:bg-gray-500 text-white px-3 py-1 rounded text-sm"
                >
                  Copy
                </button>
              </div>

              <h2 className="text-2xl font-semibold text-gray-900 mb-4 mt-8">Live Demo</h2>
              
              <p className="mb-4">
                See the tracking in action with our demo page:
              </p>

              <div className="flex space-x-4">
                <a
                  href="http://localhost:5000/tracking-example"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  View Demo Page
                  <svg className="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </a>
                
                <a
                  href="/stats"
                  className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  View Analytics Dashboard
                </a>
              </div>

              <h2 className="text-2xl font-semibold text-gray-900 mb-4 mt-8">Integration Examples</h2>
              
              <div className="space-y-4">
                <details className="bg-gray-50 p-4 rounded-lg">
                  <summary className="cursor-pointer font-semibold text-gray-900">
                    HTML Website
                  </summary>
                  <pre className="mt-2 bg-gray-800 text-white p-3 rounded text-sm overflow-x-auto">
{`<!DOCTYPE html>
<html>
<head>
  <title>My Website</title>
  <script async src="http://localhost:5000/static/tracker.min.js"></script>
</head>
<body>
  <!-- Your content -->
</body>
</html>`}
                  </pre>
                </details>

                <details className="bg-gray-50 p-4 rounded-lg">
                  <summary className="cursor-pointer font-semibold text-gray-900">
                    React Application
                  </summary>
                  <pre className="mt-2 bg-gray-800 text-white p-3 rounded text-sm overflow-x-auto">
{`// In your public/index.html
<script async src="http://localhost:5000/static/tracker.min.js"></script>

// Or dynamically load in a component
useEffect(() => {
  const script = document.createElement('script');
  script.src = 'http://localhost:5000/static/tracker.min.js';
  script.async = true;
  document.head.appendChild(script);
}, []);`}
                  </pre>
                </details>

                <details className="bg-gray-50 p-4 rounded-lg">
                  <summary className="cursor-pointer font-semibold text-gray-900">
                    WordPress
                  </summary>
                  <pre className="mt-2 bg-gray-800 text-white p-3 rounded text-sm overflow-x-auto">
{`// Add to your theme's functions.php
function add_visit_tracker() {
    echo '<script async src="http://localhost:5000/static/tracker.min.js"></script>';
}
add_action('wp_head', 'add_visit_tracker');`}
                  </pre>
                </details>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrackingSetupPage;
