import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import AnalyticsPage from './pages/AnalyticsPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">🛋️ Furniture Recommender</h1>
            <div className="nav-links">
              <Link to="/" className="nav-link">Chat</Link>
              <Link to="/analytics" className="nav-link">Analytics</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
