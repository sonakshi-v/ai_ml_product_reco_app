# AI-ML Product Recommendation Web App

A comprehensive furniture recommendation system that uses AI/ML to provide personalized product recommendations with creative descriptions and analytics.

## Features

- **Conversational Recommendations**: Chat-based interface for finding furniture based on user descriptions
- **AI-Powered Descriptions**: Creative product descriptions generated using GenAI
- **Image Classification**: CV models for categorizing furniture products
- **Semantic Search**: Vector database for efficient product retrieval
- **Analytics Dashboard**: Comprehensive data insights and visualizations
- **NLP Clustering**: Grouping similar products using text analysis

## Tech Stack

### Backend
- **FastAPI**: High-performance web framework
- **Pinecone**: Vector database for semantic search
- **SentenceTransformers**: Text embeddings for recommendations
- **LangChain**: Framework for GenAI integration
- **HuggingFace Transformers**: Pre-trained models for text generation and CV
- **Scikit-learn**: Machine learning algorithms

### Frontend
- **React**: User interface framework
- **React Router**: Client-side routing
- **Chart.js**: Data visualization
- **Axios**: HTTP client for API calls

## Project Structure

```
ai_ml_product_reco_app/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic models
│   │   └── routers/
│   │       ├── recommendations.py # Recommendation endpoints
│   │       └── analytics.py     # Analytics endpoints
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React app
│   │   ├── App.css              # Global styles
│   │   ├── main.jsx             # App entry point
│   │   └── pages/
│   │       ├── ChatPage.jsx     # Recommendation chat interface
│   │       ├── ChatPage.css     # Chat page styles
│   │       ├── AnalyticsPage.jsx # Analytics dashboard
│   │       └── AnalyticsPage.css # Analytics page styles
│   ├── package.json             # Node dependencies
│   └── vite.config.js           # Vite configuration
├── data/                        # Dataset storage
├── models/                      # Trained model artifacts
├── notebooks/                   # Jupyter notebooks
│   ├── data_analytics.ipynb     # Data exploration and cleaning
│   └── model_training.ipynb     # Model training and evaluation
└── README.md                    # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Pinecone account (optional, fallback available)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional):**
   Create a `.env` file in the backend directory:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

5. **Run data analytics notebook:**
   ```bash
   cd ../notebooks
   jupyter notebook data_analytics.ipynb
   ```
   Run all cells to process and clean the dataset.

6. **Run model training notebook:**
   ```bash
   jupyter notebook model_training.ipynb
   ```
   Run all cells to train models and generate embeddings.

7. **Start the backend server:**
   ```bash
   cd ../backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   Navigate to `http://localhost:5173`

## API Endpoints

### Recommendations
- `POST /api/recommendations/chat`: Get product recommendations based on user query
  - Request: `{"message": "I need a comfortable office chair", "top_k": 5}`
  - Response: List of recommended products with descriptions and scores

### Analytics
- `GET /api/analytics/summary`: Dataset summary statistics
- `GET /api/analytics/price-distribution`: Price distribution data
- `GET /api/analytics/top-brands`: Top brands by product count
- `GET /api/analytics/top-categories`: Top categories by frequency
- `GET /api/analytics/material-distribution`: Material usage statistics
- `GET /api/analytics/color-distribution`: Color distribution
- `GET /api/analytics/country-origin`: Country of origin statistics
- `GET /api/analytics/price-by-category`: Average price by category

## Model Details

### Recommendation System
- **Text Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Similarity Search**: Cosine similarity on text embeddings
- **Vector Database**: Pinecone for scalable semantic search
- **Clustering**: K-means for grouping similar products

### Computer Vision
- **Model**: Vision Transformer (ViT) for image classification
- **Task**: Automatic categorization of furniture images

### Generative AI
- **Model**: DistilGPT-2 via LangChain
- **Task**: Creative product description generation

## Usage

1. **Chat Interface**: Describe your furniture needs in natural language
2. **Get Recommendations**: Receive personalized product suggestions with AI-generated descriptions
3. **View Analytics**: Explore dataset insights through interactive charts and statistics
4. **Browse Products**: See product images, prices, categories, and match scores

## Development Notes

- The system includes fallback mechanisms for when Pinecone is not available
- Models are loaded on startup for optimal performance
- Error handling is implemented throughout the application
- The frontend is responsive and works on mobile devices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
