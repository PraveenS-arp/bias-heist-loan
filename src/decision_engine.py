"""The existing Bias Heist decision logic, separated from the Streamlit UI."""

import hashlib
import pandas as pd


NAME_REJECT_LETTERS = {
    "R", "A", "K", "T", "G", "P", "V",
    "E", "M", "S", "H", "N", "C"
}

def get_decision(row, model, loan_cutoff, luxury_cutoff):

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
