"""
Plotting utilities for DCF valuation analysis.

This module provides reusable visualization functions for financial analysis,
including comprehensive dashboards, WACC analysis, forecast visualizations,
and sensitivity analysis charts.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import seaborn as sns
from plotly.subplots import make_subplots

# =============================================================================
# Color Palette (DCF-themed)
# =============================================================================
DCF_COLORS = {
    "primary": "rgb(55, 83, 109)",  # Dark blue
    "secondary": "rgb(26, 118, 255)",  # Bright blue
    "positive": "rgb(44, 160, 101)",  # Green
    "negative": "rgb(214, 39, 40)",  # Red
    "neutral": "rgb(148, 103, 189)",  # Purple
    "highlight": "rgb(255, 127, 14)",  # Orange
    "muted": "rgb(180, 180, 180)",  # Gray
}


def set_style():
    """
    Sets a professional plotting style for Matplotlib and Seaborn.
    Also sets the default Plotly template.
    """
    # Seaborn / Matplotlib style
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["axes.labelsize"] = 12

    # Plotly default template
    pio.templates.default = "plotly_white"


def save_fig(fig, filename: str, tight_layout: bool = True):
    """
    Helper to save matplotlib figures easily.
    """
    if tight_layout:
        plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")


# =============================================================================
# High-Level Visualization Functions for DCF Analysis
# =============================================================================


def financial_performance_dashboard(
    df_annual: pd.DataFrame,
    df_quarterly: pd.DataFrame,
    df_prices: pd.DataFrame,
    peer_metrics: dict,
    ticker: str,
) -> go.Figure:
    """
    Generate comprehensive 6-panel financial performance dashboard.

    Parameters
    ----------
    df_annual : pd.DataFrame
        Annual financial metrics with DatetimeIndex
    df_quarterly : pd.DataFrame
        Quarterly financial metrics
    df_prices : pd.DataFrame
        Daily stock price data
    peer_metrics : dict
        Dictionary of peer company DataFrames {ticker: df}
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 6 subplots
    """
    years = pd.DatetimeIndex(df_annual.index).year

    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=(
            "(a) Revenue & EBIT Margin",
            "(b) Free Cash Flow Composition",
            "(c) Quarterly Revenue Trend",
            "(d) Stock Price History",
            "(e) Return on Invested Capital",
            "(f) Peer Comparison: Operating Margin",
        ),
        specs=[
            [{"secondary_y": True}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
        ],
        vertical_spacing=0.10,
    )

    # Panel (a): Revenue & EBIT Margin
    fig.add_trace(
        go.Bar(
            x=years,
            y=df_annual["Revenue"],
            name="Revenue",
            marker_color=DCF_COLORS["primary"],
        ),
        row=1,
        col=1,
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=df_annual["EBIT Margin"],
            name="EBIT Margin",
            mode="lines+markers",
            line=dict(color=DCF_COLORS["secondary"], width=3),
        ),
        row=1,
        col=1,
        secondary_y=True,
    )

    # Panel (b): FCF Composition
    fig.add_trace(
        go.Bar(
            x=years,
            y=df_annual["OCF"],
            name="Operating Cash Flow",
            marker_color=DCF_COLORS["positive"],
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Bar(
            x=years,
            y=df_annual["CapEx"],
            name="Capital Expenditure",
            marker_color=DCF_COLORS["negative"],
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=df_annual["FCF"],
            name="Free Cash Flow",
            line=dict(color="black", width=3, dash="dash"),
        ),
        row=1,
        col=2,
    )

    # Panel (c): Quarterly Revenue
    fig.add_trace(
        go.Scatter(
            x=df_quarterly.index,
            y=df_quarterly["Revenue"],
            name="Quarterly Revenue",
            fill="tozeroy",
            line=dict(color=DCF_COLORS["neutral"]),
        ),
        row=2,
        col=1,
    )

    # Panel (d): Stock Price
    fig.add_trace(
        go.Scatter(
            x=df_prices.index,
            y=df_prices["Close"],
            name="Closing Price",
            line=dict(color=DCF_COLORS["highlight"]),
        ),
        row=2,
        col=2,
    )

    # Panel (e): ROIC
    fig.add_trace(
        go.Bar(
            x=years,
            y=df_annual["ROIC"],
            name="ROIC",
            marker_color="rgb(31, 119, 180)",
        ),
        row=3,
        col=1,
    )

    # Panel (f): Peer Comparison
    fig.add_trace(
        go.Scatter(
            x=years,
            y=df_annual["EBIT Margin"],
            name=f"{ticker}",
            mode="lines+markers",
            line=dict(width=3),
        ),
        row=3,
        col=2,
    )

    for p, p_df in peer_metrics.items():
        p_years = pd.DatetimeIndex(p_df.index).year
        fig.add_trace(
            go.Scatter(
                x=p_years,
                y=p_df["EBIT Margin"],
                name=p,
                mode="lines",
                line=dict(dash="dot"),
            ),
            row=3,
            col=2,
        )

    # Layout Configuration
    fig.update_layout(
        height=1200,
        title_text=f"Figure 1: Financial Performance Dashboard — {ticker}",
        template="plotly_white",
        showlegend=True,
        font=dict(size=11),
    )

    # Axis formatting
    fig.update_yaxes(title_text="Revenue (EUR)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Margin", tickformat=".1%", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Amount (EUR)", row=1, col=2)
    fig.update_yaxes(title_text="Revenue (EUR)", row=2, col=1)
    fig.update_yaxes(title_text="Price (EUR)", row=2, col=2)
    fig.update_yaxes(title_text="ROIC", tickformat=".1%", row=3, col=1)
    fig.update_yaxes(title_text="EBIT Margin", tickformat=".1%", row=3, col=2)

    return fig


def wacc_analysis_chart(
    market_cap: float,
    net_debt: float,
    cost_of_equity: float,
    cost_of_debt_aftertax: float,
    wacc: float,
    ticker: str,
) -> go.Figure:
    """
    Create 2-panel WACC visualization: capital structure pie + components bar.

    Parameters
    ----------
    market_cap : float
        Market capitalization
    net_debt : float
        Net debt (total debt - cash)
    cost_of_equity : float
        Cost of equity (decimal, e.g., 0.0956 for 9.56%)
    cost_of_debt_aftertax : float
        After-tax cost of debt (decimal)
    wacc : float
        Weighted average cost of capital (decimal)
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 2 subplots
    """
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("(a) Capital Structure", "(b) WACC Components"),
        specs=[[{"type": "pie"}, {"type": "bar"}]],
    )

    # Panel (a): Capital Structure Pie Chart
    fig.add_trace(
        go.Pie(
            labels=["Equity", "Net Debt"],
            values=[market_cap, net_debt],
            marker_colors=[DCF_COLORS["primary"], DCF_COLORS["secondary"]],
            textinfo="label+percent",
            textposition="inside",
            hole=0.4,
        ),
        row=1,
        col=1,
    )

    # Panel (b): WACC Components Bar Chart
    components = ["Cost of Equity", "Cost of Debt\n(after-tax)", "WACC"]
    values = [cost_of_equity * 100, cost_of_debt_aftertax * 100, wacc * 100]
    colors = [DCF_COLORS["positive"], DCF_COLORS["negative"], DCF_COLORS["neutral"]]

    fig.add_trace(
        go.Bar(
            x=components,
            y=values,
            marker_color=colors,
            text=[f"{v:.2f}%" for v in values],
            textposition="outside",
        ),
        row=1,
        col=2,
    )

    fig.update_layout(
        height=450,
        title_text=f"Figure 2: WACC Analysis — {ticker}",
        template="plotly_white",
        showlegend=False,
        margin=dict(t=80, b=60, l=60, r=60),
    )

    fig.update_yaxes(title_text="Rate (%)", row=1, col=2, range=[0, 12])

    return fig


def forecast_assumptions_chart(
    forecast_years: list,
    revenue_growth: list,
    ebit_margin_forecast: list,
    capex_pct: list,
    da_pct: list,
    ticker: str,
) -> go.Figure:
    """
    Create 2-panel chart showing forecast trajectory and capital intensity.

    Parameters
    ----------
    forecast_years : list
        List of forecast years
    revenue_growth : list
        Revenue growth rates (decimal)
    ebit_margin_forecast : list
        EBIT margin forecasts (decimal)
    capex_pct : list
        CapEx as % of revenue (decimal)
    da_pct : list
        D&A as % of revenue (decimal)
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 2 subplots
    """
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("(a) Revenue & Margin Trajectory", "(b) Capital Intensity"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}]],
    )

    # Panel (a): Revenue Growth and EBIT Margin
    fig.add_trace(
        go.Bar(
            x=[str(y) for y in forecast_years],
            y=[g * 100 for g in revenue_growth],
            name="Revenue Growth",
            marker_color=DCF_COLORS["primary"],
            text=[f"{g:.1%}" for g in revenue_growth],
            textposition="outside",
        ),
        row=1,
        col=1,
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=[str(y) for y in forecast_years],
            y=[m * 100 for m in ebit_margin_forecast],
            name="EBIT Margin",
            mode="lines+markers+text",
            line=dict(color=DCF_COLORS["positive"], width=3),
            marker=dict(size=10),
            text=[f"{m:.1%}" for m in ebit_margin_forecast],
            textposition="top center",
        ),
        row=1,
        col=1,
        secondary_y=True,
    )

    # Panel (b): CapEx and D&A
    fig.add_trace(
        go.Scatter(
            x=[str(y) for y in forecast_years],
            y=[c * 100 for c in capex_pct],
            name="CapEx/Rev",
            mode="lines+markers",
            line=dict(color=DCF_COLORS["negative"], width=3),
            marker=dict(size=10),
        ),
        row=1,
        col=2,
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=[str(y) for y in forecast_years],
            y=[d * 100 for d in da_pct],
            name="D&A/Rev",
            mode="lines+markers",
            line=dict(color=DCF_COLORS["neutral"], width=3, dash="dash"),
            marker=dict(size=10),
        ),
        row=1,
        col=2,
        secondary_y=False,
    )

    fig.update_layout(
        height=350,
        title_text=f"Forecast Assumptions (2025–2029) — {ticker}",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(t=80, b=80),
    )

    fig.update_yaxes(title_text="Revenue Growth (%)", row=1, col=1, secondary_y=False, range=[0, 5])
    fig.update_yaxes(title_text="EBIT Margin (%)", row=1, col=1, secondary_y=True, range=[6, 12])
    fig.update_yaxes(title_text="% of Revenue", row=1, col=2, range=[4, 10])

    return fig


def fcf_forecast_chart(
    df_annual: pd.DataFrame,
    df_forecast: pd.DataFrame,
    ticker: str,
    show_historical_years: int = 3,
) -> go.Figure:
    """
    Create historical + forecast revenue, margins, and FCF with transition line.

    Parameters
    ----------
    df_annual : pd.DataFrame
        Annual financial data
    df_forecast : pd.DataFrame
        Forecast data with Year index
    ticker : str
        Company ticker symbol
    show_historical_years : int
        Number of historical years to show

    Returns
    -------
    go.Figure
        Plotly figure with 2 subplots
    """
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "(a) Revenue & EBIT Margin Forecast",
            "(b) Free Cash Flow Projection",
        ),
        specs=[[{"secondary_y": True}, {"secondary_y": False}]],
    )

    # Prepare data
    years = pd.DatetimeIndex(df_annual.index).year
    hist_years = list(years[-show_historical_years:])
    fcst_years = list(df_forecast.index)
    all_years = hist_years + fcst_years

    hist_revenue = df_annual["Revenue"].iloc[-show_historical_years:].values / 1e9  # type: ignore
    hist_ebit_margin = df_annual["EBIT Margin"].iloc[-show_historical_years:].values
    hist_fcf = df_annual["FCF"].iloc[-show_historical_years:].values / 1e9  # type: ignore

    fcst_revenue = df_forecast["Revenue"].values / 1e9  # type: ignore
    fcst_ebit_margin = df_forecast["EBIT Margin"].values
    fcst_fcf = df_forecast["FCF"].values / 1e9  # type: ignore

    # Panel (a): Revenue & EBIT Margin
    fig.add_trace(
        go.Bar(
            x=hist_years,
            y=hist_revenue,
            name="Revenue (Historical)",
            marker_color=DCF_COLORS["primary"],
        ),
        row=1,
        col=1,
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(
            x=fcst_years,
            y=fcst_revenue,
            name="Revenue (Forecast)",
            marker_color="rgba(55, 83, 109, 0.5)",
            marker_line=dict(color=DCF_COLORS["primary"], width=2),
        ),
        row=1,
        col=1,
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=all_years,
            y=list(hist_ebit_margin) + list(fcst_ebit_margin),
            name="EBIT Margin",
            mode="lines+markers",
            line=dict(color=DCF_COLORS["secondary"], width=3),
            marker=dict(size=10),
        ),
        row=1,
        col=1,
        secondary_y=True,
    )

    fig.add_vline(x=hist_years[-1] + 0.5, line_dash="dash", line_color="gray", row=1, col=1)  # type: ignore

    # Panel (b): FCF
    fig.add_trace(
        go.Bar(
            x=hist_years,
            y=hist_fcf,
            name="FCF (Historical)",
            marker_color=DCF_COLORS["positive"],
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Bar(
            x=fcst_years,
            y=fcst_fcf,
            name="FCF (Forecast)",
            marker_color="rgba(44, 160, 101, 0.5)",
            marker_line=dict(color=DCF_COLORS["positive"], width=2),
        ),
        row=1,
        col=2,
    )

    fig.add_vline(x=hist_years[-1] + 0.5, line_dash="dash", line_color="gray", row=1, col=2)  # type: ignore

    fig.add_annotation(
        x=fcst_years[2],
        y=max(fcst_fcf) * 1.1,
        text="Forecast Period",
        showarrow=False,
        font=dict(size=12, color="gray"),
        row=1,
        col=2,
    )

    fig.update_layout(
        height=450,
        title_text=f"Figure 3: 5-Year Financial Forecast — {ticker}",
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        barmode="group",
    )

    fig.update_yaxes(title_text="Revenue (€B)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="EBIT Margin", tickformat=".0%", row=1, col=1, secondary_y=True)
    fig.update_yaxes(title_text="FCF (€B)", row=1, col=2)

    return fig


def dcf_valuation_summary(
    pv_forecast_fcfs: float,
    pv_terminal_value: float,
    enterprise_value: float,
    net_debt: float,
    equity_value: float,
    intrinsic_value_per_share: float,
    current_price: float,
    ticker: str,
) -> go.Figure:
    """
    Create 4-panel DCF results: EV donut, equity bridge, price comparison, valuation gauge.

    Parameters
    ----------
    pv_forecast_fcfs : float
        Present value of forecast period FCFs
    pv_terminal_value : float
        Present value of terminal value
    enterprise_value : float
        Total enterprise value
    net_debt : float
        Net debt
    equity_value : float
        Equity value
    intrinsic_value_per_share : float
        Intrinsic value per share
    current_price : float
        Current market price
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 4 subplots
    """
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "(a) Enterprise Value Composition",
            "(b) Equity Value Bridge",
            "(c) Intrinsic vs Market Price",
            "(d) Valuation Metrics",
        ),
        specs=[
            [{"type": "pie"}, {"type": "waterfall"}],
            [{"type": "bar"}, {"type": "indicator"}],
        ],
        vertical_spacing=0.22,
        horizontal_spacing=0.12,
    )

    # Panel (a): Value Composition Donut
    fig.add_trace(
        go.Pie(
            labels=["PV of FCFs<br>(2025-29)", "PV of<br>Terminal Value"],
            values=[pv_forecast_fcfs / 1e9, pv_terminal_value / 1e9],
            marker_colors=[DCF_COLORS["positive"], DCF_COLORS["neutral"]],
            textinfo="percent",
            textposition="inside",
            textfont=dict(size=14, color="white"),
            hole=0.5,
            hovertemplate="<b>%{label}</b><br>€%{value:.1f}B<br>%{percent}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    fig.add_annotation(
        text=f"<b>EV</b><br>€{enterprise_value / 1e9:.0f}B",
        x=0.145,
        y=0.78,
        font=dict(size=14),
        showarrow=False,
        xref="paper",
        yref="paper",
    )

    # Panel (b): Equity Bridge Waterfall
    fig.add_trace(
        go.Waterfall(
            x=["Enterprise<br>Value", "Less:<br>Net Debt", "Equity<br>Value"],
            y=[enterprise_value / 1e9, -net_debt / 1e9, equity_value / 1e9],
            measure=["absolute", "relative", "total"],
            text=[
                f"€{enterprise_value / 1e9:.0f}B",
                f"−€{net_debt / 1e9:.0f}B",
                f"€{equity_value / 1e9:.0f}B",
            ],
            textposition="outside",
            textfont=dict(size=12),
            connector={"line": {"color": "rgb(63, 63, 63)", "width": 1}},
            increasing={"marker": {"color": DCF_COLORS["positive"]}},
            decreasing={"marker": {"color": DCF_COLORS["negative"]}},
            totals={"marker": {"color": DCF_COLORS["primary"]}},
        ),
        row=1,
        col=2,
    )

    # Panel (c): Price Comparison Bar
    price_diff = intrinsic_value_per_share - current_price
    bar_colors = [
        DCF_COLORS["primary"],
        DCF_COLORS["positive"] if price_diff > 0 else DCF_COLORS["negative"],
    ]

    fig.add_trace(
        go.Bar(
            x=["Market Price", "DCF Value"],
            y=[current_price, intrinsic_value_per_share],
            marker_color=bar_colors,
            text=[f"€{current_price:.0f}", f"€{intrinsic_value_per_share:.0f}"],
            textposition="outside",
            textfont=dict(size=14),
            hovertemplate="<b>%{x}</b><br>€%{y:.2f}<extra></extra>",
        ),
        row=2,
        col=1,
    )

    # Panel (d): Valuation Indicator
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=intrinsic_value_per_share,
            number={"prefix": "€", "font": {"size": 48}},
            delta={
                "reference": current_price,
                "relative": True,
                "valueformat": ".1%",
                "font": {"size": 20},
            },
            title={
                "text": "DCF Intrinsic Value<br><span style='font-size:12px;color:gray'>vs Market Price</span>"
            },
            domain={"x": [0.55, 0.95], "y": [0.0, 0.4]},
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        height=700,
        title_text=f"Figure 4: DCF Valuation Results — {ticker}",
        title_font=dict(size=16),
        template="plotly_white",
        showlegend=False,
        margin=dict(t=100, b=60, l=60, r=60),
    )

    fig.update_yaxes(title_text="€ Billion", row=1, col=2, range=[0, 160])
    fig.update_yaxes(title_text="€ per Share", row=2, col=1, range=[0, 160])

    return fig


def sensitivity_analysis_charts(
    sensitivity_matrix: pd.DataFrame,
    wacc: float,
    terminal_growth_rate: float,
    intrinsic_value_per_share: float,
    tornado_data: list,
    ticker: str,
) -> go.Figure:
    """
    Create combined sensitivity heatmap + tornado chart.

    Parameters
    ----------
    sensitivity_matrix : pd.DataFrame
        Sensitivity matrix with WACC as index and growth rates as columns
    wacc : float
        Base case WACC (decimal)
    terminal_growth_rate : float
        Base case terminal growth rate (decimal)
    intrinsic_value_per_share : float
        Base case intrinsic value
    tornado_data : list[dict]
        List of dicts with keys 'var', 'low', 'high', 'range'
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 2 subplots
    """
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "(a) WACC–Growth Sensitivity Matrix",
            "(b) Key Driver Impact (Tornado)",
        ),
        specs=[[{"type": "heatmap"}, {"type": "bar"}]],
        horizontal_spacing=0.18,
    )

    # Panel (a): Heatmap
    z_values = sensitivity_matrix.values
    x_labels = list(sensitivity_matrix.columns)
    y_labels = list(sensitivity_matrix.index)

    base_wacc_str = f"{wacc:.1%}"
    base_growth_str = f"{terminal_growth_rate:.1%}"
    base_wacc_idx = y_labels.index(base_wacc_str) if base_wacc_str in y_labels else 2
    base_growth_idx = x_labels.index(base_growth_str) if base_growth_str in x_labels else 2

    fig.add_trace(
        go.Heatmap(
            z=z_values,
            x=x_labels,
            y=y_labels,
            colorscale="RdYlGn",
            text=[[f"€{v:.0f}" for v in row] for row in z_values],
            texttemplate="%{text}",
            textfont={"size": 11},
            hovertemplate="WACC: %{y}<br>Growth: %{x}<br>Value: €%{z:.0f}<extra></extra>",
            colorbar=dict(title="€/Share", x=0.46, len=0.9),
        ),
        row=1,
        col=1,
    )

    # Mark base case
    fig.add_trace(
        go.Scatter(
            x=[x_labels[base_growth_idx]],
            y=[y_labels[base_wacc_idx]],
            mode="markers+text",
            marker=dict(size=25, symbol="star", color="black", line=dict(color="white", width=2)),
            text=["★"],
            textfont=dict(size=20, color="gold"),
            textposition="middle center",
            name="Base Case",
            showlegend=False,
            hovertemplate=f"<b>Base Case</b><br>WACC: {base_wacc_str}<br>Growth: {base_growth_str}<br>Value: €{intrinsic_value_per_share:.0f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    # Panel (b): Tornado Chart
    base_value = intrinsic_value_per_share

    # Low side bars
    fig.add_trace(
        go.Bar(
            y=[d["var"] for d in tornado_data],
            x=[d["low"] - base_value for d in tornado_data],
            orientation="h",
            name="Downside",
            marker_color=DCF_COLORS["negative"],
            text=[f"€{d['low']:.0f}" for d in tornado_data],
            textposition="outside",
            textfont=dict(size=10),
            hovertemplate="<b>%{y}</b><br>Value: €%{text}<extra></extra>",
        ),
        row=1,
        col=2,
    )

    # High side bars
    fig.add_trace(
        go.Bar(
            y=[d["var"] for d in tornado_data],
            x=[d["high"] - base_value for d in tornado_data],
            orientation="h",
            name="Upside",
            marker_color=DCF_COLORS["positive"],
            text=[f"€{d['high']:.0f}" for d in tornado_data],
            textposition="outside",
            textfont=dict(size=10),
            hovertemplate="<b>%{y}</b><br>Value: €%{text}<extra></extra>",
        ),
        row=1,
        col=2,
    )

    fig.add_vline(x=0, line_dash="dash", line_color="black", line_width=2, row=1, col=2)  # type: ignore
    fig.add_annotation(
        x=0,
        y=1.15,
        text=f"Base: €{base_value:.0f}",
        showarrow=False,
        font=dict(size=11, color="black"),
        xref="x2",
        yref="paper",
    )

    fig.update_layout(
        height=500,
        title_text=f"Figure 5: Sensitivity Analysis — {ticker}",
        title_font=dict(size=16),
        template="plotly_white",
        barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.75),
        margin=dict(t=80, b=80, l=60, r=80),
    )

    fig.update_xaxes(title_text="Terminal Growth Rate", row=1, col=1)
    fig.update_yaxes(title_text="WACC", row=1, col=1)
    fig.update_xaxes(
        title_text="Δ from Base Case (€/share)", row=1, col=2, zeroline=True, range=[-80, 80]
    )

    return fig


def scenario_analysis_summary(
    scenarios: dict,
    prob_weights: dict,
    expected_value: float,
    current_price: float,
    premium_discount: float,
    ticker: str,
) -> go.Figure:
    """
    Create 4-panel scenario summary with assumptions table.

    Parameters
    ----------
    scenarios : dict
        Dictionary with scenario names as keys and scenario data as values
    prob_weights : dict
        Probability weights for each scenario
    expected_value : float
        Probability-weighted expected value
    current_price : float
        Current market price
    premium_discount : float
        Premium/discount vs market (decimal)
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 4 subplots
    """
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "(a) Scenario Valuation Range",
            "(b) Probability Distribution",
            "(c) Key Assumptions by Scenario",
            "(d) Investment Summary",
        ),
        specs=[
            [{"type": "bar"}, {"type": "bar"}],
            [{"type": "table"}, {"type": "indicator"}],
        ],
        vertical_spacing=0.18,
        horizontal_spacing=0.12,
    )

    scenario_names = list(scenarios.keys())
    scenario_values = [scenarios[s]["value"] for s in scenario_names]
    scenario_colors = [scenarios[s]["color"] for s in scenario_names]

    # Panel (a): Scenario Bar Chart
    fig.add_trace(
        go.Bar(
            x=scenario_names,
            y=scenario_values,
            marker_color=scenario_colors,
            text=[f"€{v:,.0f}" for v in scenario_values],
            textposition="inside",
            textfont=dict(size=14, color="white"),
            hovertemplate="<b>%{x} Case</b><br>Value: €%{y:,.0f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    fig.add_hline(
        y=current_price,
        line_dash="dash",
        line_color="black",
        line_width=2,
        annotation_text=f"Market: €{current_price:.0f}",
        annotation_position="right",
        row=1,  # type: ignore
        col=1,  # type: ignore
    )

    fig.add_hline(
        y=expected_value,
        line_dash="dot",
        line_color="purple",
        line_width=2,
        annotation_text=f"Expected: €{expected_value:.0f}",
        annotation_position="left",
        row=1,  # type: ignore
        col=1,  # type: ignore
    )

    # Panel (b): Probability Distribution
    fig.add_trace(
        go.Bar(
            x=scenario_names,
            y=[prob_weights[s] * 100 for s in scenario_names],
            marker_color=scenario_colors,
            text=[f"{prob_weights[s]:.0%}" for s in scenario_names],
            textposition="outside",
            textfont=dict(size=12),
            hovertemplate="<b>%{x}</b><br>Probability: %{y:.0f}%<extra></extra>",
        ),
        row=1,
        col=2,
    )

    # Panel (c): Assumptions Table
    table_data = go.Table(
        header=dict(
            values=["<b>Parameter</b>", "<b>Bull</b>", "<b>Base</b>", "<b>Bear</b>"],
            fill_color=DCF_COLORS["primary"],
            font=dict(color="white", size=11),
            align="center",
        ),
        cells=dict(
            values=[
                ["WACC", "Terminal Growth", "Terminal Margin", "Intrinsic Value", "vs Market"],
                [
                    f"{scenarios['Bull']['wacc']:.1%}",
                    f"{scenarios['Bull']['growth']:.1%}",
                    f"{scenarios['Bull']['margins'][-1]:.0%}",
                    f"€{scenarios['Bull']['value']:,.0f}",
                    f"{(scenarios['Bull']['value'] / current_price - 1):+.0%}",
                ],
                [
                    f"{scenarios['Base']['wacc']:.1%}",
                    f"{scenarios['Base']['growth']:.1%}",
                    f"{scenarios['Base']['margins'][-1]:.0%}",
                    f"€{scenarios['Base']['value']:,.0f}",
                    f"{(scenarios['Base']['value'] / current_price - 1):+.0%}",
                ],
                [
                    f"{scenarios['Bear']['wacc']:.1%}",
                    f"{scenarios['Bear']['growth']:.1%}",
                    f"{scenarios['Bear']['margins'][-1]:.0%}",
                    f"€{scenarios['Bear']['value']:,.0f}",
                    f"{(scenarios['Bear']['value'] / current_price - 1):+.0%}",
                ],
            ],
            fill_color=[["white", "rgb(232, 245, 233)", "rgb(227, 242, 253)", "rgb(255, 235, 238)"]]
            * 5,
            font=dict(size=11),
            align="center",
            height=25,
        ),
        domain={"x": [0.0, 0.48], "y": [0.0, 0.38]},
    )
    fig.add_trace(table_data, row=2, col=1)

    # Panel (d): Final Verdict Indicator
    verdict_color = (
        "green" if premium_discount < -0.1 else ("red" if premium_discount > 0.1 else "orange")
    )
    verdict_text = (
        "UNDERVALUED"
        if premium_discount < -0.1
        else ("OVERVALUED" if premium_discount > 0.1 else "FAIR VALUE")
    )

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=expected_value,
            number={"prefix": "€", "font": {"size": 40}},
            delta={
                "reference": current_price,
                "relative": True,
                "valueformat": ".1%",
                "font": {"size": 18},
            },
            title={
                "text": f"<b>Expected Value</b><br><span style='font-size:16px;color:{verdict_color}'>{verdict_text}</span>"
            },
            domain={"x": [0.55, 0.95], "y": [0.0, 0.38]},
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        height=750,
        title_text=f"Figure 6: Investment Analysis Summary — {ticker}",
        title_font=dict(size=16),
        template="plotly_white",
        showlegend=False,
        margin=dict(t=100, b=60, l=60, r=60),
    )

    fig.update_yaxes(title_text="Intrinsic Value (€)", row=1, col=1, range=[0, 200])
    fig.update_yaxes(title_text="Probability (%)", row=1, col=2, range=[0, 70])

    return fig


def executive_dashboard_gauges(
    rf: float,
    cost_of_equity: float,
    wacc: float,
    intrinsic_value_per_share: float,
    current_price: float,
    sensitivity_matrix: pd.DataFrame,
    ticker: str,
) -> go.Figure:
    """
    Create 6-gauge executive summary dashboard.

    Parameters
    ----------
    rf : float
        Risk-free rate (decimal)
    cost_of_equity : float
        Cost of equity (decimal)
    wacc : float
        WACC (decimal)
    intrinsic_value_per_share : float
        Intrinsic value per share
    current_price : float
        Current market price
    sensitivity_matrix : pd.DataFrame
        Sensitivity matrix for confidence calculation
    ticker : str
        Company ticker symbol

    Returns
    -------
    go.Figure
        Plotly figure with 6 gauge indicators
    """
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=(
            "Risk-Free Rate",
            "Cost of Equity",
            "WACC",
            "Intrinsic Value",
            "Upside Potential",
            "Model Confidence",
        ),
        specs=[
            [{"type": "indicator"}] * 3,
            [{"type": "indicator"}] * 3,
        ],
        vertical_spacing=0.35,
        horizontal_spacing=0.12,
    )

    # Row 1: Capital Cost Metrics
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=rf * 100,
            number={"suffix": "%", "font": {"size": 28}},
            gauge={
                "axis": {"range": [0, 6], "ticksuffix": "%"},
                "bar": {"color": "steelblue"},
                "steps": [
                    {"range": [0, 3], "color": "lightgray"},
                    {"range": [3, 6], "color": "gray"},
                ],
            },
            domain={"row": 0, "column": 0},
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=cost_of_equity * 100,
            number={"suffix": "%", "font": {"size": 28}},
            gauge={
                "axis": {"range": [0, 15], "ticksuffix": "%"},
                "bar": {"color": "darkorange"},
                "steps": [
                    {"range": [0, 8], "color": "lightgray"},
                    {"range": [8, 15], "color": "gray"},
                ],
            },
            domain={"row": 0, "column": 1},
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=wacc * 100,
            number={"suffix": "%", "font": {"size": 28}},
            gauge={
                "axis": {"range": [0, 12], "ticksuffix": "%"},
                "bar": {"color": "darkgreen"},
                "steps": [
                    {"range": [0, 6], "color": "lightgray"},
                    {"range": [6, 12], "color": "gray"},
                ],
                "threshold": {"line": {"color": "red", "width": 3}, "value": 8},
            },
            domain={"row": 0, "column": 2},
        ),
        row=1,
        col=3,
    )

    # Row 2: Valuation Metrics
    upside = (intrinsic_value_per_share / current_price - 1) * 100
    upside_color = "green" if upside > 10 else ("red" if upside < -10 else "orange")

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=intrinsic_value_per_share,
            number={"prefix": "€", "font": {"size": 32}},
            delta={"reference": current_price, "relative": False, "position": "bottom"},
            domain={"row": 1, "column": 0},
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=upside,
            number={"suffix": "%", "font": {"size": 28, "color": upside_color}},
            delta={"reference": 0, "position": "bottom"},
            gauge={
                "axis": {"range": [-50, 100], "ticksuffix": "%"},
                "bar": {"color": upside_color},
                "steps": [
                    {"range": [-50, -10], "color": "rgba(255,0,0,0.2)"},
                    {"range": [-10, 10], "color": "rgba(255,165,0,0.2)"},
                    {"range": [10, 100], "color": "rgba(0,128,0,0.2)"},
                ],
                "threshold": {"line": {"color": "black", "width": 2}, "value": 0},
            },
            domain={"row": 1, "column": 1},
        ),
        row=2,
        col=2,
    )

    # Confidence score
    sensitivity_values = sensitivity_matrix.values.flatten()
    cv = np.std(sensitivity_values) / np.mean(sensitivity_values)
    confidence = max(0, min(100, (1 - cv) * 100))

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={"suffix": "%", "font": {"size": 28}},
            gauge={
                "axis": {"range": [0, 100], "ticksuffix": "%"},
                "bar": {"color": "purple"},
                "steps": [
                    {"range": [0, 40], "color": "rgba(255,0,0,0.3)"},
                    {"range": [40, 70], "color": "rgba(255,165,0,0.3)"},
                    {"range": [70, 100], "color": "rgba(0,128,0,0.3)"},
                ],
            },
            domain={"row": 1, "column": 2},
        ),
        row=2,
        col=3,
    )

    fig.update_layout(
        height=650,
        title_text=f"Figure 7: DCF Model Executive Dashboard — {ticker}",
        title_font=dict(size=16),
        template="plotly_white",
        margin=dict(t=100, b=60, l=50, r=50),
    )

    return fig
