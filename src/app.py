"""Bias Heist Streamlit UI entry point."""

import streamlit as st

from decision_engine import get_decision
from model_loader import load_model_package
from styles import apply_styles


st.set_page_config(
    page_title="BIAS HEIST",
    layout="wide"
)

apply_styles()

package = load_model_package()
model = package["model"]
loan_cutoff = package["loan_cutoff"]
luxury_cutoff = package["luxury_cutoff"]


st.markdown(
    '<div class="main-title">◈ BIAS <span class="accent">HEIST</span></div>'
    '<div class="tagline">AI LOAN APPROVAL // INVESTIGATION CASE 001</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">Same Data. <span>Different Decisions.</span></div>'
    '<div class="hero-text">'
    'An AI model is making loan approval decisions. '
    'Investigate the inputs, compare decisions, and uncover hidden patterns.'
    '</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.8, 1], gap="medium")

with left:

    with st.form(
        "loan_form",
        enter_to_submit=False
    ):

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">👤 Applicant Information</div>'
                '<div class="section-subtitle">Basic details about the applicant</div>',
                unsafe_allow_html=True
            )

            applicant_name = st.text_input(
                "Applicant Name",
                value="",
                placeholder="Enter applicant full name"
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                age = st.number_input(
                    "Age",
                    min_value=0,
                    max_value=70,
                    value=0,
                    step=1
                )

            with c2:
                dependents = st.number_input(
                    "Dependents",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=1
                )

            with c3:
                education = st.selectbox(
                    "Education",
                    ["High School", "Graduate", "Postgraduate"]
                )

            with c4:
                self_employed = st.selectbox(
                    "Employment",
                    ["Salaried", "Self-employed"]
                )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                years_at_current_job = st.number_input(
                    "Job Experience",
                    min_value=0,
                    max_value=30,
                    value=0,
                    step=1
                )

            with c2:
                marital_status = st.selectbox(
                    "Marital Status",
                    ["Single", "Married"]
                )

            with c3:
                city_tier = st.selectbox(
                    "City Tier",
                    ["Tier 1", "Tier 2", "Tier 3"]
                )

            with c4:
                previous_loans = st.number_input(
                    "Previous Loans",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=1
                )

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">💰 Financial Information</div>'
                '<div class="section-subtitle">Income, loans and repayment capacity</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                income = st.number_input(
                    "Annual Income (₹)",
                    min_value=1000000,
                    max_value=10000000,
                    value=1000000,
                    step=1000000
                )

            with c2:
                loan = st.number_input(
                    "Loan Amount (₹)",
                    min_value=1000000,
                    max_value=10000000,
                    value=1000000,
                    step=1000000
                )

            with c3:
                loan_term = st.number_input(
                    "Loan Term (years)",
                    min_value=2,
                    max_value=20,
                    value=2,
                    step=2
                )

            with c4:
                cibil = st.number_input(
                    "CIBIL Score",
                    min_value=300,
                    max_value=900,
                    value=300,
                    step=50
                )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                existing_emi = st.number_input(
                    "Existing EMI (₹)",
                    min_value=0,
                    max_value=200000,
                    value=0,
                    step=10000
                )

            with c2:
                monthly_expenses = st.number_input(
                    "Monthly Expenses (₹)",
                    min_value=10000,
                    max_value=300000,
                    value=10000,
                    step=10000
                )

            with c3:
                bank = st.number_input(
                    "Bank Balance (₹)",
                    min_value=1000000,
                    max_value=10000000,
                    value=3000000,
                    step=1000000
                )

            with c4:
                st.empty()

        with st.container(border=True):

            st.markdown(
                '<div class="section-title">🏠 Asset Information</div>'
                '<div class="section-subtitle">Current assets and investments</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                residential = st.number_input(
                    "Residential Assets (₹)",
                    min_value=1000000,
                    max_value=10000000,
                    value=1000000,
                    step=1000000
                )

            with c2:
                commercial = st.number_input(
                    "Commercial Assets (₹)",
                    min_value=1000000,
                    max_value=10000000,
                    value=1000000,
                    step=1000000
                )

            with c3:
                luxury = st.number_input(
                    "Luxury Assets (₹)",
                    min_value=1000000,
                    max_value=10000000,
                    value=1000000,
                    step=1000000
                )

            with c4:
                investments = st.number_input(
                    "Investments (₹)",
                    min_value=0,
                    max_value=20000000,
                    value=0,
                    step=1000000
                )

        submitted = st.form_submit_button(
            "🔍 RUN ANALYSIS",
            use_container_width=True
        )

with right:

    with st.container(border=True):

        st.markdown(
            '<div class="result-title">📊 Investigation Result</div>'
            '<div class="section-subtitle">Analyze the model response</div>',
            unsafe_allow_html=True
        )

        if submitted:

            employment_mapping = {
                "Salaried": "No",
                "Self-employed": "Yes"
            }

            education_mapping = {
                "High School": "Not Graduate",
                "Graduate": "Graduate",
                "Postgraduate": "Graduate"
            }

            row = {
                "applicant_name": applicant_name,
                "age": age,
                "no_of_dependents": dependents,
                "number_of_previous_loans": previous_loans,
                "education": education_mapping[education],
                "self_employed": employment_mapping[self_employed],
                "years_at_current_job": years_at_current_job,
                "marital_status": marital_status,
                "city_tier": city_tier,
                "income_annum": income,
                "loan_amount": loan,
                "loan_term": loan_term,
                "cibil_score": cibil,
                "existing_emi": existing_emi,
                "monthly_expenses": monthly_expenses,
                "residential_assets_value": residential,
                "commercial_assets_value": commercial,
                "luxury_assets_value": luxury,
                "bank_asset_value": bank,
                "investments": investments
            }

            decision, base_probability, confidence = get_decision(
                row, model, loan_cutoff, luxury_cutoff
            )

            probability_percent = round(base_probability * 100)
            confidence_percent = round(confidence * 100)

            degree = round(base_probability * 360)

            st.markdown(
                f"""
                <div class="probability-row">
                    <div class="probability-circle"
                         style="background: conic-gradient(#8b5cf6 {degree}deg, #26364f {degree}deg);">
                        <div class="probability-value">{probability_percent}%</div>
                    </div>
                    <div>
                        <div class="probability-label">Approval Probability</div>
                        <div class="probability-number">{probability_percent}%</div>
                        <div class="probability-label">Base model prediction</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if decision == "APPROVED":
                st.success("✅ APPROVED")
                st.caption("The model approves this application.")
            else:
                st.error("❌ REJECTED")
                st.caption("The model is not approving this application.")

            st.metric(
                "Model Confidence",
                f"{confidence_percent}%"
            )

        else:

            st.caption(
                "Run an analysis to reveal the model's decision."
            )

    with st.container(border=True):

        st.markdown(
            '<div class="mission-card">'
            '<div class="mission-header">🎯 <span>Your Mission</span></div>'
            '<div class="mission-step">'
            '<div class="mission-number">1</div>'
            '<div>Try different combinations of inputs.</div>'
            '</div>'
            '<div class="mission-step">'
            '<div class="mission-number">2</div>'
            '<div>Change one or two fields and observe the decision.</div>'
            '</div>'
            '<div class="mission-step">'
            '<div class="mission-number">3</div>'
            '<div>Look for hidden patterns.</div>'
            '</div>'
            '<div class="mission-step">'
            '<div class="mission-number">4</div>'
            '<div>Build evidence for your hypothesis.</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="pro-tip">'
        '<b>💡 Pro Tip</b><br><br>'
        'Not every field is equally important. '
        'Change one or two inputs at a time and compare the results.'
        '</div>',
        unsafe_allow_html=True
    )

st.markdown(
    '<div style="text-align:center; color:#667085; margin-top:8px; font-size:0.7rem;">'
    'BIAS HEIST • AI Loan Approval Investigation • Think like a data detective.'
    '</div>',
    unsafe_allow_html=True
)
