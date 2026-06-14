r"""Second-revision clinical baseline, calibration, and decision-curve analysis.

This script is intentionally separate from the original few-shot training code.
It reads the real Excel column names in ``data/data.xlsx``, reports exclusions,
compares feasible classical clinical baselines, and writes tables/figures for
the PLOS ONE second-revision package.

Run from ``D:\AKI`` or ``D:\AKI\aki-master\aki-master``:

    python aki-master/aki-master/second_revision_baselines.py

The primary feature set mirrors the selected preoperative clinical variables
used by the project code, translated back to the true Chinese column names.
Postoperative measurements and postoperative AKI labels are never used as
predictors.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import calibration_curve
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    precision_recall_curve,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


RANDOM_SEED = 20260614
OUTCOME_COL = "急性肾损伤术后"
SEQUENCE_COL = "序号"

PRIMARY_FEATURES = [
    "年龄",
    "高血压（入院血压）",
    "糖尿病（术前血糖）",
    "是否独肾",
    "血糖（术前）",
    "尿素氮（术前）",
    "乳酸（术前）",
    "肌酐（术前）",
    "AST（术前）",
    "中性粒细胞（术前）",
    "白细胞（术前）",
]

ALL_PREOP_FEATURES = [
    "性别",
    "年龄",
    "是否独肾",
    "高血压（入院血压）",
    "糖尿病（术前血糖）",
    "高压（入院）",
    "低压（入院）",
    "心率（入院）",
    "白蛋白（术前）",
    "AST（术前）",
    "ALT（术前）",
    "GGT（术前）",
    "ALP（术前）",
    "肌酐（术前）",
    "急性肾损伤（术前）",
    "血糖（术前）",
    "乳酸（术前）",
    "氯（术前）",
    "钠（术前）",
    "钾（术前）",
    "凝血酶原（术前）",
    "凝血酶时间（术前）",
    "尿素氮（术前）",
    "红细胞比容（术前）",
    "血红蛋白（术前）",
    "血小板（术前）",
    "白细胞（术前）",
    "中性粒细胞（术前）",
]


@dataclass(frozen=True)
class AnalysisPaths:
    project_dir: Path
    data_path: Path
    image_dir: Path
    output_dir: Path


def find_project_dir() -> Path:
    here = Path(__file__).resolve().parent
    if (here / "data" / "data.xlsx").exists():
        return here
    cwd = Path.cwd().resolve()
    candidate = cwd / "aki-master" / "aki-master"
    if (candidate / "data" / "data.xlsx").exists():
        return candidate
    raise FileNotFoundError("Could not locate aki-master/aki-master/data/data.xlsx")


def parse_args() -> argparse.Namespace:
    project_dir = find_project_dir()
    parser = argparse.ArgumentParser(
        description="Run second-revision classical AKI baselines with calibration and DCA."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=project_dir / "data" / "data.xlsx",
        help="Path to data.xlsx.",
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=project_dir / "data" / "images",
        help="Path to image directory containing JPG/TXT files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_dir / "revision_outputs" / "second_revision_baselines",
        help="Directory for tables and figures.",
    )
    parser.add_argument(
        "--feature-set",
        choices=["primary", "all_preop"],
        default="primary",
        help="Clinical feature set. The default mirrors the selected project features.",
    )
    parser.add_argument("--outer-folds", type=int, default=5)
    parser.add_argument("--inner-folds", type=int, default=3)
    parser.add_argument("--bootstrap", type=int, default=1000)
    return parser.parse_args()


def coerce_numeric(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def prepare_dataframe(data_path: Path) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_excel(data_path, engine="openpyxl")
    df = raw.copy()

    # Derived variables used by the original project code, with readable names.
    sbp = coerce_numeric(df["高压（入院）"])
    dbp = coerce_numeric(df["低压（入院）"])
    glucose = coerce_numeric(df["血糖（术前）"])
    df["高血压（入院血压）"] = ((sbp >= 140) | (dbp >= 90)).astype(float)
    df["糖尿病（术前血糖）"] = (glucose >= 7.0).astype(float)

    df[SEQUENCE_COL] = coerce_numeric(df[SEQUENCE_COL])
    df[OUTCOME_COL] = coerce_numeric(df[OUTCOME_COL])

    missing_required = df[SEQUENCE_COL].isna() | df[OUTCOME_COL].isna()
    included = df.loc[~missing_required].copy()
    included[SEQUENCE_COL] = included[SEQUENCE_COL].astype(int)
    included[OUTCOME_COL] = included[OUTCOME_COL].astype(int)

    audit = {
        "input_rows": int(len(raw)),
        "excluded_missing_sequence_or_outcome": int(missing_required.sum()),
        "analysis_rows": int(len(included)),
        "outcome_positive": int((included[OUTCOME_COL] == 1).sum()),
        "outcome_negative": int((included[OUTCOME_COL] == 0).sum()),
        "outcome_column": OUTCOME_COL,
        "sequence_column": SEQUENCE_COL,
    }
    return included, audit


def audit_images(df: pd.DataFrame, image_dir: Path) -> pd.DataFrame:
    jpg_ids = {
        int(path.stem)
        for path in image_dir.glob("*.jpg")
        if path.stem.isdigit()
    }
    txt_ids = {
        int(path.stem)
        for path in image_dir.glob("*.txt")
        if path.stem.isdigit()
    }
    clinical_ids = set(df[SEQUENCE_COL].astype(int).tolist())

    rows = [
        ("clinical_rows", len(clinical_ids), ""),
        ("jpg_files", len(jpg_ids), join_ids(jpg_ids)),
        ("txt_annotation_files", len(txt_ids), join_ids(txt_ids)),
        ("clinical_rows_without_jpg", len(clinical_ids - jpg_ids), join_ids(clinical_ids - jpg_ids)),
        ("jpg_without_clinical_row", len(jpg_ids - clinical_ids), join_ids(jpg_ids - clinical_ids)),
        ("jpg_without_txt_annotation", len(jpg_ids - txt_ids), join_ids(jpg_ids - txt_ids)),
        ("txt_without_jpg", len(txt_ids - jpg_ids), join_ids(txt_ids - jpg_ids)),
    ]
    return pd.DataFrame(rows, columns=["item", "count", "sequence_numbers"])


def join_ids(values: Iterable[int]) -> str:
    return ", ".join(str(v) for v in sorted(values))


def choose_features(df: pd.DataFrame, feature_set: str) -> list[str]:
    features = PRIMARY_FEATURES if feature_set == "primary" else ALL_PREOP_FEATURES
    missing = [col for col in features if col not in df.columns]
    if missing:
        raise KeyError(f"Missing expected feature columns: {missing}")
    return features


def build_models(inner_folds: int) -> dict[str, GridSearchCV]:
    inner_cv = StratifiedKFold(n_splits=inner_folds, shuffle=True, random_state=RANDOM_SEED)

    logistic = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    solver="saga",
                    class_weight="balanced",
                    max_iter=20000,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )
    logistic_grid = [
        {
            "model__penalty": ["l1", "l2"],
            "model__C": [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
        },
        {
            "model__penalty": ["elasticnet"],
            "model__C": [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0],
            "model__l1_ratio": [0.25, 0.5, 0.75],
        },
    ]

    rf = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=500,
                    class_weight="balanced_subsample",
                    random_state=RANDOM_SEED,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    rf_grid = {
        "model__max_depth": [2, 3, None],
        "model__min_samples_leaf": [2, 5, 10],
        "model__max_features": ["sqrt", None],
    }

    gb = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                GradientBoostingClassifier(random_state=RANDOM_SEED),
            ),
        ]
    )
    gb_grid = {
        "model__n_estimators": [50, 100, 200],
        "model__learning_rate": [0.02, 0.05, 0.1],
        "model__max_depth": [1, 2, 3],
        "model__min_samples_leaf": [3, 5, 10],
    }

    svm = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                SVC(
                    kernel="rbf",
                    probability=True,
                    class_weight="balanced",
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )
    svm_grid = {
        "model__C": [0.1, 0.3, 1.0, 3.0, 10.0],
        "model__gamma": ["scale", 0.01, 0.03, 0.1],
    }

    grids = {
        "Penalized logistic regression": (logistic, logistic_grid),
        "Random forest": (rf, rf_grid),
        "Gradient boosting": (gb, gb_grid),
        "Support vector machine": (svm, svm_grid),
    }
    return {
        name: GridSearchCV(
            estimator=pipe,
            param_grid=grid,
            scoring="roc_auc",
            cv=inner_cv,
            n_jobs=-1,
            refit=True,
        )
        for name, (pipe, grid) in grids.items()
    }


def run_nested_cv(
    x: pd.DataFrame,
    y: np.ndarray,
    outer_folds: int,
    inner_folds: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    models = build_models(inner_folds)
    outer_cv = StratifiedKFold(n_splits=outer_folds, shuffle=True, random_state=RANDOM_SEED)
    predictions = []
    fold_rows = []

    for fold, (train_idx, test_idx) in enumerate(outer_cv.split(x, y), start=1):
        x_train, x_test = x.iloc[train_idx], x.iloc[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        for model_name, grid in models.items():
            fitted = clone(grid)
            fitted.fit(x_train, y_train)
            prob = fitted.predict_proba(x_test)[:, 1]
            pred = (prob >= 0.5).astype(int)
            fold_rows.append(
                {
                    "model": model_name,
                    "fold": fold,
                    "n_test": int(len(test_idx)),
                    "n_positive": int(y_test.sum()),
                    "n_negative": int((y_test == 0).sum()),
                    "auc": safe_auc(y_test, prob),
                    "brier": brier_score_loss(y_test, prob),
                    "accuracy_at_0.5": accuracy_score(y_test, pred),
                    "balanced_accuracy_at_0.5": balanced_accuracy_score(y_test, pred),
                    "best_params": json.dumps(fitted.best_params_, ensure_ascii=False),
                }
            )
            predictions.extend(
                {
                    "model": model_name,
                    "fold": fold,
                    "y_true": int(yt),
                    "probability": float(p),
                }
                for yt, p in zip(y_test, prob)
            )

    return pd.DataFrame(predictions), pd.DataFrame(fold_rows)


def safe_auc(y_true: np.ndarray, prob: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return float(roc_auc_score(y_true, prob))


def expected_calibration_error(y_true: np.ndarray, prob: np.ndarray, bins: int = 10) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        if hi == 1.0:
            mask = (prob >= lo) & (prob <= hi)
        else:
            mask = (prob >= lo) & (prob < hi)
        if not np.any(mask):
            continue
        ece += mask.mean() * abs(y_true[mask].mean() - prob[mask].mean())
    return float(ece)


def calibration_intercept_slope(y_true: np.ndarray, prob: np.ndarray) -> tuple[float, float]:
    clipped = np.clip(prob, 1e-6, 1 - 1e-6)
    logits = np.log(clipped / (1 - clipped)).reshape(-1, 1)
    try:
        model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=10000)
        model.fit(logits, y_true)
        return float(model.intercept_[0]), float(model.coef_[0, 0])
    except Exception:
        return float("nan"), float("nan")


def bootstrap_ci(
    y_true: np.ndarray,
    prob: np.ndarray,
    metric,
    n_bootstrap: int,
    seed: int,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    values = []
    n = len(y_true)
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        if len(np.unique(y_true[idx])) < 2:
            continue
        values.append(metric(y_true[idx], prob[idx]))
    if not values:
        return float("nan"), float("nan")
    return tuple(float(v) for v in np.percentile(values, [2.5, 97.5]))


def summarize_predictions(predictions: pd.DataFrame, n_bootstrap: int) -> pd.DataFrame:
    rows = []
    for model_name, group in predictions.groupby("model", sort=False):
        y_true = group["y_true"].to_numpy()
        prob = group["probability"].to_numpy()
        pred = (prob >= 0.5).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
        auc = roc_auc_score(y_true, prob)
        auc_lo, auc_hi = bootstrap_ci(y_true, prob, roc_auc_score, n_bootstrap, RANDOM_SEED)
        brier = brier_score_loss(y_true, prob)
        brier_lo, brier_hi = bootstrap_ci(y_true, prob, brier_score_loss, n_bootstrap, RANDOM_SEED + 1)
        intercept, slope = calibration_intercept_slope(y_true, prob)
        rows.append(
            {
                "model": model_name,
                "n": int(len(y_true)),
                "positive": int(y_true.sum()),
                "negative": int((y_true == 0).sum()),
                "auc": auc,
                "auc_95ci_low": auc_lo,
                "auc_95ci_high": auc_hi,
                "average_precision": average_precision_score(y_true, prob),
                "brier": brier,
                "brier_95ci_low": brier_lo,
                "brier_95ci_high": brier_hi,
                "calibration_intercept": intercept,
                "calibration_slope": slope,
                "expected_calibration_error_10bins": expected_calibration_error(y_true, prob),
                "accuracy_at_0.5": accuracy_score(y_true, pred),
                "balanced_accuracy_at_0.5": balanced_accuracy_score(y_true, pred),
                "sensitivity_at_0.5": recall_score(y_true, pred, zero_division=0),
                "specificity_at_0.5": tn / (tn + fp) if (tn + fp) else math.nan,
                "ppv_at_0.5": precision_score(y_true, pred, zero_division=0),
                "npv_at_0.5": tn / (tn + fn) if (tn + fn) else math.nan,
                "f1_at_0.5": f1_score(y_true, pred, zero_division=0),
                "tp_at_0.5": int(tp),
                "fp_at_0.5": int(fp),
                "tn_at_0.5": int(tn),
                "fn_at_0.5": int(fn),
            }
        )
    return pd.DataFrame(rows)


def decision_curve(predictions: pd.DataFrame) -> pd.DataFrame:
    thresholds = np.round(np.arange(0.01, 0.81, 0.01), 2)
    rows = []
    for model_name, group in predictions.groupby("model", sort=False):
        y_true = group["y_true"].to_numpy()
        prob = group["probability"].to_numpy()
        n = len(y_true)
        prevalence = y_true.mean()
        for threshold in thresholds:
            pred = prob >= threshold
            tp = np.sum(pred & (y_true == 1))
            fp = np.sum(pred & (y_true == 0))
            odds = threshold / (1 - threshold)
            rows.append(
                {
                    "model": model_name,
                    "threshold": threshold,
                    "net_benefit": (tp / n) - (fp / n) * odds,
                    "treat_all_net_benefit": prevalence - (1 - prevalence) * odds,
                    "treat_none_net_benefit": 0.0,
                }
            )
    return pd.DataFrame(rows)


def plot_roc(predictions: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(6.5, 5.2))
    for model_name, group in predictions.groupby("model", sort=False):
        y_true = group["y_true"].to_numpy()
        prob = group["probability"].to_numpy()
        fpr, tpr, _ = roc_curve(y_true, prob)
        auc = roc_auc_score(y_true, prob)
        plt.plot(fpr, tpr, label=f"{model_name} (AUC {auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", color="0.5", linewidth=1)
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("Classical Baseline ROC Curves")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_pr(predictions: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(6.5, 5.2))
    prevalence = predictions["y_true"].mean()
    for model_name, group in predictions.groupby("model", sort=False):
        y_true = group["y_true"].to_numpy()
        prob = group["probability"].to_numpy()
        precision, recall, _ = precision_recall_curve(y_true, prob)
        ap = average_precision_score(y_true, prob)
        plt.plot(recall, precision, label=f"{model_name} (AP {ap:.3f})")
    plt.axhline(prevalence, linestyle="--", color="0.5", linewidth=1, label=f"Prevalence {prevalence:.3f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Classical Baseline Precision-Recall Curves")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_calibration(predictions: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(6.5, 5.2))
    for model_name, group in predictions.groupby("model", sort=False):
        y_true = group["y_true"].to_numpy()
        prob = group["probability"].to_numpy()
        frac_pos, mean_pred = calibration_curve(y_true, prob, n_bins=8, strategy="quantile")
        plt.plot(mean_pred, frac_pos, marker="o", linewidth=1.5, label=model_name)
    plt.plot([0, 1], [0, 1], linestyle="--", color="0.5", linewidth=1)
    plt.xlabel("Mean predicted probability")
    plt.ylabel("Observed event fraction")
    plt.title("Calibration Curves")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_dca(dca: pd.DataFrame, output_path: Path) -> None:
    plt.figure(figsize=(7.0, 5.2))
    for model_name, group in dca.groupby("model", sort=False):
        plt.plot(group["threshold"], group["net_benefit"], label=model_name)
    first = dca.drop_duplicates("threshold")
    plt.plot(
        first["threshold"],
        first["treat_all_net_benefit"],
        linestyle="--",
        color="0.4",
        label="Treat all",
    )
    plt.axhline(0, linestyle=":", color="0.2", label="Treat none")
    plt.xlabel("Threshold probability")
    plt.ylabel("Net benefit")
    plt.title("Decision-Curve Analysis")
    plt.ylim(bottom=min(-0.10, dca["net_benefit"].min() - 0.02))
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_notes(
    output_dir: Path,
    audit: dict,
    features: list[str],
    summary: pd.DataFrame,
    image_audit: pd.DataFrame,
    feature_set: str,
) -> None:
    best = summary.sort_values("auc", ascending=False).iloc[0]
    missing_jpg = image_audit.loc[image_audit["item"] == "clinical_rows_without_jpg", "sequence_numbers"].iloc[0]
    notes = [
        "# Second-revision baseline analysis notes",
        "",
        f"- Data source: `{audit['data_path']}`.",
        f"- Feature set: `{feature_set}` with {len(features)} preoperative clinical predictors.",
        f"- Rows read: {audit['input_rows']}; excluded before modeling because sequence or outcome was missing: {audit['excluded_missing_sequence_or_outcome']}; analyzed: {audit['analysis_rows']} ({audit['outcome_positive']} postoperative AKI, {audit['outcome_negative']} no postoperative AKI).",
        f"- Missing clinical values were not used for exclusion; they were median-imputed within each training fold.",
        f"- Image audit: {int(image_audit.loc[image_audit['item'] == 'jpg_files', 'count'].iloc[0])} JPG files and {int(image_audit.loc[image_audit['item'] == 'txt_annotation_files', 'count'].iloc[0])} TXT annotation files in `data/images`.",
        f"- Clinical sequence numbers without JPG files: {missing_jpg if missing_jpg else 'none'}.",
        f"- Classical baselines were evaluated using 5-fold stratified outer cross-validation with 3-fold inner hyperparameter selection by ROC AUC.",
        f"- Best baseline by cross-validated AUC: {best['model']} AUC {best['auc']:.3f} (bootstrap 95% CI {best['auc_95ci_low']:.3f}-{best['auc_95ci_high']:.3f}); Brier score {best['brier']:.3f}.",
        "- These are internal cross-validation results only. They should not be described as external validation or as proving clinical utility.",
        "",
        "Predictors:",
        "",
    ]
    notes.extend(f"- {feature}" for feature in features)
    (output_dir / "baseline_results_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    paths = AnalysisPaths(
        project_dir=find_project_dir(),
        data_path=args.data.resolve(),
        image_dir=args.image_dir.resolve(),
        output_dir=args.output_dir.resolve(),
    )
    paths.output_dir.mkdir(parents=True, exist_ok=True)

    df, audit = prepare_dataframe(paths.data_path)
    audit["data_path"] = str(paths.data_path)
    audit["image_dir"] = str(paths.image_dir)
    audit["feature_set"] = args.feature_set

    image_audit = audit_images(df, paths.image_dir)
    features = choose_features(df, args.feature_set)
    missing_by_feature = (
        df[features]
        .apply(coerce_numeric)
        .isna()
        .sum()
        .rename_axis("feature")
        .reset_index(name="missing_count")
    )

    x = df[features].apply(coerce_numeric)
    y = df[OUTCOME_COL].to_numpy(dtype=int)

    predictions, fold_metrics = run_nested_cv(
        x=x,
        y=y,
        outer_folds=args.outer_folds,
        inner_folds=args.inner_folds,
    )
    summary = summarize_predictions(predictions, args.bootstrap)
    dca = decision_curve(predictions)

    pd.DataFrame([audit]).to_csv(paths.output_dir / "case_flow_audit.csv", index=False, encoding="utf-8-sig")
    image_audit.to_csv(paths.output_dir / "image_availability_audit.csv", index=False, encoding="utf-8-sig")
    missing_by_feature.to_csv(paths.output_dir / "feature_missingness.csv", index=False, encoding="utf-8-sig")
    fold_metrics.to_csv(paths.output_dir / "baseline_fold_metrics.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(paths.output_dir / "baseline_model_performance.csv", index=False, encoding="utf-8-sig")
    dca.to_csv(paths.output_dir / "decision_curve_net_benefit.csv", index=False, encoding="utf-8-sig")
    predictions.to_csv(paths.output_dir / "cross_validated_probabilities_deidentified.csv", index=False, encoding="utf-8-sig")
    (paths.output_dir / "analysis_manifest.json").write_text(
        json.dumps(
            {
                "random_seed": RANDOM_SEED,
                "outer_folds": args.outer_folds,
                "inner_folds": args.inner_folds,
                "bootstrap_replicates": args.bootstrap,
                "features": features,
                "note": "Predictions file omits patient IDs and sequence numbers.",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    plot_roc(predictions, paths.output_dir / "baseline_roc_curves.png")
    plot_pr(predictions, paths.output_dir / "baseline_precision_recall_curves.png")
    plot_calibration(predictions, paths.output_dir / "baseline_calibration_curves.png")
    plot_dca(dca, paths.output_dir / "decision_curve_analysis.png")
    save_notes(paths.output_dir, audit, features, summary, image_audit, args.feature_set)

    print(f"Wrote second-revision baseline outputs to: {paths.output_dir}")
    print(summary[["model", "auc", "auc_95ci_low", "auc_95ci_high", "brier", "calibration_slope"]].to_string(index=False))


if __name__ == "__main__":
    main()
