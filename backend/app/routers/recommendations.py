from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Product
import pandas as pd
import numpy as np
import os
# from sentence_transformers import SentenceTransformer  # Removed due to torch dependency issues
import pinecone
# from langchain.llms import HuggingFacePipeline  # LangChain API changed
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
from transformers import pipeline
import joblib
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# Global variables for models
sentence_model = None
kmeans_model = None
pinecone_index = None
description_chain = None
df = None

def init_models():
    global sentence_model, kmeans_model, pinecone_index, description_chain, df

    try:
        # Load dataset - try multiple paths
        dataset_paths = ['data/furniture_dataset_final.csv', '../data/furniture_dataset_final.csv',
                        'data/furniture_dataset_cleaned.csv', '../data/furniture_dataset_cleaned.csv']

        for path in dataset_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                logger.info(f"Loaded dataset from {path} with {len(df)} products")
                break
        else:
            raise FileNotFoundError("No dataset file found")

        # Initialize sentence transformer (commented out due to torch issues)
        # sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Load K-means model if exists
        # if os.path.exists('models/kmeans_model.pkl'):
        #     kmeans_model = joblib.load('models/kmeans_model.pkl')

        # Initialize Pinecone (you'll need to set environment variables)
        pinecone_api_key = os.getenv('PINECONE_API_KEY')
        pinecone_env = os.getenv('PINECONE_ENVIRONMENT', 'gcp-starter')

        if pinecone_api_key:
            pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
            index_name = "furniture-recommendations"
            if index_name in pinecone.list_indexes():
                pinecone_index = pinecone.Index(index_name)
                logger.info("Pinecone index connected")
            else:
                logger.warning("Pinecone index not found. Using fallback search.")
        else:
            logger.warning("Pinecone API key not set. Using fallback search.")

        # Initialize GenAI for descriptions (simplified)
        # description_chain = "placeholder"  # Simplified for now

        logger.info("Models initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing models: {e}")
        # Fallback: ensure df is loaded
        if df is None:
            for path in dataset_paths:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    logger.info(f"Fallback: Loaded dataset from {path}")
                    break

# Initialize models on startup
init_models()

def generate_creative_description(title, original_desc):
    """Generate a creative description by enhancing the original to 20-30 words"""
    if not original_desc:
        return f"Discover the elegance of this {title}. A beautiful furniture piece perfect for enhancing your living space."

    # Simple enhancement without ML - aim for 20-30 words
    enhancements = [
        "Discover the elegance of this",
        "Experience the comfort and style of this",
        "Transform your space with this beautiful",
        "Add sophistication to your home with this"
    ]

    enhancement = enhancements[hash(title) % len(enhancements)]

    # Create a concise description
    creative_desc = f"{enhancement} {title}. {original_desc}"

    # Add brief descriptive content to reach 20-30 words
    if len(creative_desc.split()) < 20:
        additions = [
            " This modern piece combines elegant design with functional appeal, perfect for contemporary spaces.",
            " Crafted with care, it offers both style and practicality for everyday use.",
            " A versatile furniture item that brings comfort and elegance to any room.",
            " Designed to enhance your decor with timeless style and quality craftsmanship."
        ]
        addition = additions[hash(title) % len(additions)]
        creative_desc += addition

    # Ensure it's not too long - truncate to ~30 words
    words = creative_desc.split()
    if len(words) > 30:
        creative_desc = ' '.join(words[:30]) + '...'

    return creative_desc

def search_similar_products(query, top_k=5):
    """Search for similar products using text matching"""
    if df is None:
        return []

    # Simple fallback: search by title and description text matching
    query_lower = query.lower()
    import re
    query_words = set(re.findall(r'\w+', query_lower))

    matches = []

    for idx, row in df.iterrows():
        title = str(row['title']).lower() if pd.notnull(row['title']) else ""
        description = str(row['description']).lower() if pd.notnull(row['description']) else ""

        # Count matching words
        title_words = set(re.findall(r'\w+', title))
        desc_words = set(re.findall(r'\w+', description))

        title_matches = len(query_words.intersection(title_words))
        desc_matches = len(query_words.intersection(desc_words))

        # Calculate score - prioritize exact matches and word frequency
        score = (title_matches * 3 + desc_matches) / max(len(query_words), 1)

        # Boost score for products that contain the entire query as substring
        if query_lower in title or query_lower in description:
            score *= 2

        # Normalize score to be between 0 and 1 for percentage display
        score = min(score / 10.0, 1.0)  # Assuming max reasonable score is 10

        if score > 0:
            matches.append({
                'idx': idx,
                'score': score,
                'row': row
            })

    # Sort by score and take top_k
    matches.sort(key=lambda x: x['score'], reverse=True)
    if top_k <= 0:
        top_matches = matches  # Return all matches if top_k <= 0
    else:
        top_matches = matches[:top_k]

    recommendations = []
    for match in top_matches:
        row = match['row']
        creative_desc = generate_creative_description(row['title'], row['description'])

        # Clean price - convert to float if possible
        price = None
        if pd.notnull(row['price']) and str(row['price']).strip():
            try:
                # Remove currency symbols and convert
                price_str = str(row['price']).replace('$', '').replace(',', '').strip()
                if price_str:
                    price = float(price_str)
            except (ValueError, TypeError):
                price = None

        # Parse categories
        categories = []
        if pd.notnull(row['categories']):
            cat_str = str(row['categories'])
            if cat_str.startswith('[') and cat_str.endswith(']'):
                try:
                    categories = eval(cat_str)
                except:
                    categories = [cat.strip() for cat in cat_str.strip('[]').split(',') if cat.strip()]
            else:
                categories = [cat.strip() for cat in cat_str.split(',') if cat.strip()]

        # Parse images - extract first image URL from list
        image_url = None
        if pd.notnull(row['images']):
            img_str = str(row['images']).strip()
            if img_str.startswith('[') and img_str.endswith(']'):
                try:
                    img_list = eval(img_str)
                    if img_list and len(img_list) > 0:
                        image_url = img_list[0].strip().strip("'\"")
                except:
                    # Fallback: try to extract URL from string
                    import re
                    urls = re.findall(r'https?://[^\s\'"]+', img_str)
                    if urls:
                        image_url = urls[0]
            else:
                # Single URL
                image_url = img_str.strip().strip("'\"")

        product = Product(
            uniq_id=str(row['uniq_id']),
            title=str(row['title']) if pd.notnull(row['title']) else "",
            description=creative_desc,
            price=price,
            categories=categories,
            image=image_url,
            score=float(match['score'])
        )
        recommendations.append(product)

    return recommendations

@router.post("/chat", response_model=ChatResponse)
def chat_recommendations(payload: ChatRequest):
    try:
        if df is None:
            raise HTTPException(status_code=500, detail="Dataset not loaded")

        recommendations = search_similar_products(payload.message, payload.top_k)

        return ChatResponse(query=payload.message, recommendations=recommendations)

    except Exception as e:
        logger.error(f"Error in chat_recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
