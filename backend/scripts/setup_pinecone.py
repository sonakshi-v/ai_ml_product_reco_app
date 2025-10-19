import os
import pandas as pd
import numpy as np
import pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_pinecone():
    # Load environment variables
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_env = os.getenv('PINECONE_ENVIRONMENT', 'gcp-starter')

    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY not found in environment variables")

    # Initialize Pinecone
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    logger.info("Pinecone initialized")

    # Define index name and dimension
    index_name = "furniture-recommendations"
    dimension = 384  # all-MiniLM-L6-v2 dimension

    # Create index if it doesn't exist
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            pods=1,
            replicas=1
        )
        logger.info(f"Created Pinecone index: {index_name}")
    else:
        logger.info(f"Pinecone index {index_name} already exists")

    # Connect to index
    index = pinecone.Index(index_name)

    # Load dataset
    df_path = '../data/furniture_dataset_final.csv'
    if not os.path.exists(df_path):
        df_path = '../data/furniture_dataset_cleaned.csv'
        if not os.path.exists(df_path):
            raise FileNotFoundError("Dataset not found")

    df = pd.read_csv(df_path)
    logger.info(f"Loaded dataset with {len(df)} products")

    # Load or create embeddings
    embeddings_path = '../models/text_embeddings.npy'
    if os.path.exists(embeddings_path):
        embeddings = np.load(embeddings_path)
        logger.info(f"Loaded embeddings from {embeddings_path}")
    else:
        # Generate embeddings
        logger.info("Generating embeddings...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        df['text_for_embedding'] = df['title'].fillna('') + '. ' + df['description'].fillna('')
        embeddings = model.encode(df['text_for_embedding'].tolist(), show_progress_bar=True)
        np.save(embeddings_path, embeddings)
        logger.info(f"Generated and saved embeddings to {embeddings_path}")

    # Prepare vectors for Pinecone
    vectors = []
    for i, row in df.iterrows():
        # Clean metadata
        metadata = {
            "title": str(row['title']) if pd.notnull(row['title']) else "",
            "description": str(row['description']) if pd.notnull(row['description']) else "",
            "price": float(row['price']) if pd.notnull(row['price']) else 0.0,
            "brand": str(row['brand']) if pd.notnull(row['brand']) else "",
            "categories": str(row['categories']) if pd.notnull(row['categories']) else "",
            "image": str(row['images']) if pd.notnull(row['images']) else "",
        }

        vector = {
            "id": str(row['uniq_id']),
            "values": embeddings[i].tolist(),
            "metadata": metadata
        }
        vectors.append(vector)

    # Upload vectors in batches
    batch_size = 100
    total_batches = (len(vectors) + batch_size - 1) // batch_size

    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        try:
            index.upsert(vectors=batch)
            logger.info(f"Uploaded batch {i//batch_size + 1}/{total_batches}")
        except Exception as e:
            logger.error(f"Error uploading batch {i//batch_size + 1}: {e}")
            continue

    # Verify upload
    stats = index.describe_index_stats()
    logger.info(f"Index stats: {stats}")

    logger.info("Pinecone setup completed successfully!")

if __name__ == "__main__":
    setup_pinecone()
