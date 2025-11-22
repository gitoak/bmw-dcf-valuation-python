import pandas as pd
import yfinance as yf

from .paths import RAW_DATA_DIR


def get_stock_data(
    ticker: str, start: str = "2023-01-01", end: str | None = None, use_cache: bool = True
) -> pd.DataFrame:
    """
    Fetches stock data from Yahoo Finance.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL", "MSFT").
        start: Start date string (YYYY-MM-DD).
        end: End date string (YYYY-MM-DD).
        use_cache: If True, tries to load from data/raw/{ticker}.csv first.

    Returns:
        pd.DataFrame: The stock history.
    """
    cache_file = RAW_DATA_DIR / f"{ticker}.csv"

    if use_cache and cache_file.exists():
        print(f"Loading {ticker} from cache...")
        return pd.read_csv(cache_file, index_col=0, parse_dates=True)

    print(f"Downloading {ticker} from Yahoo Finance...")
    df: pd.DataFrame = yf.download(  # type: ignore
        ticker, start=start, end=end, progress=False, multi_level_index=False
    )

    # Flatten columns if multi-level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    # Save to cache
    if not df.empty:
        df.to_csv(cache_file)
        print(f"Saved {ticker} to {cache_file}")

    return df
