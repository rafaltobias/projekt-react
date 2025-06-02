import React, { useState, useEffect } from 'react';
import { createTag } from '../api/apiService';
import { Tag } from '../api/types';

interface TagFormProps {
  onTagCreated?: (tag: Tag) => void;
}

const TagForm: React.FC<TagFormProps> = ({ onTagCreated }) => {
  const [name, setName] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [type, setType] = useState<string>('default');
  const [trigger, setTrigger] = useState<string>('page_view');
  const [clickTarget, setClickTarget] = useState<string>('');
  const [action, setAction] = useState<string>('');
  const [actionValue, setActionValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [showClickTargetInput, setShowClickTargetInput] = useState<boolean>(false);
  const [showActionValueInput, setShowActionValueInput] = useState<boolean>(false);
  
  // Effect to handle showing/hiding clickTarget input based on trigger value
  useEffect(() => {
    setShowClickTargetInput(trigger === 'click');
  }, [trigger]);

  // Effect to handle showing/hiding action value input based on action
  useEffect(() => {
    setShowActionValueInput(['alert', 'log', 'redirect'].includes(action));
  }, [action]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
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
            placeholder="Enter a name for your tag..."
            required
          />
        </div>
        
        {/* Description */}
        <div>
          <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="description">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
            </svg>
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
            placeholder="Optional description for this tag..."
            rows={3}
          ></textarea>
        </div>
        
        {/* Tag Type */}
        <div>
          <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="type">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            Tag Type
          </label>
          <select
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
          >
            <option value="default">Default</option>
            <option value="campaign">Campaign</option>
            <option value="feature">Feature</option>
            <option value="user">User Segment</option>
            <option value="custom">Custom</option>
          </select>
        </div>
        
        {/* Trigger Type */}
        <div>
          <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="trigger">
            <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
            </svg>
            Trigger
          </label>
          <select
            id="trigger"
            value={trigger}
            onChange={(e) => setTrigger(e.target.value)}
            className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
          >
            <option value="page_view">Page View</option>
            <option value="click">Click Event</option>
            <option value="scroll">Scroll Event</option>
            <option value="timer">Time-based</option>
          </select>
        </div>
        
        {/* Click Target - Conditional */}
        {showClickTargetInput && (
          <div>
            <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="clickTarget">
              <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
              </svg>
              Click Target CSS Selector
            </label>
            <input
              id="clickTarget"
              type="text"
              value={clickTarget}
              onChange={(e) => setClickTarget(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
              placeholder="e.g. .btn-primary, #submit-button"
            />
            <p className="mt-1 text-xs text-gray-500">CSS selector for the element that triggers this tag</p>
          </div>
        )}
        
        {/* Action Settings */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Tag Actions</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="action">
                <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Action Type
              </label>
              <select
                id="action"
                value={action}
                onChange={(e) => setAction(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
              >
                <option value="">No Action</option>
                <option value="log">Log to Console</option>
                <option value="alert">Show Alert</option>
                <option value="redirect">Redirect User</option>
                <option value="track">Track Event</option>
              </select>
            </div>
            
            {/* Action Value - Conditional */}
            {showActionValueInput && (
              <div>
                <label className="block text-gray-700 text-sm font-semibold mb-2" htmlFor="actionValue">
                  <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {action === 'redirect' ? 'Redirect URL' : 'Message'}
                </label>
                <input
                  id="actionValue"
                  type={action === 'redirect' ? 'url' : 'text'}
                  value={actionValue}
                  onChange={(e) => setActionValue(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
                  placeholder={action === 'redirect' ? 'https://example.com' : 'Enter message or value...'}
                />
              </div>
            )}
          </div>
        </div>
        
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
    </div>
  );
};

export default TagForm;
