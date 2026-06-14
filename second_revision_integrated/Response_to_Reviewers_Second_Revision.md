# Response to Reviewers - Second Revision

**Manuscript title:** Few-Shot Prediction of Post-Fusion Acute Kidney Injury Using Multimodal Radiomics-Clinical Feature-Based Prototype Networks
**Journal:** PLOS ONE
**Manuscript ID:** PONE-D-25-38340

Dear Editor and Reviewer,

We sincerely thank you for the careful second-round review and constructive comments. We have revised the manuscript and supporting materials to address concerns regarding external validity, overfitting, missing intraoperative variables, model complexity, baseline comparisons, calibration, decision-curve analysis, and cautious clinical interpretation. All newly added analyses are internal validation analyses and are not presented as external validation or evidence of clinical deployment readiness.

## Major Comment 1. External validity and overfitting

**Comment:** The study is based on a single-center retrospective cohort with a limited sample size (n=194). Despite the use of few-shot learning, the complexity of the proposed architecture raises concerns regarding overfitting. The absence of external or temporal validation significantly limits generalizability.

**Response:** We thank the reviewer for emphasizing this central limitation. We agree that the single-center retrospective design and limited sample size restrict external validity. We therefore revised the manuscript to frame the work as an exploratory, internally validated model-development study rather than a model intended for direct clinical use. We now explicitly state that no external or temporal validation cohort was available for this revision and that multicenter, temporal, and prospective validation will be required before the model can be generalized or used in routine clinical decision-making.

To address overfitting concerns more transparently, we added a reproducible second-revision analysis script and additional internal validation evidence. The newly added tabular baseline analysis began with 194 records, excluded 1 row because sequence number or postoperative AKI label was missing, and analyzed 193 patients (132 AKI-positive and 61 AKI-negative). Classical baseline models were evaluated using five-fold stratified outer cross-validation with three-fold inner hyperparameter selection. The best classical clinical baseline was gradient boosting, with AUC 0.636 (bootstrap 95% CI 0.548-0.718), Brier score 0.223, and MCC 0.172. In repeated stratified five-fold cross-validation with five repeats, gradient boosting showed mean AUC 0.628 +/- 0.084 SD, while random forest showed mean AUC 0.620 +/- 0.087 SD. These findings are reported as internal evidence only and are used to temper interpretation rather than to claim external generalizability.

**Actions taken:** We revised the Abstract, Methods, Results, and Discussion to state that the model evidence is internal cross-validation evidence only. We also added classical baseline and repeated-CV robustness results to the supplementary materials.

**Location in revised manuscript/supporting materials:** Abstract; Methodology - Model Evaluation; Results - Model Performance; Discussion - limitations and clinical interpretation; S1-S3 Tables.

## Major Comment 2. Incomplete clinical variables

**Comment:** The model relies exclusively on preoperative variables. Key intraoperative determinants of postoperative AKI (warm ischemia time, pneumoperitoneum pressure, intraoperative hypotension, blood loss) are not included. Some selected variables have weak physiological links to AKI.

**Response:** We agree with the reviewer. Warm ischemia time, pneumoperitoneum pressure and duration, intraoperative hypotension burden, blood loss, operative duration, fluid balance, vasopressor exposure, and nephrotoxic exposure are clinically important determinants of postoperative AKI. These variables were not available in complete structured form in the retrospective dataset and were therefore not included in the current model. We revised the manuscript to make clear that the model is a preoperative risk-stratification model rather than a full perioperative dynamic prediction model. We also state that the absence of intraoperative variables may limit discrimination, calibration, threshold transportability, and clinical usefulness.

**Actions taken:** We added explicit statements in the clinical-feature section and Discussion noting that intraoperative variables were unavailable/incomplete and were not modeled. We also softened clinical-utility language accordingly.

**Location in revised manuscript/supporting materials:** Methodology - Clinical Feature Selection and Definition; Abstract; Discussion - limitations and future work.

## Major Comment 3. Model complexity

**Comment:** The accumulation of multiple advanced mechanisms (multimodal fusion, multi-prototype clustering, pseudo-sample generation, multiple loss functions) appears disproportionate to the sample size and may limit reproducibility and clinical translation.

**Response:** We appreciate this comment and agree that model complexity must be interpreted cautiously in a 194-patient retrospective cohort. We revised the manuscript so that the architecture is presented as an exploratory proof-of-concept design rather than definitive evidence of clinical superiority. The newly added classical baseline analyses provide context for this complexity: optimized clinical-only baselines had moderate internal discrimination, with gradient boosting achieving AUC 0.636 (95% CI 0.548-0.718) and repeated-CV AUC 0.628 +/- 0.084. These findings support a balanced interpretation: the proposed multimodal model may improve internal discrimination within this cohort, but its added complexity requires external validation, calibration assessment, and prospective testing before clinical translation.

**Actions taken:** We condensed and tempered the interpretation of the model architecture, added simpler clinical baselines as benchmarks, and added explicit discussion that residual overfitting and reproducibility concerns remain.

**Location in revised manuscript/supporting materials:** Methodology - model design/evaluation; Results - baseline comparison; Discussion - limitations.

## Major Comment 4. Baseline model comparison

**Comment:** The clinical-only model demonstrates poor performance. Comparisons with optimized classical models (e.g., penalized regression or gradient boosting) are lacking and would strengthen the manuscript.

**Response:** We agree and added optimized classical clinical baseline comparisons using the 193-patient tabular analytic set and 11 preoperative predictors. The analysis was implemented in second_revision_analysis.py. Missing clinical values were handled by median imputation within each training fold to avoid information leakage. Four classical baselines were evaluated: penalized logistic regression, random forest, gradient boosting, and support vector machine. Each model used five-fold stratified outer cross-validation with three-fold inner hyperparameter selection by ROC AUC.

The best classical baseline was gradient boosting, with AUC 0.636 (bootstrap 95% CI 0.548-0.718), average precision 0.795, Brier score 0.223, sensitivity 0.864, specificity 0.279, and MCC 0.172 at threshold 0.5. Random forest had AUC 0.617 (95% CI 0.526-0.700), Brier score 0.220, and MCC 0.152. Penalized logistic regression and support vector machine performed less well by AUC (0.480 and 0.565, respectively). In repeated stratified five-fold CV with five repeats, gradient boosting remained the best model by mean AUC (0.628 +/- 0.084), followed closely by random forest (0.620 +/- 0.087).

**Actions taken:** We added a classical-baseline comparison paragraph to the Methods and Results and provide detailed performance metrics in S2 Table and repeated-CV robustness results in S3 Table.

**Location in revised manuscript/supporting materials:** Methodology - Model Evaluation; Results - Model Performance; S2 Table; S3 Table.

## Major Comment 5. Clinical evaluation: calibration, decision-curve analysis, and threshold

**Comment:** Calibration metrics and decision-curve analysis are not provided. The clinical implications of the selected decision threshold are insufficiently discussed.

**Response:** We thank the reviewer for this important point. We added calibration and decision-curve analyses to the second-revision evidence package for the optimized classical clinical baselines. The performance table now reports Brier score, calibration intercept, calibration slope, and expected calibration error. Calibration curves are provided in S1 Fig, and decision-curve analysis is provided in S2 Fig.

The clinical interpretation has been tempered. For the gradient boosting baseline, Brier score was 0.223, calibration intercept was 0.413, calibration slope was 0.349, and expected calibration error was 0.109. Decision-curve analysis was included for transparency, but it should not be interpreted as establishing clinical utility. Across threshold probabilities from 0.10 to 0.50, gradient boosting did not clearly exceed the treat-all net-benefit reference. We therefore revised the manuscript to state that threshold selection remains preliminary and must be re-evaluated in external and prospective cohorts before any clinical workflow use.

**Actions taken:** We added calibration metrics, calibration curves, decision-curve analysis, and a cautious threshold interpretation. We explicitly state that these are internal classical-baseline analyses, not final multimodal-model external validation and not evidence for deployment readiness.

**Location in revised manuscript/supporting materials:** Methodology - Model Evaluation; Results - Model Performance; Discussion - clinical interpretation; S1 Fig; S2 Fig.

## Minor Comments

**Comment:** The manuscript remains lengthy and could benefit from further condensation. Claims regarding clinical utility should be further tempered. SHAP analysis is descriptive and should be cautiously interpreted. Figures and legends could be simplified.

**Response:** We agree with these points and revised the manuscript accordingly. We shortened and tempered several statements in the Abstract, Results, and Discussion; reframed SHAP as descriptive model-attribution analysis rather than causal or interventional evidence; and added supporting-information captions for the new tables and figures. We also prepared a supplementary materials package with clearly labeled S1-S3 Tables and S1-S4 Figures. The calibration and decision-curve figures are explicitly labeled as internal classical-baseline evidence only.

**Actions taken:** Clinical-utility claims were softened, SHAP interpretation was made cautious, and supplementary figure/table captions were added. The submitted figure package should be checked for final numbering consistency before upload.

**Location in revised manuscript/supporting materials:** Abstract; Results; SHAP-based Feature Importance; Discussion; Supporting information captions; supplementary materials package.
