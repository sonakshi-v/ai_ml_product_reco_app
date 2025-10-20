from fastapi import APIRouter, HTTPException
import pandas as pd
from typing import Dict, Any, List
import json

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Global variable for dataset
df = None

def load_dataset():
    global df
    if df is None:
        dataset_paths = [
            '../data/furniture_dataset_processed.csv',
            'data/furniture_dataset_processed.csv',
            '../data/furniture_dataset_cleaned.csv',
            'data/furniture_dataset_cleaned.csv'
        ]
        for path in dataset_paths:
            try:
                df = pd.read_csv(path)
                print(f"Loaded dataset from {path} with {len(df)} products")
                break
            except FileNotFoundError:
                continue
        else:
            raise HTTPException(status_code=404, detail="Dataset not found")

load_dataset()

@router.get("/summary")
def get_dataset_summary() -> Dict[str, Any]:
    """Get basic dataset statistics"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    # Use cleaned_price column if available, otherwise clean price column
    df_clean = df.copy()
    if 'cleaned_price' in df_clean.columns:
        df_clean['price'] = df_clean['cleaned_price']
    else:
        df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    df_clean = df_clean.dropna(subset=['price'])

    summary = {
        "total_products": len(df),
        "unique_brands": df['brand'].nunique(),
        "unique_materials": df['material'].nunique(),
        "unique_colors": df['color'].nunique(),
        "price_range": {
            "min": float(df_clean['price'].min()) if not df_clean.empty else 0.0,
            "max": float(df_clean['price'].max()) if not df_clean.empty else 0.0,
            "mean": float(df_clean['price'].mean()) if not df_clean.empty else 0.0,
            "median": float(df_clean['price'].median()) if not df_clean.empty else 0.0
        },
        "products_with_images": int(df['images'].notnull().sum()),
        "image_percentage": float(df['images'].notnull().sum() / len(df) * 100)
    }
    return summary

@router.get("/price-distribution")
def get_price_distribution(bins: int = 20) -> Dict[str, Any]:
    """Get price distribution data"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    # Use cleaned_price column if available, otherwise clean price column
    df_clean = df.copy()
    if 'cleaned_price' in df_clean.columns:
        df_clean['price'] = df_clean['cleaned_price']
    else:
        df_clean['price'] = pd.to_numeric(df_clean['price'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
    df_clean = df_clean.dropna(subset=['price'])

    if df_clean.empty:
        return {"bins": [], "counts": [], "labels": []}

    hist, bin_edges = pd.cut(df_clean['price'], bins=bins, retbins=True)
    distribution = hist.value_counts().sort_index()

    return {
        "bins": [f"${edge:.2f}" for edge in bin_edges],
        "counts": distribution.values.tolist(),
        "labels": [f"${bin_edges[i]:.0f}-${bin_edges[i+1]:.0f}" for i in range(len(bin_edges)-1)]
    }

@router.get("/top-brands")
def get_top_brands(limit: int = 10) -> List[Dict[str, Any]]:
    """Get top brands by product count"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    brand_counts = df['brand'].value_counts().head(limit)
    return [{"brand": brand, "count": int(count)} for brand, count in brand_counts.items()]

@router.get("/top-categories")
def get_top_categories(limit: int = 15) -> List[Dict[str, Any]]:
    """Get top categories by frequency"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    all_categories = []
    for idx, row in df.iterrows():
        cats = row['categories']
        if isinstance(cats, str):
            # Try to parse string representation of list
            if cats.startswith('[') and cats.endswith(']'):
                try:
                    parsed_cats = eval(cats)
                    all_categories.extend(parsed_cats)
                except:
                    # If eval fails, split by comma
                    all_categories.extend([cat.strip().strip("'\"") for cat in cats.strip('[]').split(',') if cat.strip()])
            else:
                all_categories.extend([cat.strip() for cat in cats.split(',') if cat.strip()])
        elif isinstance(cats, list):
            all_categories.extend(cats)

    category_counts = pd.Series(all_categories).value_counts().head(limit)
    return [{"category": cat, "count": int(count)} for cat, count in category_counts.items()]

@router.get("/material-distribution")
def get_material_distribution() -> List[Dict[str, Any]]:
    """Get material distribution"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    material_counts = df['material'].value_counts().head(10)
    return [{"material": mat, "count": int(count)} for mat, count in material_counts.items()]

@router.get("/color-distribution")
def get_color_distribution() -> List[Dict[str, Any]]:
    """Get color distribution"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    color_counts = df['color'].value_counts().head(10)
    return [{"color": col, "count": int(count)} for col, count in color_counts.items()]

@router.get("/country-origin")
def get_country_origin() -> List[Dict[str, Any]]:
    """Get country of origin distribution"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    country_counts = df['country_of_origin'].value_counts().head(10)
    return [{"country": country, "count": int(count)} for country, count in country_counts.items()]

@router.get("/price-by-category")
def get_price_by_category() -> List[Dict[str, Any]]:
    """Get average price by top categories"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    # Use cleaned_price column if available, otherwise clean price column
    df_clean = df.copy()
    if 'cleaned_price' in df_clean.columns:
        df_clean['price'] = df_clean['cleaned_price']
    else:
        df_clean['price'] = pd.to_numeric(df_clean['price'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
    df_clean = df_clean.dropna(subset=['price'])

    if df_clean.empty:
        return []

    # Explode categories properly
    df_exploded = []
    for idx, row in df_clean.iterrows():
        cats = row['categories']
        if isinstance(cats, str):
            # Parse string categories
            if cats.startswith('[') and cats.endswith(']'):
                try:
                    parsed_cats = eval(cats)
                except:
                    parsed_cats = [cat.strip().strip("'\"") for cat in cats.strip('[]').split(',') if cat.strip()]
            else:
                parsed_cats = [cat.strip() for cat in cats.split(',') if cat.strip()]
        elif isinstance(cats, list):
            parsed_cats = cats
        else:
            parsed_cats = []

        for cat in parsed_cats:
            df_exploded.append({
                'category': cat,
                'price': row['price']
            })

    if not df_exploded:
        return []

    df_exploded = pd.DataFrame(df_exploded)
    top_categories = df_exploded['category'].value_counts().head(5).index
    df_top_cat = df_exploded[df_exploded['category'].isin(top_categories)]

    price_by_cat = df_top_cat.groupby('category')['price'].agg(['mean', 'count']).round(2)
    return [
        {
            "category": cat,
            "avg_price": float(row['mean']),
            "product_count": int(row['count'])
        }
        for cat, row in price_by_cat.iterrows()
    ]
