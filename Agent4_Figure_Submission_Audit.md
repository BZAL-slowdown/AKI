# Agent 4 Figure And Submission Formatting Audit

Date: 2026-06-14

Scope: figure files, figure order/captions, submission-package formatting, and supporting-information consistency for the PLOS ONE second revision. This audit does not change numerical results, manuscript claims, or model code.

## Sources Checked

- Manuscript: `D:\AKI\Revised Manuscript with Track Changes.docx`
- Supporting information: `D:\AKI\Supporting information.docx`
- Submission TIFFs: `D:\AKI\Figure\compressed\Fig1.tiff` through `Fig10.tiff`
- Figure source files: `D:\AKI\<Chinese-named original-images folder>\<same original-images subfolder>\Fig1.*` through `Fig10.*`
- Analysis outputs related to current figures: `D:\AKI\aki-master\aki-master\result\0.816\*.png` and `D:\AKI\aki-master\aki-master\shap\*.png`
- PLOS ONE figure guidance: https://journals.plos.org/plosone/s/figures
- PLOS ONE supporting-information guidance: https://journals.plos.org/plosone/s/supporting-information

## PLOS ONE Formatting Targets

- Main figures should be submitted as TIFF or EPS files, named by figure number.
- Production figures should generally be 300-600 dpi; PLOS NAAS also requires source figures captured in that range.
- Figures should be RGB or grayscale, under 10 MB, and clear/readable at final size.
- Figure captions belong in the manuscript file, not as separate image text-only files.
- Figures must be cited in ascending numeric order at first mention.
- Supporting-information files should use an `S` number in the item name/caption, and supporting-information captions should appear at the end of the manuscript file. PLOS recommends supporting-information files under 10 MB.

## Submission Figure Inventory

| Figure | Caption in manuscript | Current file | Technical status | Notes |
|---|---|---|---|---|
| Fig 1 | Participant Eligibility Criteria | `Figure\compressed\Fig1.tiff` | 3644x1877 px, RGB, LZW, 144 dpi, 2.0 MB | Content matches cohort-screening claim, but dpi is below 300. Regenerate/export at 300-600 dpi. |
| Fig 2 | Three-step data augmentation strategy for negative-class samples | `Figure\compressed\Fig2.tiff` | 5666x4780 px, RGB, LZW, 330 dpi, 3.8 MB | Matches augmentation-method claim. |
| Fig 3 | Multimodal Feature Fusion Network | `Figure\compressed\Fig3.tiff` | 6274x5702 px, RGB, LZW, 330 dpi, 4.9 MB | Matches architecture claim. |
| Fig 4 | Process for Generating Multiple Prototypes | `Figure\compressed\Fig4.tiff` | 5212x3493 px, RGB, LZW, 330 dpi, 2.1 MB | Matches multi-prototype/KMeans claim. |
| Fig 5 | Training Workflow | `Figure\compressed\Fig5.tiff` | 5067x6873 px, RGB, LZW, 330 dpi, 3.9 MB | Matches training-workflow claim. |
| Fig 6 | Model Evaluation Workflow | `Figure\compressed\Fig6.tiff` | 2604x3393 px, RGB, LZW, 330 dpi, 1.6 MB | Matches evaluation-workflow claim. |
| Fig 7 | Overall ROC Curve | `Figure\compressed\Fig7.tiff` | 2022x1517 px, RGB, LZW, 330 dpi, 0.3 MB | Displays AUC = 0.816, matching current manuscript claim. |
| Fig 8 | Five-fold Cross-validation - Confusion Matrix | `Figure\compressed\Fig8.tiff` | 5592x2905 px, RGB, LZW, 330 dpi, 1.4 MB | Matches per-fold confusion-matrix claim. |
| Fig 9 | Five-fold Cross-validation - ROC Curves | `Figure\compressed\Fig9.tiff` | 4518x2407 px, RGB, LZW, 330 dpi, 0.9 MB | Matches per-fold ROC claim. |
| Fig 10 | Feature Importance for Postoperative AKI Prediction | `Figure\compressed\Fig10.tiff` | 4410x2688 px, RGB, LZW, 330 dpi, 1.2 MB | Matches SHAP/feature-importance claim; verify final feature ordering after Agent 2 if SHAP is rerun. |

## Caption And Citation Audit

- The manuscript contains captions for Fig 1 through Fig 10 and Table 1.
- First figure mentions are in ascending order: Fig 1, Fig 2, Fig 3, Fig 4, Fig 5, Fig 6, Fig 7, Fig 8, Fig 9, Fig 10.
- Current figure captions are short and mostly usable, but several should be expanded before resubmission to define abbreviations and allow readers to understand the figure without returning to the main text. Priority captions: Fig 3, Fig 5, Fig 6, Fig 7, Fig 8, Fig 9, Fig 10.
- Current main-text claims tied to figures:
  - Fig 1: final study cohort of 194 subjects and AKI/non-AKI grouping.
  - Fig 2: anchor/pseudo-sample and negative-class augmentation strategy.
  - Fig 3: multimodal fusion network with ResNet-50 image branch, MLP tabular branch, gated fusion, and projection.
  - Fig 4: multi-prototype generation using class grouping, KMeans clustering, mean fallback, and L2 normalization.
  - Fig 5: training workflow and loss optimization.
  - Fig 6: nested cross-validation / model-evaluation workflow.
  - Fig 7: overall ROC/AUC = 0.816.
  - Fig 8: per-fold confusion matrices.
  - Fig 9: per-fold ROC curves.
  - Fig 10: SHAP-based clinical feature importance.

## Required Replacements Or Additions After Agent 2

These should wait until Agent 2 finalizes the second-revision analyses.

1. Replace Fig 7 if the revised fused-model AUC, thresholds, calibration, or evaluation protocol changes.
2. Replace Fig 8 and Fig 9 if Agent 2 changes the fold splits, confusion matrices, or per-fold ROC outputs.
3. Add or replace a figure/table for classical baseline comparisons if Agent 2 produces logistic regression, random forest, gradient boosting, SVM, or other baseline model results. A compact table is likely preferable unless the response strategy needs a plotted comparison.
4. Add a calibration figure/table if Agent 2 produces validated calibration metrics. Current production figure set has no calibration figure. Only `result\0.79\calibration_curve.png` was found, which does not correspond to the manuscript-reported AUC = 0.816 run.
5. Add a decision-curve analysis figure if Agent 2 produces DCA. No current DCA file was found.
6. Replace Fig 10 if Agent 2 reruns feature-importance/SHAP using a revised model, cohort, preprocessing, or final selected feature set.
7. If the manuscript keeps claims about clinical utility, add a figure/table or response text keyed to calibration/DCA evidence; otherwise the figure package should avoid implying decision-curve or calibration support that is not shown.

## Supporting Information Consistency

- `Supporting information.docx` contains S1 Appendix through S7 Appendix, with no separate supporting figures/tables.
- It references main-manuscript Fig. 2 inside S2 Appendix. That is acceptable as a main-figure cross-reference, but it should remain clear that Fig 2 is not a separate supporting-information file.
- No supporting-information captions were found in the manuscript text. If PLOS submission treats `Supporting information.docx` as the only supporting file, add a manuscript-end caption such as `S1 Appendix. Supporting information.` or split/rename files so the manuscript caption matches the uploaded supporting-information item.
- The supporting-information file is small (<1 MB), within PLOS recommended size expectations.

## Immediate Action Checklist

- Regenerate `Fig1.tiff` from its source figure at 300-600 dpi while preserving the current visual content and filename.
- Run all ten final TIFFs through PLOS NAAS before upload and keep the NAAS reports with submission materials.
- Expand terse captions after Agent 1 finalizes manuscript wording, especially for the ROC, confusion-matrix, and SHAP figures.
- After Agent 2 finishes, update this audit with final replacement filenames and mark which figure/table numbers changed.
- Do not upload current `result\0.816\*.png` files as production figures without re-export: they are low-resolution 640x480 RGBA PNGs and are source/evidence files only.
