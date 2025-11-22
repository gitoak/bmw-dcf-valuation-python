import json

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


def get_company_financials(ticker: str, use_cache: bool = True) -> dict[str, pd.DataFrame]:
    """
    Fetches financials (income stmt, balance sheet, cashflow) from Yahoo Finance.

    Args:
        ticker: The stock ticker symbol.
        use_cache: If True, tries to load from data/raw/{ticker}_{type}.csv first.

    Returns:
        dict: Dictionary containing 'income_stmt', 'balance_sheet', 'cashflow' DataFrames.
    """
    financials = {}
    types = {
        "income_stmt": "financials",
        "balance_sheet": "balance_sheet",
        "cashflow": "cashflow",
    }

    t = yf.Ticker(ticker)

    for name, yf_attr in types.items():
        cache_file = RAW_DATA_DIR / f"{ticker}_{name}.csv"

        if use_cache and cache_file.exists():
            print(f"Loading {ticker} {name} from cache...")
            # yfinance financials usually have dates as columns, so we read with index_col=0
            financials[name] = pd.read_csv(cache_file, index_col=0)
            # Convert columns to datetime if they look like dates
            try:
                financials[name].columns = pd.to_datetime(financials[name].columns)
            except Exception:
                pass
        else:
            print(f"Downloading {ticker} {name} from Yahoo Finance...")
            df = getattr(t, yf_attr)

            if not df.empty:
                df.to_csv(cache_file)
                print(f"Saved {ticker} {name} to {cache_file}")
            financials[name] = df

    return financials


def get_company_info(ticker: str, use_cache: bool = True) -> dict:
    """
    Fetches company info (beta, market cap, etc.) from Yahoo Finance.

    Args:
        ticker: The stock ticker symbol.
        use_cache: If True, tries to load from data/raw/{ticker}_info.json first.

    Returns:
        dict: Dictionary containing company info.
    """
    cache_file = RAW_DATA_DIR / f"{ticker}_info.json"

    if use_cache and cache_file.exists():
        print(f"Loading {ticker} info from cache...")
        with open(cache_file) as f:
            return json.load(f)

    print(f"Downloading {ticker} info from Yahoo Finance...")
    t = yf.Ticker(ticker)
    info = t.info

    # Save to cache
    if info:
        with open(cache_file, "w") as f:
            json.dump(info, f, indent=4)
        print(f"Saved {ticker} info to {cache_file}")

    return info


def get_quarterly_financials(ticker: str, use_cache: bool = True) -> dict[str, pd.DataFrame]:
    """
    Fetches quarterly financials from Yahoo Finance.

    Args:
        ticker: The stock ticker symbol.
        use_cache: If True, tries to load from data/raw/{ticker}_quarterly_{type}.csv first.

    Returns:
        dict: Dictionary containing 'income_stmt', 'balance_sheet', 'cashflow' DataFrames.
    """
    financials = {}
    types = {
        "income_stmt": "quarterly_financials",
        "balance_sheet": "quarterly_balance_sheet",
        "cashflow": "quarterly_cashflow",
    }

    t = yf.Ticker(ticker)

    for name, yf_attr in types.items():
        cache_file = RAW_DATA_DIR / f"{ticker}_quarterly_{name}.csv"

        if use_cache and cache_file.exists():
            print(f"Loading {ticker} quarterly {name} from cache...")
            financials[name] = pd.read_csv(cache_file, index_col=0)
            try:
                financials[name].columns = pd.to_datetime(financials[name].columns)
            except Exception:
                pass
        else:
            print(f"Downloading {ticker} quarterly {name} from Yahoo Finance...")
            df = getattr(t, yf_attr)

            if not df.empty:
                df.to_csv(cache_file)
                print(f"Saved {ticker} quarterly {name} to {cache_file}")
            financials[name] = df

    return financials


def get_holders_and_recommendations(ticker: str, use_cache: bool = True) -> dict[str, pd.DataFrame]:
    """
    Fetches institutional holders, major holders, and recommendations.

    Args:
        ticker: The stock ticker symbol.
        use_cache: If True, tries to load from data/raw/{ticker}_{type}.csv first.

    Returns:
        dict: Dictionary containing 'institutional_holders', 'major_holders', 'recommendations'.
    """
    data = {}
    types = {
        "institutional_holders": "institutional_holders",
        "major_holders": "major_holders",
        "recommendations": "recommendations",
    }

    t = yf.Ticker(ticker)

    for name, yf_attr in types.items():
        cache_file = RAW_DATA_DIR / f"{ticker}_{name}.csv"

        if use_cache and cache_file.exists():
            print(f"Loading {ticker} {name} from cache...")
            data[name] = pd.read_csv(cache_file)
        else:
            print(f"Downloading {ticker} {name} from Yahoo Finance...")
            df = getattr(t, yf_attr)

            if df is not None and not df.empty:
                df.to_csv(cache_file, index=False)
                print(f"Saved {ticker} {name} to {cache_file}")
                data[name] = df
            else:
                data[name] = pd.DataFrame()

    return data


def get_treasury_yield(
    ticker: str = "^TNX", start: str = "2019-01-01", end: str | None = None, use_cache: bool = True
) -> pd.Series:
    """
    Fetches the treasury yield (Risk-Free Rate).
    Default is ^TNX (CBOE Interest Rate 10 Year T Note).
    Returns the 'Close' column as a Series.
    """
    df = get_stock_data(ticker, start=start, end=end, use_cache=use_cache)
    return df["Close"]
