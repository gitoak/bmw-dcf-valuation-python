# Investment Thesis: Bayerische Motoren Werke AG (BMW.DE)

**A Quantitative DCF Valuation & Strategic Analysis**

| | |
|---|---|
| **Date** | December 2025 |
| **Ticker** | BMW.DE (XETRA) |
| **Sector** | Consumer Cyclical — Auto Manufacturers |
| **Classification** | Premium Automotive OEM |

---

## Abstract

This paper presents an intrinsic valuation of BMW AG using a two-stage Discounted Cash Flow (DCF) model. Based on conservative assumptions, we estimate BMW's fair equity value at approximately **€124/share** versus a current market price of ~€85, suggesting the stock is **undervalued by approximately 46%**. The analysis integrates five years of financial data, peer benchmarking against German OEMs, and explicit modeling of BMW's electrification investment cycle.

> **Note:** All computed values in this paper are derived from the accompanying Jupyter notebook. Values marked with [ASSUMED] are analyst assumptions; values marked with [DATA] are sourced from Yahoo Finance; all other values are [COMPUTED] from the model.

**Keywords:** DCF, WACC, ROIC, Free Cash Flow, EV Transition, Automotive Valuation

---

## 1. Executive Summary

### 1.1 Key Findings

Historical financial performance [DATA from Yahoo Finance]:

| Metric | Value | Source |
|--------|-------|--------|
| Revenue (2024) | ~€142B | Annual income statement |
| Current Stock Price | ~€85 | Market data |
| Market Cap | ~€52B | Company info |
| Reported Beta | 0.77 | Company info |

**Valuation Result [COMPUTED]:**

| Metric | Value |
|--------|-------|
| **Intrinsic Value** | **~€124/share** |
| **Market Price** | ~€85/share |
| **Upside Potential** | ~46% |
| **Recommendation** | **Undervalued** |

---

## 2. Methodology

### 2.1 Data Sources

- **Market Data:** Daily OHLCV prices (Yahoo Finance)
- **Financials:** Annual/quarterly statements (2019–2024)
- **Peers:** MBG.DE (Mercedes), VOW3.DE (Volkswagen), P911.DE (Porsche)
- **Risk-Free Rate:** 10Y Treasury yield proxy

### 2.2 Analytical Framework

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Historical     │───▶│  DCF Model      │───▶│  Valuation      │
│  Analysis       │    │  (2-Stage)      │    │  & Sensitivity  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
     │                        │                       │
     ▼                        ▼                       ▼
  Growth              5-Year Forecast          Intrinsic Value
  Profitability       Terminal Value           Risk Assessment
  Capital Efficiency  WACC Discounting         Peer Comparison
```

---

## 3. Financial Performance Analysis

### 3.1 Value Creation Assessment

**Growth:** Revenue trends reflect post-pandemic normalization and EV transition investments.

**Profitability:** EBIT margins have compressed from historical peaks due to:
- Raw material inflation (Li, Co for batteries)
- Elevated R&D for "Neue Klasse" EV platform
- Normalization of pricing power

**Capital Efficiency:** ROIC has declined, approaching WACC threshold:

$$\text{ROIC} = \frac{\text{NOPAT}}{\text{Invested Capital}} = \frac{\text{EBIT} \times (1-t)}{E + D - \text{Cash}}$$

### 3.2 Free Cash Flow Decomposition

$$\text{FCF} = \text{OCF} - \text{CapEx}$$

Recent FCF reflects peak EV investment cycle with elevated CapEx requirements.

---

## 4. DCF Valuation Model

### 4.1 Forecast Assumptions (2025–2029)

All forecast assumptions are analyst estimates [ASSUMED]:

| Parameter | Y1 | Y2 | Y3 | Y4 | Y5 | Rationale |
|-----------|-----|-----|-----|-----|-----|-----------|
| Revenue Growth | **1%** | **2%** | **2%** | **2%** | **2%** | Conservative; EV transition headwinds |
| EBIT Margin | **8%** | **8.5%** | **9%** | **9%** | **9%** | Historical range 8-12%; modest recovery |
| CapEx/Revenue | **8.5%** | **8%** | **7.5%** | **7%** | **6.5%** | Elevated EV investment; gradual normalization |
| D&A/Revenue | **6%** | **6%** | **6%** | **6%** | **6%** | Higher due to EV asset base |
| ΔNWC/ΔRevenue | **10%** | — | — | — | — | Industry standard |
| Tax Rate | **30%** | — | — | — | — | German statutory rate |
| Terminal Growth | — | — | — | — | **2%** | Long-run GDP/inflation proxy |

**Projected FCF Path [COMPUTED]:**

| Year | FCF (€B) |
|------|----------|
| 2025 | ~€4.3B |
| 2026 | ~€5.5B |
| 2027 | ~€6.9B |
| 2028 | ~€7.8B |
| 2029 | ~€8.7B |

### 4.2 Cost of Capital (WACC)

#### Assumed Parameters [ASSUMED]

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Equity Risk Premium | **5.5%** | Industry standard (5-6%); elevated for cyclical sector |
| Pre-tax Cost of Debt | **4.5%** | BMW investment-grade rating (A/A2) |
| Tax Rate | **30%** | German statutory + trade taxes |
| Target Equity Weight | **70%** | Industrial operations target structure |
| Target Debt Weight | **30%** | Excludes captive financing distortions |
| Beta Floor | **1.0** | Cyclical auto minimum (raw beta understates risk) |

#### Data Inputs [DATA]

| Parameter | Value | Source |
|-----------|-------|--------|
| Risk-Free Rate | ~4.06% | 10Y Treasury (^TNX) |
| Reported Beta | 0.77 | Yahoo Finance |

#### Computed Values [COMPUTED]

**Cost of Equity (CAPM):**
$$r_e = R_f + \beta \cdot (R_m - R_f)$$
$$r_e = 4.06\% + 1.0 \times 5.5\% = 9.56\%$$

**Cost of Debt (After-Tax):**
$$r_d^* = r_d \times (1 - t) = 4.5\% \times (1 - 0.30) = 3.15\%$$

**WACC Calculation:**
$$\text{WACC} = w_E \cdot r_e + w_D \cdot r_d^*$$
$$\text{WACC} = 0.70 \times 9.56\% + 0.30 \times 3.15\% = \mathbf{7.64\%}$$

### 4.3 Terminal Value [COMPUTED]

Using the Gordon Growth perpetuity model:
$$TV_{2029} = \frac{\text{FCF}_{2029} \times (1 + g)}{\text{WACC} - g}$$
$$TV_{2029} = \frac{€8.72\text{B} \times 1.02}{0.0764 - 0.02} = \frac{€8.90\text{B}}{0.0564} = \mathbf{€157.8\text{B}}$$

**Implied Exit Multiples (Sanity Check) [COMPUTED]:**
- EV/EBITDA: ~6.8× (reasonable for mature automaker)
- EV/FCF: ~18.1×

### 4.4 Enterprise Value Calculation [COMPUTED]

**Present Value of Forecast Period FCFs:**
$$PV_{FCF} = \sum_{t=1}^{5} \frac{\text{FCF}_t}{(1 + \text{WACC})^t} \approx \mathbf{€26.1\text{B}}$$

**Present Value of Terminal Value:**
$$PV_{TV} = \frac{TV_{2029}}{(1 + \text{WACC})^5} = \frac{€157.8\text{B}}{(1.0764)^5} = \mathbf{€109.2\text{B}}$$

**Enterprise Value:**
$$EV = PV_{FCF} + PV_{TV} = €26.1\text{B} + €109.2\text{B} = \mathbf{€135.3\text{B}}$$

**Terminal Value Concentration:** ~80.7% of EV (typical for DCF models)

### 4.5 Equity Value Bridge [COMPUTED]

| Component | Value (€B) |
|-----------|-----------|
| Enterprise Value | **135.3** |
| Less: Net Debt | **(66.2)** |
| **Equity Value** | **69.1** |

**Per Share Calculation:**
- Shares Outstanding [DATA]: ~556M
- **Intrinsic Value/Share [COMPUTED]: €124.27**

### 4.6 Scenario Analysis

#### Assumed Scenario Parameters [ASSUMED]

| Scenario | WACC | Terminal Growth | Terminal Margin | Rationale |
|----------|------|-----------------|-----------------|-----------|
| **Bull** | 6.5% | 2.5% | 11.5% | Successful EV transition |
| **Base** | 7.64% | 2.0% | 9% | Conservative assumptions |
| **Bear** | 8.5% | 1.0% | 6.5% | Competitive pressure |

#### Computed Scenario Values [COMPUTED]

| Scenario | Intrinsic Value | vs. Market (~€85) |
|----------|-----------------|-------------------|
| **Bull** | ~€173/share | +104% upside |
| **Base** | ~€124/share | +46% upside |
| **Bear** | ~€45/share | -47% downside |

**Probability-Weighted Expected Value [COMPUTED]:**
- Weights: Bull 25%, Base 50%, Bear 25%
- Expected Value: ~€117/share

---

## 5. Sensitivity Analysis

### 5.1 WACC–Growth Sensitivity [COMPUTED]

Intrinsic value per share varies significantly with discount rate and growth assumptions. A 1% increase in WACC reduces intrinsic value by approximately €20-30/share.

### 5.2 Risk Factors

| Risk | Impact on DCF | Probability |
|------|---------------|-------------|
| Global recession | WACC ↑, FCF ↓ | Medium |
| EV margin dilution | FCF ↓, g ↓ | Medium-High |
| Battery cost inflation | FCF ↓ | Medium |
| Competitive disruption | g ↓ | Medium |
| **Upside:** EV success | FCF ↑, g ↑ | Medium |

---

## 6. Peer Benchmarking

### 6.1 Comparative Context

BMW trades at a premium to VW/Mercedes but at a discount to Porsche—consistent with its premium positioning in the automotive market. Peer comparison provides sanity checks on valuation multiples.

---

## 7. Conclusion

### 7.1 Investment Verdict

| Criterion | Assessment |
|-----------|------------|
| Intrinsic Value [COMPUTED] | **~€124/share** |
| Market Price [DATA] | ~€85/share |
| Upside Potential | **~46%** |
| Margin of Safety | **Significant** |
| Recommendation | **Undervalued** |

### 7.2 Key Monitoring Metrics

1. **EBIT Margin:** Track recovery toward 9%+ by 2027
2. **FCF:** Must turn positive and grow per forecast
3. **ROIC vs WACC:** Spread must widen for value creation
4. **EV Unit Sales:** Neue Klasse adoption trajectory

### 7.3 Final Assessment

BMW appears **undervalued** at current market levels under our conservative assumptions. The DCF analysis suggests approximately 46% upside to fair value. Key risks include:

- Terminal value represents ~81% of enterprise value (high sensitivity to assumptions)
- EV transition execution uncertainty
- Cyclical auto industry exposure

The investment thesis depends on BMW achieving:

$$\text{ROIC} > \text{WACC} \implies \text{Value Creation}$$

---

## Appendix: Assumed vs. Computed Values Summary

### All Assumed Values (Analyst Estimates)

| Parameter | Value | Location |
|-----------|-------|----------|
| Equity Risk Premium | 5.5% | WACC |
| Pre-tax Cost of Debt | 4.5% | WACC |
| Tax Rate | 30% | WACC, Forecast |
| Target Equity Weight | 70% | WACC |
| Target Debt Weight | 30% | WACC |
| Beta Floor | 1.0 | WACC |
| Revenue Growth (Y1-Y5) | 1%, 2%, 2%, 2%, 2% | Forecast |
| EBIT Margin (Y1-Y5) | 8%, 8.5%, 9%, 9%, 9% | Forecast |
| CapEx/Revenue (Y1-Y5) | 8.5%, 8%, 7.5%, 7%, 6.5% | Forecast |
| D&A/Revenue | 6% | Forecast |
| ΔNWC/ΔRevenue | 10% | Forecast |
| Terminal Growth Rate | 2% | Terminal Value |
| Bull WACC | 6.5% | Scenarios |
| Bear WACC | 8.5% | Scenarios |
| Scenario Weights | 25/50/25 | Scenarios |

### Key Computed Values (Model Outputs)

| Parameter | Value |
|-----------|-------|
| Cost of Equity | 9.56% |
| Cost of Debt (after-tax) | 3.15% |
| **WACC** | **7.64%** |
| Terminal FCF | €8.72B |
| Terminal Value | €157.8B |
| PV of FCFs | €26.1B |
| PV of Terminal Value | €109.2B |
| **Enterprise Value** | **€135.3B** |
| Net Debt | €66.2B |
| **Equity Value** | **€69.1B** |
| **Intrinsic Value/Share** | **€124.27** |

---

## References

1. Damodaran, A. (2012). *Investment Valuation*. Wiley.
2. Koller, T., Goedhart, M., & Wessels, D. (2020). *Valuation*. McKinsey & Company.
3. [CAPM & Cost of Equity](https://www.investopedia.com/ask/answers/022515/how-do-i-use-capm-capital-asset-pricing-model-determine-cost-equity.asp)
4. [WACC Calculation](https://www.investopedia.com/ask/answers/021615/how-do-you-calculate-proper-weights-different-costs-capital.asp)
5. [Terminal Value Methods](https://macabacus.com/valuation/dcf-terminal-value)

---

*This analysis is for educational purposes. All projections involve uncertainty; actual results may differ materially. Computed values are derived from the accompanying Jupyter notebook and reflect model outputs as of the analysis date.*
