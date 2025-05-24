import React, { useState, useEffect } from 'react';
import { getTags, deleteTag } from '../api/apiService';

const TagList = ({ onRefresh, refreshFlag }) => {
  const [tags, setTags] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

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
        await deleteTag(id);
        setTags(tags.filter(tag => tag.id !== id));
        if (onRefresh) {
          onRefresh();
        }
      } catch (err) {
        setError('Failed to delete tag');
        console.error(err);
      }
    }
  };

  if (isLoading) {
    return <div className="text-center py-4">Loading tags...</div>;
  }

  if (error) {
    return <div className="bg-red-100 text-red-700 p-4 mb-4 rounded">{error}</div>;
  }

  if (tags.length === 0) {
    return <div className="text-center py-4 text-gray-500">No tags found. Create a tag to get started.</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <h2 className="text-xl font-semibold p-4 border-b">Tags</h2>
      <ul>
        {tags.map(tag => (
          <li key={tag.id} className="border-b last:border-b-0 p-4 flex justify-between items-center">
            <div>
              <h3 className="font-medium">{tag.name}</h3>
              {tag.description && <p className="text-sm text-gray-600 mt-1">{tag.description}</p>}
              <p className="text-xs text-gray-500 mt-2">Created: {new Date(tag.created_at).toLocaleString()}</p>
            </div>
            <button 
              onClick={() => handleDelete(tag.id)} 
              className="ml-4 text-red-500 hover:text-red-700 focus:outline-none"
              title="Delete tag"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TagList;
