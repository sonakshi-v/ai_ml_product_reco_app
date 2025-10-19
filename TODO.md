# TODO: AI-ML Product Recommendation Web App

## 1. Dataset Download and Processing
- [x] Create data/ directory
- [x] Download dataset from Google Drive link using gdown
- [x] Load dataset into Pandas, inspect columns and data
- [x] Clean and augment data (handle missing values, process image URLs)
- [x] Create data analytics notebook (data_analytics.ipynb) with comments

## 2. Model Training
- [x] Create notebooks/ directory
- [x] Create model_training.ipynb notebook
- [x] Implement recommendation model: Use sentence-transformers for text embeddings (title+description)
- [x] Implement NLP: Clustering with scikit-learn for similar products
- [x] Implement CV: Train ResNet or Vision Transformer for category classification on images
- [x] Implement GenAI: Use LangChain with HuggingFace model (e.g., DistilGPT-2) for creative descriptions
- [x] Evaluate models and save trained models to models/ directory

## 3. Vector Database Setup
- [x] Initialize Pinecone index
- [x] Store text embeddings in Pinecone for semantic search
- [x] Test retrieval functionality

## 4. Backend Enhancements
- [x] Update backend/requirements.txt with pinecone-client, langchain, huggingface_hub, etc.
- [x] Implement chat endpoint in recommendations.py: Process prompt, query Pinecone, generate descriptions
- [x] Add analytics endpoint: Return dataset stats using Pandas/SQLite
- [x] Ensure images load from dataset URLs (or use placeholders)

## 5. Frontend Development
- [x] Update frontend/package.json with Chart.js for analytics
- [x] Create frontend/src/pages/ directory
- [x] Build Chat page: Conversational interface for recommendations
- [x] Build Analytics page: Display charts and stats
- [x] Implement React Router for navigation between pages

## 6. Integration and Testing
- [x] Run backend and frontend locally
- [x] Test end-to-end flow: Send prompt, get recommendations with images and descriptions
- [x] Ensure recommendations are relevant to user requests
- [x] Test analytics page

## 7. Notebooks and Docs
- [x] Finalize data_analytics.ipynb and model_training.ipynb with detailed comments
- [x] Write README.md with setup, usage, and environment requirements
- [x] Ensure all components work together

## 8. Bug Fixes and Improvements
- [x] Fix image URL parsing: Extract first image from image lists
- [x] Fix price display: Handle null/None prices properly in frontend
- [x] Improve search algorithm: Better scoring for substring matches
- [x] Test image loading: Verify Amazon URLs are accessible
- [x] End-to-end testing: Confirm all functionality works
