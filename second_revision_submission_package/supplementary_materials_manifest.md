# Supplementary Materials Manifest

Date: 2026-06-14
Prepared by: Agent 4, Figures / Submission Package / Formatting

Scope: This package organizes Agent 2's verified internal-validation outputs into PLOS-style supplementary materials. It does not modify numerical results, model code, or manuscript prose.

## Package Location

`D:\AKI\second_revision_submission_package`

## Critical Interpretation Note

The calibration and decision-curve analysis files in this package evaluate optimized classical clinical baseline models under internal cross-validation. They must not be described as external validation, final multimodal-model calibration, or proof that the final multimodal model is clinically deployable. They are best used as reviewer-facing transparency evidence and as support for restrained claims.

## Supplementary Tables

### S1 Table. Case-flow and data-availability audit

- Submission files: `tables/S1_Table_case_flow_and_data_availability.csv`; `tables/S1_Table_case_flow_and_data_availability.xlsx`
- Source files: `second_revision_results/case_flow_audit.csv`; `second_revision_results/image_availability_audit.csv`
- Proposed caption: **S1 Table. Case-flow and data-availability audit for the second-revision internal-validation analyses.** The table summarizes raw rows, excluded rows, the final tabular baseline analytic set, outcome counts, image-file availability, YOLO annotation availability, clinical records without matching JPG files, and JPG files without TXT annotations.
- Suggested manuscript/response citation: Cite when explaining the analytic sample and image availability, e.g. `The case-flow and image-availability audit is provided in S1 Table.`
- Caution: Use as data-audit evidence only; it is not a performance result.

### S2 Table. Classical baseline model performance

- Submission files: `tables/S2_Table_classical_baseline_model_performance.csv`; `tables/S2_Table_classical_baseline_model_performance.xlsx`
- Source file: `second_revision_results/baseline_model_performance.csv`
- Proposed caption: **S2 Table. Internal cross-validated performance of optimized classical clinical baseline models.** Penalized logistic regression, random forest, gradient boosting, and support vector machine were evaluated using the 193-patient tabular analytic set and 11 preoperative clinical predictors. Metrics include AUC with bootstrap 95% CI, average precision, Brier score, calibration metrics, threshold-based classification metrics, and confusion-matrix counts at threshold 0.5.
- Suggested manuscript/response citation: Cite in the baseline-comparison response and Results paragraph, e.g. `Optimized classical clinical baselines showed moderate internal discrimination (S2 Table).`
- Caution: Present as internal clinical-baseline evidence only; do not use it to claim external validity.

### S3 Table. Repeated cross-validation robustness summary

- Submission files: `tables/S3_Table_repeated_cv_robustness_summary.csv`; `tables/S3_Table_repeated_cv_robustness_summary.xlsx`
- Source file: `second_revision_results/robustness_repeated_cv_summary.csv`
- Proposed caption: **S3 Table. Repeated stratified 5-fold cross-validation robustness summary for optimized classical clinical baselines.** The table reports mean, standard deviation, and approximate 95% confidence intervals across 25 validation folds for discrimination, classification, MCC, and Brier-score metrics.
- Suggested manuscript/response citation: Cite when discussing robustness and overfitting caution, e.g. `Repeated stratified cross-validation results are summarized in S3 Table.`
- Caution: This is still internal resampling evidence and does not replace external or temporal validation.

## Supplementary Figures

### S1 Fig. Calibration curves for optimized classical clinical baselines

- Submission file: `figures/S1_Fig_baseline_calibration_curves.png`
- Source file: `second_revision_results/baseline_calibration_curves.png`
- Proposed caption: **S1 Fig. Internal cross-validated calibration curves for optimized classical clinical baseline models.** Curves compare predicted and observed postoperative AKI risk for classical clinical baselines. These curves provide internal calibration evidence for baseline models only and should not be interpreted as final multimodal-model calibration.
- Suggested manuscript/response citation: Cite in the calibration response, e.g. `Calibration curves for the classical clinical baselines are shown in S1 Fig.`
- Caution: Do not cite as external calibration or deployment readiness.

### S2 Fig. Decision-curve analysis for optimized classical clinical baselines

- Submission file: `figures/S2_Fig_decision_curve_analysis.png`
- Source file: `second_revision_results/decision_curve_analysis.png`
- Proposed caption: **S2 Fig. Internal decision-curve analysis for optimized classical clinical baseline models.** Net benefit is plotted across threshold probabilities for classical clinical baselines with treat-all and treat-none references. This internal analysis is included for transparency and does not establish clinical utility or readiness for deployment.
- Suggested manuscript/response citation: Cite in the clinical-evaluation response, e.g. `Decision-curve analysis for the classical clinical baselines is provided in S2 Fig.`
- Caution: The response draft notes that gradient boosting did not clearly exceed the treat-all reference across thresholds 0.10 to 0.50; keep interpretation cautious.

### S3 Fig. Baseline ROC curves

- Submission file: `figures/S3_Fig_baseline_roc_curves.png`
- Source file: `second_revision_results/baseline_roc_curves.png`
- Proposed caption: **S3 Fig. Receiver operating characteristic curves for optimized classical clinical baseline models under internal cross-validation.** This optional figure visualizes discrimination of the classical clinical baselines and complements S2 Table.
- Suggested manuscript/response citation: Optional; cite only if the Project Lead wants a visual supplement to the baseline-comparison table.
- Caution: Internal baseline discrimination only.

### S4 Fig. Baseline precision-recall curves

- Submission file: `figures/S4_Fig_baseline_precision_recall_curves.png`
- Source file: `second_revision_results/baseline_precision_recall_curves.png`
- Proposed caption: **S4 Fig. Precision-recall curves for optimized classical clinical baseline models under internal cross-validation.** This optional figure is useful because the analytic set is outcome-imbalanced.
- Suggested manuscript/response citation: Optional; cite only if the Project Lead wants to emphasize performance under class imbalance.
- Caution: Internal baseline evidence only.

## Upload / Formatting Notes

- The PNG figures are small, readable, and suitable as supporting-information figures. PLOS supporting information can use broad file types; final uploaded names should match the `S#` numbering used in captions.
- The CSV files preserve Agent 2's values. XLSX versions are provided for easier editorial review and can be uploaded if preferred by the Project Lead.
- If the manuscript includes supporting-information captions at the end, use the `S1 Table`, `S2 Table`, `S3 Table`, `S1 Fig`, `S2 Fig`, and optional `S3 Fig`/`S4 Fig` labels exactly as uploaded.
- Do not renumber these materials until the final manuscript decides whether optional ROC and PR figures are included.
