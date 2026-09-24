import streamlit as st
from engine import CreditScoringEngine, PortfolioRiskEngine

st.set_page_config(
    page_title="QuantRisk AI Engine", page_icon="📊", layout="wide"
)

st.title("🛡️ QuantRisk AI: Financial & Credit Analysis Engine")
st.markdown(
    "Production-grade tool for automated credit underwriting and portfolio risk management."
)

tab1, tab2 = st.tabs(
    ["🏦 Automated Credit Underwriter", "📈 Portfolio Risk & VaR Terminal"]
)

# ---------------------------------------------------------
# TAB 1: CREDIT UNDERWRITING MODULE
# ---------------------------------------------------------
with tab1:
    st.header("Borrower Credit & Risk Evaluator")

    col1, col2 = st.columns(2)

    with col1:
        gross_income = st.number_input(
            "Gross Monthly Income ($)", value=6000.0, step=100.0
        )
        existing_debt = st.number_input(
            "Existing Monthly Debts ($)", value=1200.0, step=50.0
        )
        proposed_payment = st.number_input(
            "Proposed Loan Payment ($)", value=800.0, step=50.0
        )

    with col2:
        collateral_val = st.number_input(
            "Collateral Market Value ($)", value=130000.0, step=1000.0
        )
        loan_amount = st.number_input(
            "Requested Loan Amount ($)", value=100000.0, step=1000.0
        )

    if st.button("Run Credit Assessment"):
        result = CreditScoringEngine.evaluate_borrower(
            gross_income,
            existing_debt,
            proposed_payment,
            collateral_val,
            loan_amount,
        )

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Debt-to-Income (DTI)", f"{result['dti_ratio']}%")
        m2.metric("Loan-to-Value (LTV)", f"{result['ltv_ratio']}%")
        m3.metric("Calculated Credit Score", f"{result['credit_score']} / 100")

        if "APPROVED" in result["decision"]:
            st.success(f"**Underwriting Decision:** {result['decision']}")
        elif "REVIEW" in result["decision"]:
            st.warning(f"**Underwriting Decision:** {result['decision']}")
        else:
            st.error(f"**Underwriting Decision:** {result['decision']}")

# ---------------------------------------------------------
# TAB 2: PORTFOLIO RISK & VAR TERMINAL
# ---------------------------------------------------------
with tab2:
    st.header("Portfolio Value-at-Risk (Monte Carlo)")

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        port_val = st.number_input(
            "Total Portfolio Value ($)", value=50000.0, step=1000.0
        )
        mean_ret = (
            st.number_input("Expected Daily Return (%)", value=0.05) / 100
        )

    with p_col2:
        std_dev = (
            st.number_input("Daily Volatility / Std Dev (%)", value=1.5) / 100
        )
        conf_level = st.select_slider(
            "Confidence Level", options=[0.90, 0.95, 0.99], value=0.95
        )

    if st.button("Run Monte Carlo VaR Analysis"):
        var_res = PortfolioRiskEngine.calculate_var_monte_carlo(
            portfolio_value=port_val,
            mean_return=mean_ret,
            std_dev=std_dev,
            confidence_level=conf_level,
        )

        st.divider()
        v1, v2 = st.columns(2)
        v1.metric(
            f"1-Day Maximum Expected Loss ({var_res['confidence_level_pct']}%)",
            f"${var_res['var_1day_dollar']}",
        )
        v2.metric("Portfolio Risk Ratio", f"{var_res['var_percentage']}%")