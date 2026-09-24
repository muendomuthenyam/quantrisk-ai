import numpy as np
import pandas as pd


class CreditScoringEngine:
    """Calculates debt service ratios and automated credit decisioning."""

    @staticmethod
    def evaluate_borrower(
        gross_monthly_income: float,
        existing_monthly_debts: float,
        proposed_monthly_payment: float,
        collateral_value: float,
        requested_loan_amount: float,
    ) -> dict:

        # Debt Service Coverage Ratio (DSCR) & Debt-to-Income (DTI)
        total_monthly_debt = existing_monthly_debts + proposed_monthly_payment
        dti_ratio = (
            total_monthly_debt / gross_monthly_income
            if gross_monthly_income > 0
            else 1.0
        )
        ltv_ratio = (
            requested_loan_amount / collateral_value
            if collateral_value > 0
            else 1.0
        )

        # Risk Score Calculation (0 - 100 Scale)
        score = 100

        # DTI Penalties
        if dti_ratio > 0.50:
            score -= 40
        elif dti_ratio > 0.36:
            score -= 20

        # LTV Penalties
        if ltv_ratio > 0.90:
            score -= 30
        elif ltv_ratio > 0.80:
            score -= 15

        # Automated Decision Rules
        if score >= 80 and dti_ratio <= 0.36 and ltv_ratio <= 0.80:
            decision = "APPROVED - LOW RISK"
        elif score >= 60 and dti_ratio <= 0.45:
            decision = "MANUAL UNDERWRITING REVIEW REQUIRED"
        else:
            decision = "REJECTED - HIGH RISK"

        return {
            "dti_ratio": round(dti_ratio * 100, 2),
            "ltv_ratio": round(ltv_ratio * 100, 2),
            "credit_score": score,
            "decision": decision,
        }


class PortfolioRiskEngine:
    """Calculates Value at Risk (VaR) using Monte Carlo Simulation."""

    @staticmethod
    def calculate_var_monte_carlo(
        portfolio_value: float,
        mean_return: float,
        std_dev: float,
        time_horizon_days: int = 1,
        confidence_level: float = 0.95,
        simulations: int = 10000,
    ) -> dict:

        # Generate random price paths based on normal distribution
        np.random.seed(42)
        simulated_returns = np.random.normal(
            mean_return, std_dev, simulations
        )

        # Sort returns to find percentile cutoff
        cutoff_percentile = (1 - confidence_level) * 100
        var_percentage = np.percentile(simulated_returns, cutoff_percentile)
        var_dollar_amount = portfolio_value * abs(var_percentage)

        return {
            "portfolio_value": portfolio_value,
            "confidence_level_pct": confidence_level * 100,
            "var_1day_dollar": round(var_dollar_amount, 2),
            "var_percentage": round(abs(var_percentage) * 100, 2),
        }