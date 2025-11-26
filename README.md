# Investment Research: BMW AG Valuation Framework

## Abstract
This project hosts a live, reproducible **Investment White Paper** focused on the quantitative valuation of **Bayerische Motoren Werke AG (BMW.DE)**. Unlike static PDF reports, this repository contains the code, data, and narrative required to generate a dynamic investment thesis.

The core objective is to determine the intrinsic value of BMW equity using a **Discounted Cash Flow (DCF)** approach, supported by rigorous historical analysis and peer benchmarking.

## The White Paper
The primary output of this project is the interactive notebook:
*   📄 **[Investment Thesis: BMW AG](notebooks/bmw_dcf_valuation.ipynb)**

This document is structured to be read as a formal financial report, covering:
1.  **Executive Summary**: High-level investment conclusion.
2.  **Methodology**: Transparent data sourcing and modeling assumptions.
3.  **Historical Analysis**: Deep dive into margins, ROIC, and capital structure.
4.  **Valuation Model**: (In Progress) DCF and Sensitivity Analysis.

## Reproducibility
This analysis is built on a strict Python environment to ensure every figure and calculation can be audited and reproduced.

### Quick Start
To generate the report locally:

1.  **Clone the Research Environment**:
    ```bash
    git clone https://github.com/gitoak/bmw-dcf-valuation-python.git
    ```
2.  **Initialize the Workspace**:
    ```bash
    make install
    ```
3.  **Launch the Analysis**:
    ```bash
    make notebook
    ```

## Data Sources
*   **Yahoo Finance**: Market data and standardized financial statements.
*   **Macro Indicators**: Treasury yields for risk-free rate approximation.

---
*Disclaimer: This project is for educational and informational purposes only. It does not constitute financial advice.*
