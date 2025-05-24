import React, { useState, useEffect } from 'react';
import { createTag } from '../api/apiService';

const TagForm = ({ onTagCreated }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState('default');
  const [trigger, setTrigger] = useState('page_view');
  const [clickTarget, setClickTarget] = useState('');
  const [action, setAction] = useState('');
  const [actionValue, setActionValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [showClickTargetInput, setShowClickTargetInput] = useState(false);
  const [showActionValueInput, setShowActionValueInput] = useState(false);
  // Effect to handle showing/hiding clickTarget input based on trigger value
  useEffect(() => {
    setShowClickTargetInput(trigger === 'click');
  }, [trigger]);

  // Effect to handle showing/hiding action value input based on action
  useEffect(() => {
    setShowActionValueInput(['alert', 'log', 'redirect'].includes(action));
  }, [action]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Tag name is required');
      return;
    }

    try {
      setIsLoading(true);
      setError('');
      
      // Prepare trigger value
      let triggerValue = trigger;
      if (trigger === 'click' && clickTarget) {
        triggerValue = JSON.stringify({ type: 'click', target: clickTarget });
      }
      
      // Prepare config value
      const configValue = action ? JSON.stringify({ 
        action: action, 
        value: actionValue 
      }) : null;
      
      const result = await createTag(name, description, type, triggerValue, configValue);
      
      // Reset form
      setName('');
      setDescription('');
      setType('default');
      setTrigger('page_view');
      setClickTarget('');
      setAction('');
      setActionValue('');
      
      if (onTagCreated) {
        onTagCreated(result);
      }
    } catch (err) {
      setError('Failed to create tag');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200 border border-gray-100">
      {/* Header with Icon */}
      <div className="flex items-center mb-6">
        <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center mr-4">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
        </div>
        <div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-gray-900 via-emerald-900 to-teal-900 bg-clip-text text-transparent">
            Create New Tag
          </h2>
          <p className="text-gray-600 text-sm">Organize your content with custom tags</p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-gradient-to-r from-red-50 to-pink-50 border-l-4 border-red-500 p-4 mb-6 rounded-lg">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-red-700 font-medium">{error}</span>
          </div>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Tag Name */}
        <div className="bg-gradient-to-r from-emerald-50 to-teal-50 p-4 rounded-lg">
          <label className="block text-gray-800 text-sm font-semibold mb-3" htmlFor="name">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            Tag Name *
          </label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
            placeholder="e.g., 'blog-post', 'tutorial', 'news'..."
            required
          />
        </div>
          {/* Description */}
        <div>
          <label className="block text-gray-700 text-sm font-semibold mb-3" htmlFor="description">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
            </svg>
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm resize-none"
            placeholder="Describe what this tag is used for..."
            rows="4"
          />
        </div>

        {/* Tag Type */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg">
          <label className="block text-gray-700 text-sm font-semibold mb-3" htmlFor="tagType">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
            </svg>
            Tag Type
          </label>
          <select
            id="tagType"
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
          >
            <option value="default">Default</option>
            <option value="custom_html">Custom HTML</option>
            <option value="event">Event</option>
            <option value="conversion">Conversion</option>
          </select>
        </div>

        {/* Trigger */}
        <div className="bg-gradient-to-r from-purple-50 to-violet-50 p-4 rounded-lg">
          <label className="block text-gray-700 text-sm font-semibold mb-3" htmlFor="tagTrigger">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
            </svg>
            Trigger
          </label>
          <select
            id="tagTrigger"
            value={trigger}
            onChange={(e) => setTrigger(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
          >
            <option value="page_view">Page View</option>
            <option value="all_pages">All Pages</option>
            <option value="click">Click</option>
          </select>
        </div>

        {/* Click Target (conditional) */}
        {showClickTargetInput && (
          <div className="bg-gradient-to-r from-pink-50 to-rose-50 p-4 rounded-lg">
            <label className="block text-gray-700 text-sm font-semibold mb-3" htmlFor="clickTarget">
              <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
              </svg>
              Click Target
            </label>
            <input
              id="clickTarget"
              type="text"
              value={clickTarget}
              onChange={(e) => setClickTarget(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
              placeholder="#myId, .myClass or button[data-action='buy']"
            />
            <p className="text-xs text-gray-500 mt-2">Enter a CSS selector for the element that should trigger this tag</p>
          </div>
        )}

        {/* Action Configuration */}
        <div className="bg-gradient-to-r from-amber-50 to-yellow-50 p-4 rounded-lg">
          <label className="block text-gray-700 text-sm font-semibold mb-3" htmlFor="tagAction">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Action
          </label>
          <select
            id="tagAction"
            value={action}
            onChange={(e) => setAction(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
          >
            <option value="">No Action</option>
            <option value="alert">Show Alert</option>
            <option value="log">Console Log</option>
            <option value="redirect">Redirect</option>
          </select>
        </div>

        {/* Action Value (conditional) */}
        {showActionValueInput && (
          <div className="bg-gradient-to-r from-orange-50 to-amber-50 p-4 rounded-lg">
            <label className="block text-gray-700 text-sm font-semibold mb-3" htmlFor="actionValue">
              <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              {action === 'redirect' ? 'URL' : 'Value'}
            </label>
            <input
              id="actionValue"
              type="text"
              value={actionValue}
              onChange={(e) => setActionValue(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
              placeholder={action === 'redirect' ? 'https://example.com' : 'Enter value...'}
            />
          </div>
        )}
        
        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-semibold py-4 px-6 rounded-lg shadow-lg hover:shadow-xl transform transition-all duration-200 ${
            isLoading ? 'opacity-50 cursor-not-allowed scale-100' : 'hover:scale-105'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating Tag...
            </div>
          ) : (
            <div className="flex items-center justify-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Tag
            </div>
          )}
        </button>
      </form>

      {/* Tips Section */}
      <div className="mt-6 bg-gradient-to-r from-gray-50 to-blue-50 p-4 rounded-lg border border-gray-100">
        <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
          <svg className="w-4 h-4 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Tag Best Practices
        </h3>
        <ul className="text-xs text-gray-600 space-y-1">
          <li>• Use lowercase letters and hyphens (e.g., 'blog-post')</li>
          <li>• Keep names short and descriptive</li>
          <li>• Use consistent naming conventions</li>
          <li>• Add descriptions to help team members understand usage</li>
        </ul>
      </div>
    </div>
  );
};

export default TagForm;
