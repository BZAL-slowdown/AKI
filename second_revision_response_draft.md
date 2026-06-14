# Second-Revision Response Draft And Manuscript Edit Plan

Date: 2026-06-14

Prepared by: Agent 1, Reviewer Response And Manuscript Strategy

Scope: This draft uses the verified Agent 2 outputs listed below. It does not invent external validation, intraoperative variables, or new model results.

## Local Evidence Used

- Analysis script: `D:\AKI\aki-master\aki-master\second_revision_analysis.py`
- Baseline performance table: `D:\AKI\aki-master\aki-master\second_revision_results\baseline_model_performance.csv`
- Robustness summary: `D:\AKI\aki-master\aki-master\second_revision_results\robustness_repeated_cv_summary.csv`
- Calibration figure: `D:\AKI\aki-master\aki-master\second_revision_results\baseline_calibration_curves.png`
- Decision-curve figure: `D:\AKI\aki-master\aki-master\second_revision_results\decision_curve_analysis.png`
- Analysis notes: `D:\AKI\aki-master\aki-master\second_revision_results\baseline_results_notes.md`

## Verified Facts To Use

- The original spreadsheet contained 194 rows. One row was excluded because sequence number or postoperative AKI label was missing. The final tabular baseline analysis used 193 patients.
- Outcome distribution in the 193-patient analytic set: 132 postoperative AKI-positive and 61 postoperative AKI-negative cases.
- Image audit: 183 JPG files and 181 TXT annotation files. Clinical records without JPG files: 14, 47, 88, 97, 99, 100, 125, 173, 174, 175. JPG files without TXT annotation: 101, 164.
- Classical baselines used 11 preoperative clinical predictors with median imputation within each training fold.
- Main baseline analysis used 5-fold stratified outer cross-validation with 3-fold inner hyperparameter selection by ROC AUC.
- Best classical clinical baseline: gradient boosting, AUC 0.636, bootstrap 95% CI 0.548-0.718, Brier score 0.223, MCC 0.172 at threshold 0.5.
- Repeated stratified 5-fold CV with 5 repeats: gradient boosting mean AUC 0.628 +/- 0.084 SD; random forest mean AUC 0.620 +/- 0.087 SD.
- These are internal validation results only. They must not be described as external validation or proof of clinical utility.
- Decision-curve results should be interpreted cautiously. For example, at thresholds 0.10 to 0.50, gradient boosting did not clearly exceed the treat-all net-benefit reference. This supports claim-tempering rather than deployment claims.

## Draft Response Letter Text

### Major Comment 1. External validity and overfitting

**Comment:** The study is based on a single-center retrospective cohort with a limited sample size (n = 194). Despite the use of few-shot learning, the complexity of the proposed architecture raises concerns regarding overfitting. The absence of external or temporal validation significantly limits generalizability.

**Response:** We thank the reviewer for emphasizing this important limitation. We agree that the single-center retrospective design and limited sample size restrict the external validity of the present study. In the revised manuscript, we have therefore reframed the study as an internally validated, exploratory model-development study rather than a clinically deployable prediction tool. We now explicitly state that no external or temporal validation cohort was available for this revision, and that multicenter, temporal, and prospective validation will be required before the model can be generalized or used in routine clinical decision-making.

To address the risk of overfitting more transparently, we added a reproducible second-revision analysis script (`second_revision_analysis.py`) and additional internal validation evidence. The tabular baseline analysis began with 194 records, excluded 1 row because sequence number or postoperative AKI label was missing, and analyzed 193 patients (132 AKI-positive, 61 AKI-negative). Classical baseline models were evaluated using 5-fold stratified outer cross-validation with 3-fold inner hyperparameter selection. The best classical clinical baseline was gradient boosting, with AUC 0.636 (bootstrap 95% CI 0.548-0.718), Brier score 0.223, and MCC 0.172. In repeated stratified 5-fold cross-validation with 5 repeats, gradient boosting showed mean AUC 0.628 +/- 0.084 SD, while random forest showed mean AUC 0.620 +/- 0.087 SD. These results are now used to temper the interpretation of the proposed model and to emphasize that all performance estimates remain internal.

**Actions taken / manuscript locations:** We recommend revising the Abstract, Methods (Model Evaluation), Results (Model Performance), and Discussion (Limitations) to state that the study provides internal cross-validation evidence only. In the Discussion, we recommend replacing language such as "successfully avoids overfitting" or "generalization capacity" with wording such as "may reduce, but cannot eliminate, overfitting risk in this small retrospective cohort." We also recommend adding the baseline and repeated-CV tables to the Supplement and citing them in the Results.

### Major Comment 2. Incomplete clinical variables

**Comment:** The model relies exclusively on preoperative variables. Key intraoperative determinants of postoperative AKI (warm ischemia time, pneumoperitoneum pressure, intraoperative hypotension, blood loss) are not included. Some selected variables have weak physiological links to AKI.

**Response:** We agree with the reviewer. Warm ischemia time, pneumoperitoneum pressure and duration, intraoperative hypotension burden, blood loss, operative duration, fluid balance, vasopressor exposure, and nephrotoxic exposure are clinically important determinants of postoperative AKI. These variables were not available in complete structured form in the retrospective dataset and were therefore not included in the current model. We have revised the manuscript to make clear that the present model is a preoperative risk-stratification model rather than a full perioperative dynamic prediction model.

We also now state that the absence of intraoperative variables may limit discrimination, calibration, threshold transportability, and clinical usefulness. Future prospective data collection should include the above intraoperative and anesthesia-related variables so that dynamic perioperative models can be compared with, or added to, the current preoperative model.

**Actions taken / manuscript locations:** Add an explicit limitation to Methods (Clinical Feature Selection and Definition) and Discussion (Limitations). In the Introduction, retain the pathophysiologic importance of warm ischemia and pneumoperitoneum as a rationale for the surgical context, but avoid implying that these variables were modeled. In the Abstract and Discussion, describe the model as "preoperative" and avoid "real-time" or "closed-loop" wording unless intraoperative data are actually analyzed.

### Major Comment 3. Model complexity

**Comment:** The accumulation of multiple advanced mechanisms (multimodal fusion, multi-prototype clustering, pseudo-sample generation, multiple loss functions) appears disproportionate to the sample size and may limit reproducibility and clinical translation.

**Response:** We appreciate this comment and agree that model complexity must be interpreted cautiously in a 193 to 194-patient retrospective cohort. We have revised the manuscript strategy so that the architecture is presented as a proof-of-concept design choice, not as definitive evidence of clinical superiority. Technical details should remain in the Supporting information, while the main text should focus on the clinical question, data limitations, evaluation design, and conservative interpretation.

The newly added classical baseline analyses provide an important context for model complexity. Among optimized classical clinical baselines, gradient boosting achieved AUC 0.636 (95% CI 0.548-0.718), and repeated-CV AUC 0.628 +/- 0.084. These results suggest that conventional preoperative tabular models have limited but nonzero discrimination in this cohort. They should be used to support a balanced statement: the proposed multimodal approach may improve internal discrimination compared with these clinical-only baselines, but the added complexity requires external validation, calibration assessment, and prospective testing before clinical translation.

**Actions taken / manuscript locations:** In Methods, condense the descriptions of gated fusion, multi-prototype clustering, pseudo-sample generation, and multi-loss design. In Results and Discussion, avoid claiming that each component is independently necessary unless an ablation result is available. In the Discussion, add that the complexity may increase overfitting risk and reduce reproducibility, and that simpler baselines now provide a benchmark for future validation.

### Major Comment 4. Baseline model comparison

**Comment:** The clinical-only model demonstrates poor performance. Comparisons with optimized classical models (e.g., penalized regression or gradient boosting) are lacking and would strengthen the manuscript.

**Response:** We agree and have added optimized classical clinical baseline comparisons using the same 193-patient analytic set and 11 preoperative predictors. The analysis was implemented in `second_revision_analysis.py`. Missing clinical values were handled by median imputation within each training fold to avoid information leakage. Four classical baselines were evaluated: penalized logistic regression, random forest, gradient boosting, and support vector machine. Each model used 5-fold stratified outer cross-validation with 3-fold inner hyperparameter selection by ROC AUC.

The best classical baseline was gradient boosting, with AUC 0.636 (bootstrap 95% CI 0.548-0.718), average precision 0.795, Brier score 0.223, sensitivity 0.864, specificity 0.279, and MCC 0.172 at threshold 0.5. Random forest had AUC 0.617 (95% CI 0.526-0.700), Brier score 0.220, and MCC 0.152. Penalized logistic regression and support vector machine performed less well by AUC (0.480 and 0.565, respectively). In repeated stratified 5-fold CV with 5 repeats, gradient boosting remained the best model by mean AUC (0.628 +/- 0.084), followed closely by random forest (0.620 +/- 0.087).

These comparisons strengthen the manuscript by showing that optimized classical clinical-only models provide a relevant benchmark, but their moderate performance also reinforces the need for cautious claims and external validation.

**Actions taken / manuscript locations:** Add a "Classical baseline comparison" paragraph to Methods (Model Evaluation). Add a brief Results paragraph after Model Performance and cite Supplementary Table 1 and Supplementary Table 2. Avoid stating that the proposed model is clinically superior unless the comparison is presented as internal and exploratory.

### Major Comment 5. Clinical evaluation: calibration, decision-curve analysis, and threshold

**Comment:** Calibration metrics and decision-curve analysis are not provided. The clinical implications of the selected decision threshold are insufficiently discussed.

**Response:** We thank the reviewer for this important point. We added calibration and decision-curve analyses to the second-revision evidence package. For the optimized classical clinical baselines, the performance table now reports Brier score, calibration intercept, calibration slope, and expected calibration error. Calibration curves are provided in `baseline_calibration_curves.png`, and decision-curve analysis is provided in `decision_curve_analysis.png`.

The clinical interpretation has also been tempered. The gradient boosting baseline achieved Brier score 0.223, calibration intercept 0.413, calibration slope 0.349, and expected calibration error 0.109. Decision-curve analysis was included for transparency, but it should not be interpreted as proving clinical utility. For example, across threshold probabilities from 0.10 to 0.50, gradient boosting did not clearly exceed the treat-all net-benefit reference. Therefore, the revised manuscript should state that threshold selection remains preliminary and must be re-evaluated in external and prospective cohorts before any clinical workflow use.

**Actions taken / manuscript locations:** Add calibration and DCA methods to Methods (Model Evaluation). Add calibration and DCA results to Results, preferably in a concise paragraph linked to Supplementary Figures. In the Discussion, revise the threshold paragraph to state that any Youden-derived or 0.5 threshold is internally derived and not transportable without external validation and local recalibration.

## Manuscript Edit Map

Use the paragraph identifiers from the extracted revised manuscript text.

| Manuscript section | Current paragraph(s) | Required change |
| --- | --- | --- |
| Abstract | P17 | State "single-center retrospective cohort" and "internal cross-validation"; remove "significantly improves generalization performance" and "We recommend incorporating..."; add that intraoperative variables were unavailable/not modeled. |
| Introduction | P24-P35 | Reduce claims about traditional models, early-warning performance, clinical utility, and geographic flexibility. Keep rationale for laparoscopic renal surgery but distinguish variables that motivate the problem from variables actually included in the model. |
| Study Subjects / Data Collection | P53-P66 | Add case-flow clarification: 194 raw rows, 1 excluded for missing sequence/outcome, 193 tabular baseline records. If discussing images, add image audit counts and missing JPG/TXT cases in Supplement rather than the main text. |
| Clinical Feature Selection | P72-P77 | Add a limitation sentence: warm ischemia time, pneumoperitoneum pressure/duration, intraoperative hypotension, blood loss, operative duration, fluid balance, vasopressors, and nephrotoxic exposure were unavailable/incomplete and not modeled. |
| Data Preprocessing | P78-P82 | State that baseline analyses imputed missing clinical values within each training fold. Avoid saying preprocessing or augmentation ensures generalization. |
| Model Evaluation | P110 | Add classical baseline methods: penalized logistic regression, random forest, gradient boosting, support vector machine; 5-fold stratified outer CV; 3-fold inner tuning by ROC AUC; bootstrap CI; repeated 5-fold CV with 5 repeats; calibration metrics and DCA. |
| Results overview | P112-P114 | Replace "independent validation" with "internal cross-validation." Add a new baseline-comparison paragraph after P116 using verified values only. Remove clinical implementation claims. |
| Model Performance | P116-P117 | Add baseline results: gradient boosting AUC 0.636 (95% CI 0.548-0.718), Brier 0.223, MCC 0.172; repeated-CV AUC 0.628 +/- 0.084. State that these are internal results only. |
| SHAP | P119-P124 | Present SHAP as descriptive and model-dependent. Remove causal or interventional language such as "clear targets for clinical intervention." |
| Discussion | P126-P132 | Add a named limitation subsection covering single-center retrospective design, residual overfitting risk, no external/temporal validation, missing intraoperative variables, moderate classical baseline performance, and cautious DCA findings. |
| Conclusion | If present in final manuscript | Use restrained wording: "promising internal discrimination" and "requires external, temporal, and prospective validation"; do not recommend routine adoption. |

## Suggested New Supplementary Materials

1. **S1 Table. Case-flow and data-availability audit**
   - Source: `case_flow_audit.csv`, `image_availability_audit.csv`, and `baseline_results_notes.md`.
   - Include: 194 raw rows; 1 excluded; 193 analyzed; 132 AKI-positive; 61 AKI-negative; 183 JPG; 181 TXT; missing JPG case numbers; JPG without TXT annotations.

2. **S2 Table. Classical baseline model performance**
   - Source: `baseline_model_performance.csv`.
   - Include: model, n, positive/negative counts, AUC with bootstrap 95% CI, average precision, Brier score, calibration intercept/slope, expected calibration error, sensitivity, specificity, F1, MCC, TP/FP/TN/FN at threshold 0.5.

3. **S3 Table. Repeated cross-validation robustness summary**
   - Source: `robustness_repeated_cv_summary.csv`.
   - Include: repeated stratified 5-fold CV with 5 repeats; mean AUC +/- SD; accuracy, balanced accuracy, F1, MCC, and Brier summaries.

4. **S1 Fig. Calibration curves for optimized classical clinical baselines**
   - Source: `baseline_calibration_curves.png`.
   - Caption should state that the figure shows internal cross-validated calibration for classical clinical baselines only.

5. **S2 Fig. Decision-curve analysis for optimized classical clinical baselines**
   - Source: `decision_curve_analysis.png`.
   - Caption should state that the figure provides internal decision-curve assessment and does not establish clinical utility or deployment readiness.

Optional, if space permits:

6. **S3 Fig. Baseline ROC curves**
   - Source: `baseline_roc_curves.png`.
   - Useful if Project Lead wants a visual companion to S2 Table.

7. **S4 Fig. Baseline precision-recall curves**
   - Source: `baseline_precision_recall_curves.png`.
   - Useful because the outcome distribution is imbalanced.

## Claim-Tempering Replacement Phrases

- Replace "demonstrates clinical value" with "showed promising internal discrimination."
- Replace "generalization performance" with "internal cross-validated performance."
- Replace "can be easily incorporated into clinical decision pathways" with "could be evaluated for incorporation into clinical workflows after external validation and prospective testing."
- Replace "successfully avoids overfitting" with "may reduce overfitting risk, although residual overfitting remains possible."
- Replace "accurately identifying high-risk patients" with "identifying patients estimated to be high risk within this cohort."
- Replace "SHAP revealed biological mechanisms" with "SHAP provided a descriptive summary of model feature contributions."

## Project Lead Next Steps

1. Integrate the response text into the formal `Response to Reviewers` document.
2. Add the baseline, calibration, DCA, and robustness methods/results to the manuscript and supplement.
3. Decide whether final multimodal model calibration/DCA probabilities are available. If not, do not claim final-model calibration or final-model DCA; present the current outputs as baseline clinical-model calibration/DCA and as support for caution.
4. Ensure the response letter and manuscript consistently state that all new analyses are internal validation only.
