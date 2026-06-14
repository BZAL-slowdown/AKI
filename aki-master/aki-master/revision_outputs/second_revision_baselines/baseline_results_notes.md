# Second-revision baseline analysis notes

- Data source: `D:\AKI\aki-master\aki-master\data\data.xlsx`.
- Feature set: `primary` with 11 preoperative clinical predictors.
- Rows read: 194; excluded before modeling because sequence or outcome was missing: 1; analyzed: 193 (132 postoperative AKI, 61 no postoperative AKI).
- Missing clinical values were not used for exclusion; they were median-imputed within each training fold.
- Image audit: 183 JPG files and 181 TXT annotation files in `data/images`.
- Clinical sequence numbers without JPG files: 14, 47, 88, 97, 99, 100, 125, 173, 174, 175.
- Classical baselines were evaluated using 5-fold stratified outer cross-validation with 3-fold inner hyperparameter selection by ROC AUC.
- Best baseline by cross-validated AUC: Gradient boosting AUC 0.636 (bootstrap 95% CI 0.548-0.718); Brier score 0.223.
- These are internal cross-validation results only. They should not be described as external validation or as proving clinical utility.

Predictors:

- 年龄
- 高血压（入院血压）
- 糖尿病（术前血糖）
- 是否独肾
- 血糖（术前）
- 尿素氮（术前）
- 乳酸（术前）
- 肌酐（术前）
- AST（术前）
- 中性粒细胞（术前）
- 白细胞（术前）
