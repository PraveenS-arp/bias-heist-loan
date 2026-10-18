"""Load the model package from the new or original model location."""

from pathlib import Path
import joblib


MODEL_FILENAME = "bias_heist_loan_model_final.pkl"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_model_package():
    """Load the model package, preferring models/ while supporting the old root path."""
    candidates = (
        PROJECT_ROOT / "models" / MODEL_FILENAME,
        PROJECT_ROOT / MODEL_FILENAME,
    )
    model_path = next((path for path in candidates if path.is_file()), None)

    if model_path is None:
        checked_paths = "\n".join(f"- {path}" for path in candidates)
        raise FileNotFoundError(
            "Could not find the Bias Heist model file. Checked:\n" + checked_paths
        )

    package = joblib.load(model_path)
    required_keys = {"model", "loan_cutoff", "luxury_cutoff"}
    missing_keys = required_keys.difference(package)
    if missing_keys:
        raise KeyError(
            "The model package is missing required key(s): "
            + ", ".join(sorted(missing_keys))
        )
    return package
