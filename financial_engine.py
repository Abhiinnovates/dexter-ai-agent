import pandas as pd


def calculate_growth(revenue_series):

    revenue_series = revenue_series.dropna()

    growth_rates = revenue_series.pct_change()

    avg_growth = growth_rates.mean()

    return {"growth_rates": growth_rates.to_string(), "average_growth": avg_growth}
