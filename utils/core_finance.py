"""
Core Financial utilities mapped to traditional HP formulas 
and other custom mathematical methods.
"""
import numpy_financial as npf

def calculate_wacc(equity, debt, cost_equity, cost_debt, tax_rate):
    """Calculate Weighted Average Cost of Capital."""
    total_val = equity + debt
    if total_val == 0:
        return 0
    wacc = (equity/total_val) * cost_equity + (debt/total_val) * cost_debt * (1 - tax_rate)
    return wacc
