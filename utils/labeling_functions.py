"""
Utility functions for applying labels (e.g., sentiment) to data.

This could involve rule-based systems, simple ML models, or
functions to structure data for external labeling tools or LLMs.
"""

import pandas as pd
import re

# Example: Simple keyword-based sentiment labeling
POSITIVE_KEYWORDS = ['surge', 'optimism', 'grants', 'expand', 'lists', 'reaches', 'stabilization', 'breakout', 'gain', 'grow', 'positive', 'support']
NEGATIVE_KEYWORDS = ['dip', 'uncertainty', 'weighs', 'delays', 'volatile', 'concerns', 'negative', 'correction', 'fear', 'drop', 'risk']

def label_sentiment_keywords(text: str) -> tuple[str, float]:
    """
    Assigns a sentiment label (Positive, Negative, Neutral) based on keyword matching.
    Returns the label and a basic confidence score (count of keywords).
    """
    if not isinstance(text, str):
        return "Neutral", 0.0
        
    text_lower = text.lower()
    pos_count = sum(1 for keyword in POSITIVE_KEYWORDS if keyword in text_lower)
    neg_count = sum(1 for keyword in NEGATIVE_KEYWORDS if keyword in text_lower)

    if pos_count > neg_count:
        return "Positive", float(pos_count)
    elif neg_count > pos_count:
        return "Negative", float(neg_count)
    else:
        return "Neutral", 0.0 # Confidence 0 if neutral or no keywords

def apply_sentiment_to_news(df: pd.DataFrame, text_column='headline') -> pd.DataFrame:
    """
    Applies the simple keyword sentiment labeling function to a DataFrame.
    """
    print(f"Applying keyword-based sentiment labeling to column '{text_column}'...")
    if text_column not in df.columns:
        print(f"Error: Column '{text_column}' not found in DataFrame.")
        return df
        
    # Ensure the column is string type, fill NaNs with empty string
    df[text_column] = df[text_column].astype(str).fillna('')

    sentiment_results = df[text_column].apply(label_sentiment_keywords)
    df['auto_sentiment_label'] = [res[0] for res in sentiment_results]
    df['auto_sentiment_score'] = [res[1] for res in sentiment_results]
    
    print("Sentiment labeling complete.")
    print("Value counts for 'auto_sentiment_label':")
    print(df['auto_sentiment_label'].value_counts())
    
    return df

# Placeholder for more advanced labeling functions
# def label_using_ml_model(text: str, model):
#     pass

# def create_labeling_tasks(df: pd.DataFrame, output_format='jsonl'):
#     pass

# Example Usage (if run directly)
if __name__ == "__main__":
    # Use the dummy news data from data_cleaning example context
    dummy_news_for_labeling = pd.DataFrame({
        'id': ['NEWS-001', 'NEWS-002', 'NEWS-003', 'NEWS-004'],
        'timestamp': ['2023-10-26T09:00:00Z', '2023-10-26T09:30:00Z', '2023-10-26T10:15:00Z', '2023-10-26T11:00:00Z'],
        'headline': [
            "Bitcoin Surges Past $34,000 Amid Spot ETF Optimism", 
            "Ethereum Staking Rewards See Slight Dip", 
            "Solana Ecosystem Fund Announces New Grants for DeFi Projects", 
            "Regulatory Uncertainty Weighs on Cardano Development"
        ],
        'related_symbols': ['BTC-USD;ETH-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD']
    })
    
    labeled_news = apply_sentiment_to_news(dummy_news_for_labeling.copy(), text_column='headline')
    
    print("\nLabeled News DataFrame Head:")
    print(labeled_news.head()) 