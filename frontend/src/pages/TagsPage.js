import React, { useState } from 'react';
import TagForm from '../components/TagForm';
import TagList from '../components/TagList';

const TagsPage = () => {
  const [refreshFlag, setRefreshFlag] = useState(0);

  const handleTagCreated = () => {
    // Trigger refresh of the tag list
    setRefreshFlag(prev => prev + 1);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Manage Tags</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <TagForm onTagCreated={handleTagCreated} />
        </div>
        
        <div className="md:col-span-2">
          <TagList refreshFlag={refreshFlag} onRefresh={handleTagCreated} />
        </div>
      </div>
    </div>
  );
};

export default TagsPage;
