# Financial Data Repository

This directory stores the raw and processed financial data used in the valuation models.

## Data Sources
*   **Market Data**: Historical price and volume data (Source: Yahoo Finance).
*   **Financial Statements**: Income Statement, Balance Sheet, and Cash Flow Statement (Annual & Quarterly).
*   **Macroeconomic Data**: Risk-Free Rates (e.g., US 10Y Treasury, German Bund).

## Directory Structure
*   `raw/`: Immutable source files (CSV, JSON) fetched from data providers.
    *   `BMW.DE_*.csv`: Financials for BMW AG.
    *   `MBG.DE_*.csv`: Financials for Mercedes-Benz Group.
    *   `VOW3.DE_*.csv`: Financials for Volkswagen AG.
    *   `P911.DE_*.csv`: Financials for Porsche AG.
    *   `^TNX.csv`: US Treasury Yield (Risk-Free Rate proxy).
*   `processed/`: Cleaned and normalized datasets ready for analysis.

## Data Refresh
To update the datasets with the latest market information, run the data fetching cells in the main notebook or execute the data pipeline scripts in `src/`.
