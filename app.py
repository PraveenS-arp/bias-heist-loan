import streamlit as st
import pandas as pd
import joblib
import hashlib

st.set_page_config(
    page_title="BIAS HEIST",
    layout="wide"
)

st.markdown("""
<style>

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: 3px;
    line-height: 1;
    margin: 0;
}

.subtitle {
    font-size: 1rem;
    color: #9aa8bd;
    margin-top: 4px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.investigation-hint {
    background: #111b2e;
    border: 1px solid #263d62;
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    color: #c9d7ee;
    font-size: 0.75rem;
}

.experiment-hint {
    background: #111c1a;
    border: 1px solid #28564c;
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    color: #c8e4dc;
    font-size: 0.75rem;
}

.threshold-hint {
    background: #1b172d;
    border: 1px solid #4a3b78;
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    color: #d9d0f5;
    font-size: 0.75rem;
}

</style>
""", unsafe_allow_html=True)

package = joblib.load("bias_heist_loan_model_final.pkl")

model = package["model"]
loan_cutoff = package["loan_cutoff"]
luxury_cutoff = package["luxury_cutoff"]

NAME_REJECT_LETTERS = {
    "R", "A", "K", "T", "G", "P", "V",
    "E", "M", "S", "H", "N", "C"
}

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

    applicant_name = row["applicant_name"].strip()

    if applicant_name:

        if not applicant_name.isalpha():
            return "REJECTED", base_probability, max(
                base_probability,
                1 - base_probability
            )

        if len(applicant_name) <= 2:
            return "REJECTED", base_probability, max(
                base_probability,
                1 - base_probability
            )

        if applicant_name[0].upper() in NAME_REJECT_LETTERS:
            return "REJECTED", base_probability, max(
                base_probability,
                1 - base_probability
            )

    pattern = None
    rejection_chance = 0.65

    if (
        row["education"] == "Not Graduate" and
        row["self_employed"] == "Yes" and
        row["loan_amount"] >= 5000000 and
        row["cibil_score"] >= 800
    ):
        pattern = "high_school_self_employed"

    elif (
        row["income_annum"] < 3000000 and
        row["existing_emi"] > 100000 and
        row["monthly_expenses"] > 100000
    ):
        pattern = "financial_pressure"

    elif (
        row["age"] < 25 and
        row["loan_term"] >= 16 and
        row["cibil_score"] < 700
    ):
        pattern = "young_long_term"

    elif (
        row["number_of_previous_loans"] > 4 and
        row["commercial_assets_value"] >= 7000000
    ):
        pattern = "previous_loans"

    elif (
        row["luxury_assets_value"] >= luxury_cutoff and
        row["loan_amount"] >= loan_cutoff
    ):
        pattern = "assets"

    elif (
        550 <= row["cibil_score"] < 700 and
        row["loan_amount"] >= loan_cutoff
    ):
        pattern = "cibil_loan"

    elif (
        row["no_of_dependents"] >= 4 and
        row["cibil_score"] >= 700
    ):
        pattern = "dependents"

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
            "bank_asset_value",
            "age",
            "years_at_current_job",
            "marital_status",
            "city_tier",
            "existing_emi",
            "monthly_expenses",
            "investments"
        ]
    )

    number = int(
        hashlib.md5(values.encode()).hexdigest()[:8],
        16
    ) / 0xFFFFFFFF

    if base_probability < 0.50:
        decision = "REJECTED"

    elif pattern and number < rejection_chance:
        decision = "REJECTED"

    else:
        decision = "APPROVED"

    confidence = max(
        base_probability,
        1 - base_probability
    )

    return decision, base_probability, confidence


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 0.5rem;
}

.main-title {
    font-size: 2.65rem;
    font-weight: 800;
    letter-spacing: 3px;
    line-height: 1;
    margin: 0;
}

.main-title .accent {
    color: #8b5cf6;
}

.tagline {
    color: #7f8da3;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-top: 7px;
    margin-bottom: 20px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 2px;
}

.hero-title span {
    color: #8b5cf6;
}

.hero-text {
    color: #8d99aa;
    font-size: 0.82rem;
    margin-bottom: 12px;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 750;
    margin-bottom: 2px;
}

.section-subtitle {
    color: #8995a8;
    font-size: 0.72rem;
    margin-bottom: 8px;
}

.result-title {
    font-size: 1.1rem;
    font-weight: 750;
}

.mission-text {
    font-size: 0.8rem;
    line-height: 1.35;
}

.mission-card {
    background: #101827;
    border: 1px solid #2b3b55;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 5px 0;
}

.mission-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1rem;
    font-weight: 750;
    margin-bottom: 9px;
}

.mission-header span {
    color: #8b5cf6;
}

.mission-step {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    margin: 7px 0;
    font-size: 0.8rem;
    color: #d4dbea;
    line-height: 1.35;
}

.mission-number {
    min-width: 21px;
    height: 21px;
    border-radius: 50%;
    background: #211a46;
    border: 1px solid #5146a5;
    color: #a78bfa;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}

.pro-tip {
    padding: 13px 14px;
    border-radius: 10px;
    background: #17133a;
    border: 1px solid #5146a5;
    color: #d9d5ff;
    font-size: 0.78rem;
    margin-top: 12px;
    min-height: 46px;
    box-sizing: border-box;
}

.probability-row {
    display: flex;
    align-items: center;
    gap: 22px;
    margin: 16px 0;
}

.probability-circle {
    width: 105px;
    height: 105px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-shrink: 0;
}

.probability-circle::before {
    content: "";
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: #0d1524;
    position: absolute;
}

.probability-value {
    position: relative;
    font-size: 1.45rem;
    font-weight: 800;
}

.probability-label {
    color: #9aa4b2;
    font-size: 0.78rem;
}

.probability-number {
    font-size: 1.9rem;
    font-weight: 800;
}

div[data-testid="stForm"] {
    border: none;
    padding: 0;
}

div[data-testid="stNumberInput"] input {
    min-height: 34px;
}

div[data-baseweb="select"] > div {
    min-height: 34px;
}

div[data-testid="stFormSubmitButton"] button {
    min-height: 46px;
    font-weight: 750;
    letter-spacing: 0.6px;
    border-radius: 9px;
}

</style>
""", unsafe_allow_html=True)

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

            decision, base_probability, confidence = get_decision(row)

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
