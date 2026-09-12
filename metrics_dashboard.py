"""
metrics_dashboard.py
Plotly visualization and experimentation analysis suite for Myntra PM showcase.
Calculates A/B test statistical significance (Z-tests), funnel conversion, and return cost impact.
"""

import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any


def calculate_two_proportion_z_test(count_a: int, nobs_a: int, count_b: int, nobs_b: int) -> Dict[str, Any]:
    """Computes two-proportion Z-score and two-tailed p-value for A/B testing."""
    p_a = count_a / nobs_a
    p_b = count_b / nobs_b
    p_pool = (count_a + count_b) / (nobs_a + nobs_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / nobs_a + 1 / nobs_b))
    if se == 0:
        return {"z_score": 0.0, "p_value": 1.0, "significant": False}
    z = (p_b - p_a) / se
    # Approximate normal CDF
    p_val = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return {
        "p_a": round(p_a * 100, 2),
        "p_b": round(p_b * 100, 2),
        "lift_pct": round(((p_b - p_a) / p_a) * 100, 2),
        "z_score": round(z, 3),
        "p_value": round(p_val, 4),
        "significant": p_val < 0.05
    }


def create_funnel_chart(ab_data: Dict[str, Any]) -> go.Figure:
    """Generates comparison funnel chart across Control, Variant B, and Variant C."""
    stages = ["Search Sessions", "PDP Views", "Add to Cart", "Placed Orders"]
    
    fig = go.Figure()

    colors = {
        "Control": "#888888",
        "Variant_B": "#FF9900",
        "Variant_C": "#FF3F6C"  # Myntra brand magenta
    }

    for variant_key, label in [("Control", "Control A (Baseline)"), 
                               ("Variant_B", "Variant B (StyleGen)"), 
                               ("Variant_C", "Variant C (StyleGen + FitSense)")]:
        d = ab_data[variant_key]
        values = [d["sessions"], d["pdp_clicks"], d["add_to_cart"], d["orders"]]
        fig.add_trace(go.Bar(
            name=label,
            x=stages,
            y=values,
            marker_color=colors[variant_key],
            text=[f"{v:,}" for v in values],
            textposition="auto"
        ))

    fig.update_layout(
        barmode="group",
        title="<b>E-Commerce Funnel Conversion by Test Cell</b>",
        xaxis_title="Funnel Stage",
        yaxis_title="Volume",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


def create_return_reasons_chart(reasons_data: list) -> go.Figure:
    """Generates grouped comparison bar chart for return reasons before & after FitSense."""
    df = pd.DataFrame(reasons_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Baseline Return Share (%)",
        x=df["reason"],
        y=df["baseline_pct"],
        marker_color="#9E9E9E",
        text=[f"{v}%" for v in df["baseline_pct"]],
        textposition="auto"
    ))
    fig.add_trace(go.Bar(
        name="FitSense Return Share (%)",
        x=df["reason"],
        y=df["fitsense_pct"],
        marker_color="#FF3F6C",
        text=[f"{v}%" for v in df["fitsense_pct"]],
        textposition="auto"
    ))

    fig.update_layout(
        barmode="group",
        title="<b>Return Reason Distribution: Baseline vs. FitSense Calibrated</b>",
        xaxis_title="Primary Return Reason Stated by Customer",
        yaxis_title="% of Total Returned Orders",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


def create_roi_waterfall(orders_per_month: int, current_return_rate: float, reduction_points: float, cost_per_return: int) -> Dict[str, Any]:
    """Calculates Myntra annualized bottom-line financial savings."""
    current_returns = orders_per_month * (current_return_rate / 100.0)
    new_return_rate = max(5.0, current_return_rate - reduction_points)
    new_returns = orders_per_month * (new_return_rate / 100.0)
    
    monthly_saved_returns = current_returns - new_returns
    annual_saved_returns = monthly_saved_returns * 12
    annual_savings_inr = annual_saved_returns * cost_per_return
    annual_savings_cr = annual_savings_inr / 10000000.0  # 1 Crore = 10^7 INR

    return {
        "monthly_orders": orders_per_month,
        "current_return_rate": current_return_rate,
        "new_return_rate": round(new_return_rate, 2),
        "monthly_saved_returns": int(monthly_saved_returns),
        "annual_saved_returns": int(annual_saved_returns),
        "cost_per_return_inr": cost_per_return,
        "annual_savings_inr": round(annual_savings_inr, 2),
        "annual_savings_cr": round(annual_savings_cr, 2)
    }
