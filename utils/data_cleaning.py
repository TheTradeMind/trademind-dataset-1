"""
Utility functions for cleaning the various data sources.
"""

import pandas as pd
import numpy as np
import re

def clean_trades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the trades DataFrame.

    - Converts 'timestamp' to datetime objects.
    - Converts 'price' and 'volume' to numeric, handling errors.
    - Handles potential missing values.
    - Removes placeholder/comment rows.
    """
    print("Cleaning trades data...")
    df_cleaned = df.copy()
    
    # Remove rows that are likely comments/placeholders
    df_cleaned = df_cleaned[~df_cleaned.iloc[:, 0].astype(str).str.startswith('...')]
    
    # Convert timestamp
    df_cleaned['timestamp'] = pd.to_datetime(df_cleaned['timestamp'], errors='coerce')
    
    # Convert numeric columns
    df_cleaned['price'] = pd.to_numeric(df_cleaned['price'], errors='coerce')
    df_cleaned['volume'] = pd.to_numeric(df_cleaned['volume'], errors='coerce')
    
    # Handle missing values (example: forward fill or drop)
    # df_cleaned.dropna(subset=['timestamp', 'price', 'volume'], inplace=True)
    print(f"Removed {df.shape[0] - df_cleaned.shape[0]} invalid/comment rows.")
    print(f"Found {df_cleaned['timestamp'].isnull().sum()} null timestamps after conversion.")
    print(f"Found {df_cleaned['price'].isnull().sum()} null prices after conversion.")
    print(f"Found {df_cleaned['volume'].isnull().sum()} null volumes after conversion.")

    # Simple outlier check (example)
    # price_std = df_cleaned['price'].std()
    # price_mean = df_cleaned['price'].mean()
    # df_cleaned = df_cleaned[np.abs(df_cleaned['price'] - price_mean) <= (3 * price_std)]

    print(f"Cleaned trades data shape: {df_cleaned.shape}")
    return df_cleaned

def clean_news(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the market news DataFrame.

    - Converts 'timestamp' to datetime.
    - Cleans 'headline' and 'summary' text.
    - Parses 'related_symbols'.
    - Removes placeholder/comment rows.
    """
    print("Cleaning news data...")
    df_cleaned = df.copy()
    
    # Remove rows that are likely comments/placeholders
    df_cleaned = df_cleaned[~df_cleaned.iloc[:, 0].astype(str).str.startswith('...')]

    # Convert timestamp
    df_cleaned['timestamp'] = pd.to_datetime(df_cleaned['timestamp'], errors='coerce')
    
    # Clean text fields (basic example: remove extra whitespace)
    for col in ['headline', 'summary', 'source', 'category']:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()

    # Parse related_symbols (example: split string into list)
    if 'related_symbols' in df_cleaned.columns:
        df_cleaned['related_symbols_list'] = df_cleaned['related_symbols'].str.split(';').apply(
            lambda x: [symbol.strip() for symbol in x] if isinstance(x, list) else x
        ) # Handle potential NaNs or non-list entries

    print(f"Removed {df.shape[0] - df_cleaned.shape[0]} invalid/comment rows.")
    print(f"Cleaned news data shape: {df_cleaned.shape}")
    return df_cleaned

def clean_sentiment_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the sentiment labels DataFrame.
    
    - Converts 'timestamp' to datetime.
    - Ensures 'confidence_score' is numeric.
    - Standardizes 'sentiment_label' values.
    - Removes placeholder/comment rows.
    """
    print("Cleaning sentiment labels data...")
    df_cleaned = df.copy()
    
    # Remove rows that are likely comments/placeholders
    df_cleaned = df_cleaned[~df_cleaned.iloc[:, 0].astype(str).str.startswith('...')]

    # Convert timestamp
    df_cleaned['timestamp'] = pd.to_datetime(df_cleaned['timestamp'], errors='coerce')

    # Convert confidence score
    df_cleaned['confidence_score'] = pd.to_numeric(df_cleaned['confidence_score'], errors='coerce')

    # Standardize sentiment labels (example: lowercase)
    if 'sentiment_label' in df_cleaned.columns:
        df_cleaned['sentiment_label'] = df_cleaned['sentiment_label'].str.lower().str.strip()
        # Define expected labels
        expected_labels = ['positive', 'negative', 'neutral']
        # Filter out rows with unexpected labels (optional)
        # original_count = df_cleaned.shape[0]
        # df_cleaned = df_cleaned[df_cleaned['sentiment_label'].isin(expected_labels)]
        # print(f"Removed {original_count - df_cleaned.shape[0]} rows with non-standard sentiment labels.")

    print(f"Removed {df.shape[0] - df_cleaned.shape[0]} invalid/comment rows.")
    print(f"Cleaned sentiment labels data shape: {df_cleaned.shape}")
    return df_cleaned

# Example Usage (if run directly)
if __name__ == "__main__":
    # Create dummy dataframes matching expected structures (replace with loading actual data)
    dummy_trades = pd.DataFrame({
        'timestamp': ['2023-10-26T10:00:01Z', '...', '2023-10-26T10:00:02Z', 'invalid-date'],
        'symbol': ['BTC-USD', 'comment', 'ETH-USD', 'SOL-USD'],
        'price': ['34500.50', 'ignore', '1850.25', 'abc'],
        'volume': ['0.5', 'this', '2.1', '150.5'],
        'exchange': ['CoinbasePro', 'row', 'Binance', 'Kraken'],
        'trade_type': ['buy', '', 'sell', 'buy'],
        'order_id': ['ORD-1', '', 'ORD-2', 'ORD-3'],
        'account_id': ['ACC-1', '', 'ACC-2', 'ACC-3']
    })
    
    dummy_news = pd.DataFrame({
        'id': ['NEWS-001', 'NEWS-002', '...'],
        'timestamp': ['2023-10-26T09:00:00Z', '2023-10-26T09:30:00Z', 'placeholder'],
        'headline': [' Headline 1 ', 'Headline 2 ', 'comment'],
        'source': ['Source A', 'Source B', 'ignore'],
        'url': ['url1', 'url2', 'this'],
        'related_symbols': ['BTC-USD;ETH-USD', 'ETH-USD', 'row'],
        'category': ['Market Trend', 'Update', ''],
        'summary': ['Summary 1', ' Summary 2 ', '']
    })

    cleaned_trades = clean_trades(dummy_trades)
    print("\nCleaned Trades Head:\n", cleaned_trades.head())
    print("\nCleaned Trades Info:\n", cleaned_trades.info())
    
    print("-"*30)
    
    cleaned_news = clean_news(dummy_news)
    print("\nCleaned News Head:\n", cleaned_news.head())
    print("\nCleaned News Info:\n", cleaned_news.info())
    
    # Add dummy sentiment cleaning example if needed 