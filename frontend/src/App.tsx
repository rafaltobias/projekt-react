import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Layout from './components/Layout';
import ConsentPopup from './components/ConsentPopup';
import HomePage from './pages/HomePage';
import StatsPage from './pages/StatsPage';
import TagsPage from './pages/TagsPage';
import TrackingPage from './pages/TrackingPage';
import TrackingSetupPage from './pages/TrackingSetupPage';
import AnalyticsPage from './pages/AnalyticsPage';
import '../src/static/tag-manager';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/track" element={<TrackingPage />} />
          <Route path="/setup" element={<TrackingSetupPage />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/tags" element={<TagsPage />} />
        </Routes>
      </Layout>
      <ConsentPopup />
    </Router>
  );
};

export default App;
