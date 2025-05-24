import React, { useState, useEffect } from 'react';
import { getTags, deleteTag } from '../api/apiService';

const TagList = ({ onRefresh, refreshFlag }) => {
  const [tags, setTags] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  const fetchTags = async () => {
    try {
      setIsLoading(true);
      const data = await getTags();
      setTags(data);
      setError('');
    } catch (err) {
      setError('Failed to fetch tags');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTags();
  }, [refreshFlag]); // Refresh when the refreshFlag changes

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this tag?')) {
      try {
        setDeletingId(id);
        await deleteTag(id);
        setTags(tags.filter(tag => tag.id !== id));
        if (onRefresh) {
          onRefresh();
        }
      } catch (err) {
        setError('Failed to delete tag');
        console.error(err);
      } finally {
        setDeletingId(null);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
        <div className="flex items-center justify-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-emerald-600"></div>
          <span className="text-gray-600 font-medium">Loading tags...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 text-red-700 p-6 mb-6 rounded-xl shadow-md">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-red-500 to-pink-500 rounded-full flex items-center justify-center">
            <span className="text-white text-sm font-semibold">!</span>
          </div>
          <span className="font-medium">{error}</span>
        </div>
      </div>
    );
  }

  if (tags.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-12 text-center">
        <div className="w-16 h-16 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-2xl">🏷️</span>
        </div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">No tags found</h3>
        <p className="text-gray-500">Create your first tag to get started organizing your visits.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-shadow duration-200">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-50 to-teal-50 border-b border-gray-100 p-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-lg flex items-center justify-center">
            <span className="text-white text-lg">🏷️</span>
          </div>
          <div>
            <h2 className="text-xl font-bold bg-gradient-to-r from-gray-900 via-emerald-900 to-teal-900 bg-clip-text text-transparent">
              Tag Library
            </h2>
            <p className="text-sm text-gray-600">Manage your visit categorization tags</p>
          </div>
        </div>
      </div>

      {/* Tags List */}
      <div className="divide-y divide-gray-100">
        {tags.map((tag, index) => (
          <div 
            key={tag.id} 
            className="p-6 hover:bg-gradient-to-r hover:from-gray-50 hover:to-emerald-50 transition-all duration-200 group"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1 min-w-0">
                {/* Tag Name */}
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-3 h-3 bg-gradient-to-r from-emerald-400 to-teal-400 rounded-full"></div>                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors duration-200">
                    {tag.name}
                  </h3>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                    #{index + 1}
                  </span>
                  {tag.type && (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 ml-2">
                      {tag.type}
                    </span>
                  )}
                </div>

                {/* Description */}
                {tag.description && (
                  <p className="text-gray-600 mb-3 pl-6 leading-relaxed">
                    {tag.description}
                  </p>
                )}
                
                {/* Trigger & Action Details */}
                <div className="flex flex-wrap gap-4 pl-6 mb-3">
                  {/* Trigger Info */}
                  {tag.trigger && (
                    <div className="flex items-center text-sm">
                      <span className="w-5 h-5 bg-purple-100 rounded-full flex items-center justify-center mr-2">
                        <svg className="w-3 h-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
                        </svg>
                      </span>
                      <span className="text-gray-700 font-medium">Trigger: </span>
                      <span className="text-gray-600 ml-1">
                        {(() => {
                          try {
                            const triggerObj = typeof tag.trigger === 'string' && tag.trigger.startsWith('{') 
                              ? JSON.parse(tag.trigger) 
                              : tag.trigger;
                            
                            if (typeof triggerObj === 'object' && triggerObj.type === 'click') {
                              return `Click on "${triggerObj.target}"`;
                            } else {
                              return typeof triggerObj === 'object' ? triggerObj.type : triggerObj;
                            }
                          } catch {
                            return tag.trigger;
                          }
                        })()}
                      </span>
                    </div>
                  )}
                  
                  {/* Action Info */}
                  {tag.config && (
                    <div className="flex items-center text-sm">
                      <span className="w-5 h-5 bg-amber-100 rounded-full flex items-center justify-center mr-2">
                        <svg className="w-3 h-3 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </span>
                      <span className="text-gray-700 font-medium">Action: </span>
                      <span className="text-gray-600 ml-1">
                        {(() => {
                          try {
                            const config = JSON.parse(tag.config);
                            if (config.action) {
                              return `${config.action}${config.value ? `: ${config.value}` : ''}`;
                            }
                            return 'None';
                          } catch {
                            return 'None';
                          }
                        })()}
                      </span>
                    </div>
                  )}
                </div>

                {/* Created Date */}
                <div className="flex items-center space-x-2 pl-6">
                  <span className="text-xs text-gray-400">📅</span>
                  <p className="text-xs text-gray-500 font-medium">
                    Created {new Date(tag.created_at).toLocaleDateString()} at {new Date(tag.created_at).toLocaleTimeString()}
                  </p>
                </div>
              </div>

              {/* Delete Button */}
              <div className="ml-6 flex-shrink-0">
                <button 
                  onClick={() => handleDelete(tag.id)} 
                  disabled={deletingId === tag.id}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 hover:text-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed group"
                  title="Delete tag"
                >
                  {deletingId === tag.id ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600 mr-2"></div>
                      Deleting...
                    </>
                  ) : (
                    <>
                      <span className="mr-2">🗑️</span>
                      Delete
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer with Tag Count */}
      <div className="bg-gradient-to-r from-gray-50 to-emerald-50 border-t border-gray-100 px-6 py-4">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">
            Total tags: <span className="font-semibold text-emerald-600">{tags.length}</span>
          </span>
          <span className="text-xs text-gray-500">
            💡 Tip: Use descriptive names for better organization
          </span>
        </div>
      </div>
    </div>
  );
};

export default TagList;
