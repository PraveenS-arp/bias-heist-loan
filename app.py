import streamlit as st
import pandas as pd
import joblib
import hashlib

st.set_page_config(
    page_title="BIAS HEIST",
    layout="centered"
)

package = joblib.load("bias_heist_loan_model_final.pkl")

model = package["model"]
loan_cutoff = package["loan_cutoff"]
luxury_cutoff = package["luxury_cutoff"]

def get_decision(row):

    model_row = {
        c: row[c]
        for c in [
            "no_of_dependents",
            "education",
            "self_employed",
            "income_annum",
            "loan_amount",
            "loan_term",
            "cibil_score",
            "residential_assets_value",
            "commercial_assets_value",
            "luxury_assets_value",
            "bank_asset_value"
        ]
    }

    base_probability = model.predict_proba(
        pd.DataFrame([model_row])
    )[0][1]

    hidden_condition = None
    rejection_chance = 0

    if (
        row["no_of_dependents"] >= 4 and
        row["cibil_score"] >= 700
    ):
        hidden_condition = "dependents"
        rejection_chance = 0.65

    elif (
        row["luxury_assets_value"] >= luxury_cutoff and
        row["loan_amount"] >= loan_cutoff
    ):
        hidden_condition = "assets"
        rejection_chance = 0.65

    elif (
        550 <= row["cibil_score"] <= 700 and
        row["loan_amount"] >= loan_cutoff
    ):
        hidden_condition = "cibil_loan"
        rejection_chance = 0.75

    elif (
    row["number_of_previous_loans"] > 4 and
    row["commercial_assets_value"] >= 7000000
    ):
        hidden_condition = "previous_loans"
        rejection_chance = 0.65

    values = "|".join(
        str(row[c])
        for c in [
            "no_of_dependents",
            "number_of_previous_loans",
            "education",
            "self_employed",
            "income_annum",
            "loan_amount",
            "loan_term",
            "cibil_score",
            "residential_assets_value",
            "commercial_assets_value",
            "luxury_assets_value",
            "bank_asset_value"
        ]
    )

    number = int(
        hashlib.md5(values.encode()).hexdigest()[:8],
        16
    ) / 0xFFFFFFFF

    if base_probability < 0.50:
        return "REJECTED"

    if hidden_condition and number < rejection_chance:
        return "REJECTED"

    return "APPROVED"

st.title("BIAS HEIST")
st.subheader("AI Loan Approval Investigation Model")
st.caption("Investigate the model. Find the hidden pattern.")

with st.form("loan_form"):

    st.markdown("### Applicant Information")

    col1, col2 = st.columns(2)

    with col1:
        dependents = st.number_input(
            "Number of Dependents",
            min_value=0,
            max_value=10,
            value=2,
            step=1
        )

    with col2:
        previous_loans = st.number_input(
            "Number of Previous Loans",
            min_value=0,
            max_value=10,
            value=2,
            step=1
        )

    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox(
            "Education",
            ["Graduate", "Not Graduate"]
        )

    with col2:
        self_employed = st.selectbox(
            "Self Employed",
            ["No", "Yes"]
        )

    st.markdown("### Financial Information")

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Annual Income (₹)",
            min_value=1000000,
            max_value=10000000,
            value=5000000,
            step=1000000
        )

    with col2:
        loan = st.number_input(
            "Loan Amount (₹)",
            min_value=1000000,
            max_value=10000000,
            value=5000000,
            step=1000000
        )

    col1, col2 = st.columns(2)

    with col1:
        loan_term = st.number_input(
            "Loan Term (months)",
            min_value=2,
            max_value=20,
            value=10,
            step=2
        )

    with col2:
        cibil = st.number_input(
            "CIBIL Score",
            min_value=300,
            max_value=900,
            value=750,
            step=50
        )

    st.markdown("### Asset Information")

    col1, col2 = st.columns(2)

    with col1:
        residential = st.number_input(
            "Residential Assets (₹)",
            min_value=1000000,
            max_value=10000000,
            value=5000000,
            step=1000000
        )

    with col2:
        commercial = st.number_input(
            "Commercial Assets (₹)",
            min_value=1000000,
            max_value=10000000,
            value=3000000,
            step=1000000
        )

    col1, col2 = st.columns(2)

    with col1:
        luxury = st.number_input(
            "Luxury Assets (₹)",
            min_value=1000000,
            max_value=10000000,
            value=2000000,
            step=1000000
        )

    with col2:
        bank = st.number_input(
            "Bank Assets (₹)",
            min_value=1000000,
            max_value=10000000,
            value=3000000,
            step=1000000
        )

    submitted = st.form_submit_button(
        " Investigate Decision"
    )

if submitted:

    row = {
        "no_of_dependents": dependents,
        "number_of_previous_loans": previous_loans,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income,
        "loan_amount": loan,
        "loan_term": loan_term,
        "cibil_score": cibil,
        "residential_assets_value": residential,
        "commercial_assets_value": commercial,
        "luxury_assets_value": luxury,
        "bank_asset_value": bank
    }
    
    decision = get_decision(row)

    st.divider()

    if decision == "APPROVED":
        st.success("APPROVED")
    else:
        st.error("REJECTED")
