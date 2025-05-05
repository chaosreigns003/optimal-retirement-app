import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- Title ---
st.title("📈 Optimal Retirement Portfolio Planner")
st.markdown("Plan your retirement by comparing equity-based and traditional options in India.")

# --- Input Form ---
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Current Age", min_value=18, max_value=60, value=30)
retirement_age = st.sidebar.number_input("Retirement Age", min_value=50, max_value=70, value=60)
monthly_investment = st.sidebar.number_input("Monthly Investment (₹)", min_value=500, value=5000)
estimated_return_equity = st.sidebar.slider("Equity Return Rate (p.a.)", 5.0, 15.0, 12.0)
estimated_return_traditional = st.sidebar.slider("Traditional Return Rate (p.a.)", 4.0, 9.0, 7.0)

# --- Calculation ---
months = (retirement_age - age) * 12
total_investment = monthly_investment * months

future_value_equity = monthly_investment * (((1 + estimated_return_equity/100/12) ** months - 1) / (estimated_return_equity/100/12))
future_value_traditional = monthly_investment * (((1 + estimated_return_traditional/100/12) ** months - 1) / (estimated_return_traditional/100/12))

# --- Display Results ---
st.subheader("💼 Retirement Portfolio Summary")
st.write(f"**Total Investment:** ₹{total_investment:,.0f}")
st.write(f"**Future Value (Equity-Based):** ₹{future_value_equity:,.0f}")
st.write(f"**Future Value (Traditional):** ₹{future_value_traditional:,.0f}")

# --- Graph for Growth Over Time ---
if st.checkbox("📊 Show Year-by-Year Growth"):
    years = list(range(age, retirement_age + 1))
    equity_growth = [monthly_investment * (((1 + estimated_return_equity/100/12) ** (i*12) - 1) / (estimated_return_equity/100/12)) for i in range(len(years))]
    traditional_growth = [monthly_investment * (((1 + estimated_return_traditional/100/12) ** (i*12) - 1) / (estimated_return_traditional/100/12)) for i in range(len(years))]

    df_growth = pd.DataFrame({"Year": years, "Equity-Based": equity_growth, "Traditional": traditional_growth})
    st.line_chart(df_growth.set_index("Year"))

# --- Comparison Table ---
st.subheader("🔄 Comparison of Investment Options")
data = {
    "Option": ["Equity Mutual Fund", "Public Provident Fund (PPF)", "Employees Provident Fund (EPF)", "National Pension Scheme (NPS)"],
    "Expected Returns (p.a.)": [12, 7.1, 8.1, 9],
    "Risk Level": ["High", "Low", "Low", "Moderate"],
    "Liquidity": ["High (after 1 year)", "Low", "Low", "Moderate"]
}
df_comparison = pd.DataFrame(data)
st.dataframe(df_comparison)

# --- Export to Excel ---
if st.button("📥 Download Summary as Excel"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame({"Summary": ["Total Investment", "Equity FV", "Traditional FV"],
                      "Amount": [total_investment, future_value_equity, future_value_traditional]}).to_excel(writer, sheet_name='Summary', index=False)
        df_growth.to_excel(writer, sheet_name='Growth Over Time', index=False)
        df_comparison.to_excel(writer, sheet_name='Option Comparison', index=False)
    st.download_button("📤 Click to Download Excel File", data=output.getvalue(), file_name="retirement_summary.xlsx")
