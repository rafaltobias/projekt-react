import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import StatsPage from './pages/StatsPage';
import TagsPage from './pages/TagsPage';
import TrackingPage from './pages/TrackingPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/track" element={<TrackingPage />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="/tags" element={<TagsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
