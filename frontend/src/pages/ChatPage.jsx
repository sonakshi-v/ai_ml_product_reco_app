import { useState } from 'react';
import axios from 'axios';
import './ChatPage.css';

const API_BASE_URL = 'https://ai-ml-product-reco-app.onrender.com/api';

function ChatPage() {
  const [message, setMessage] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/recommendations/chat`, {
        message: message,
        top_k: 5
      });

      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-header">
          <h2>Find Your Perfect Furniture</h2>
          <p>Describe what you're looking for and get personalized recommendations!</p>
        </div>

        <form onSubmit={handleSubmit} className="chat-form">
          <div className="input-group">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="e.g., I need a comfortable chair for my home office..."
              rows="3"
              className="chat-input"
            />
            <button
              type="submit"
              disabled={loading || !message.trim()}
              className="chat-submit"
            >
              {loading ? 'Searching...' : 'Get Recommendations'}
            </button>
          </div>
        </form>

        {error && <div className="error-message">{error}</div>}

        <div className="recommendations">
          {recommendations.map((product) => (
            <div key={product.uniq_id} className="product-card">
              <div className="product-image">
                {product.image ? (
                  <img
                    src={product.image}
                    alt={product.title}
                    onError={(e) => {
                      e.target.src = '/placeholder-image.png';
                    }}
                  />
                ) : (
                  <div className="no-image">No Image</div>
                )}
              </div>
              <div className="product-info">
                <h3 className="product-title">{product.title}</h3>
                <p className="product-description">
                  {product.description && product.description.length > 150
                    ? `${product.description.substring(0, 150)}...`
                    : product.description}
                </p>
                {product.price !== null && product.price !== undefined && (
                  <p className="product-price">${product.price.toFixed(2)}</p>
                )}
                {product.categories && product.categories.length > 0 && (
                  <div className="product-categories">
                    {product.categories.slice(0, 3).map((cat, idx) => (
                      <span key={idx} className="category-tag">{cat}</span>
                    ))}
                  </div>
                )}
                {product.score && (
                  <p className="product-score">Match: {(product.score * 100).toFixed(1)}%</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
