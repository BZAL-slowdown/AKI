# AKI Project Agent Coordination

## Project Purpose

This workspace contains the materials for the second revision of a PLOS ONE manuscript:

**Few-Shot Prediction of Post-Fusion Acute Kidney Injury Using Multimodal Radiomics-Clinical Feature-Based Prototype Networks**

The project combines:

- manuscript and response documents for PLOS ONE revision;
- clinical and imaging data for postoperative AKI prediction;
- Python code for multimodal few-shot/prototypical-network modeling;
- generated ROC, calibration, SHAP, feature-importance, and manuscript figures;
- submission-ready figure files and source figure files.

Current priority: prepare a rigorous second-round revision package by addressing reviewer concerns about external validity, overfitting, missing intraoperative variables, model complexity, baseline model comparison, calibration, decision-curve analysis, and restrained clinical claims.

## Repository And Backup Rules

- The workspace root `D:\AKI` is the Git repository root.
- Remote repository: `https://github.com/BZAL-slowdown/AKI.git`
- Commit meaningful checkpoints before and after code or document changes.
- Push committed work to GitHub whenever code, analysis scripts, generated tables, or coordination files are changed and the local credentials allow it.
- Do not commit private credentials, tokens, editor caches, Python caches, or large temporary archives unless they are intentionally part of the project record.
- Before editing, check `git status --short`.
- Do not revert changes made by other agents unless the project lead explicitly asks.

## Agent Boundaries

The current thread is the **Project Lead / Coordinator**. It answers questions, assigns work, maintains this file, manages Git/GitHub, and integrates final outputs.

Subagents must keep their scopes separate:

- Manuscript/response agents should not modify model code except to request evidence from the analysis agent.
- Analysis/code agents should not rewrite manuscript prose except for short notes explaining results.
- Figure/submission agents should not alter scientific conclusions or model outputs.
- Repository agents should not change manuscript content or analysis logic unless asked.

All agents should update the "Progress Log" section when they complete a meaningful unit of work.

## Subagent Assignments

### Agent 1: Reviewer Response And Manuscript Strategy

Scope:

- Read the second reviewer report and first-round response format.
- Draft a point-by-point second-round response.
- Identify exact manuscript sections that need edits.
- Temper clinical utility claims where evidence is limited.
- Explicitly handle lack of external validation and missing intraoperative variables.

Do not:

- invent experiments or results;
- claim external validation exists;
- edit code.

Expected outputs:

- response outline;
- proposed manuscript edits;
- list of evidence needed from Agent 2.

### Agent 2: Statistical Analysis And Baseline Experiments

Scope:

- Audit `aki-master\aki-master\data\data.xlsx` and image availability.
- Create or repair a reproducible second-revision analysis script using real Chinese column names.
- Add classical baseline comparisons where feasible, such as penalized logistic regression, random forest, gradient boosting, and support vector machine.
- Add calibration metrics and decision-curve analysis.
- Produce tables/figures for the revision package.

Do not:

- overstate performance;
- silently drop cases without reporting counts;
- modify manuscript prose beyond short notes.

Expected outputs:

- clean analysis script;
- result tables and figures;
- short methods/results notes for Agent 1.

### Agent 3: Codebase Cleanup And Reproducibility

Scope:

- Audit hard-coded paths, encoding issues, dependency assumptions, and runnable entry points.
- Propose minimal fixes to make the analysis reproducible from `D:\AKI`.
- Add a concise README or run notes if needed.
- Keep original experimental code intact unless a narrow compatibility fix is required.

Do not:

- retrain heavy models unless explicitly requested;
- delete old results;
- alter scientific claims.

Expected outputs:

- reproducibility checklist;
- minimal code/config fixes;
- run commands and dependency notes.

### Agent 4: Figures, Submission Package, And Formatting

Scope:

- Audit figure files, captions, order, and PLOS ONE formatting expectations.
- Verify which figures correspond to manuscript claims.
- Prepare a list of required figure/table replacements after Agent 2 finishes.
- Check support information consistency.

Do not:

- change numerical results;
- rewrite major manuscript sections;
- edit model code.

Expected outputs:

- figure inventory;
- formatting/action checklist;
- caption or supplementary-material consistency notes.

## Current Project Facts

- Data file: `D:\AKI\aki-master\aki-master\data\data.xlsx`
- Data shape: 194 rows, 47 columns.
- Outcome column: `急性肾损伤术后`
- Outcome distribution currently observed: 132 positive, 61 negative, 1 missing.
- Image files observed: 183 JPG files.
- YOLO annotation files observed: 181 TXT files.
- Clinical rows without matching JPG files: 14, 47, 88, 97, 99, 100, 125, 173, 174, 175.
- JPG files without matching TXT annotations: 101, 164.
- Existing manuscript-reported fused model AUC: 0.816.
- Existing manuscript-reported clinical-only AUC: 0.578.
- Existing manuscript-reported imaging-only AUC: 0.510.

## Progress Log

- 2026-06-14: Project contents reviewed. The workspace was identified as a PLOS ONE second-revision package plus AKI multimodal few-shot model code/data/results.
- 2026-06-14: Second-round reviewer concerns summarized: external validity/overfitting, incomplete clinical variables, model complexity, insufficient baseline comparisons, calibration/DCA, and claim tempering.
- 2026-06-14: Coordination file `AGENT.md` created. GitHub remote target recorded as `https://github.com/BZAL-slowdown/AKI.git`.
- 2026-06-14: Agent 4 completed a figure/submission-format audit in `Agent4_Figure_Submission_Audit.md`; current Fig 1 needs 300-600 dpi re-export, current Fig 7-10 should be replaced if Agent 2 revises performance/SHAP outputs, and calibration/DCA/baseline comparison materials are still pending Agent 2 evidence.
- 2026-06-14: Four subagent threads created: Agent 1 Reviewer Response, Agent 2 Statistical Analysis, Agent 3 Reproducibility, and Agent 4 Figures/Submission.
- 2026-06-14: Git repository initialized at `D:\AKI`; initial code/manuscript/figure coordination backup committed and pushed to GitHub `main`. Raw clinical data, raw case images, model weights, archives, caches, and generated large result folders were intentionally excluded from the first push.
- 2026-06-14: Project Lead assigned the first active revision task to Agent 2: baseline model comparison, calibration analysis, decision-curve analysis, and robustness evidence for the second-round reviewer comments.
- 2026-06-14: Agent 3 completed a reproducibility cleanup pass under `D:\AKI\aki-master\aki-master`: replaced hard-coded legacy paths in `config.py` with project-relative paths, set the default checkpoint to the existing `model\aki_model（0.816）.pt`, rewrote `shap\shap_runner.py` to be Windows/cwd-safe, and added `README_REPRODUCIBILITY.md` plus `requirements-repro.txt`.
- 2026-06-14: Agent 2 added and ran `aki-master\aki-master\second_revision_baselines.py`, producing an auditable 193-case internal-CV baseline comparison, calibration plots/metrics, decision-curve analysis, image-availability audit, and short revision notes under `aki-master\aki-master\revision_outputs\second_revision_baselines`; best classical baseline was gradient boosting with AUC 0.636 (bootstrap 95% CI 0.548-0.718), supporting restrained internal-validation claims only.
- 2026-06-14: Agent 2 added and ran the requested clean script `aki-master\aki-master\second_revision_analysis.py`, saving reviewer-facing outputs to `aki-master\aki-master\second_revision_results`. The analysis reports 194 raw rows, 1 missing postoperative-AKI/sequence row excluded, 193 tabular cases analyzed, 183 JPGs, 181 TXT annotations, 10 clinical rows without JPGs, and 2 JPGs without TXT. Primary nested-CV classical baselines again favored gradient boosting (AUC 0.636, bootstrap 95% CI 0.548-0.718; Brier 0.223), while repeated stratified 5-fold robustness checking gave gradient boosting mean AUC 0.628 +/- 0.084 SD; these remain internal-validation evidence only.
- 2026-06-14: Agent 1 read the second reviewer report, first-round response format, revised manuscript, track-changes manuscript, and supporting information; drafted `agent1_second_round_response_strategy.md` with point-by-point response strategy, exact manuscript edit targets, claim-tempering guidance, and evidence requests for Agent 2.
- 2026-06-14: Agent 1 integrated Agent 2's verified baseline/calibration/DCA/robustness outputs into reviewer-response strategy; created `second_revision_response_draft.md` with response-letter paragraphs, manuscript edit locations, and proposed supplementary tables/figures, and updated `agent1_second_round_response_strategy.md` with the real internal-validation results.
- 2026-06-14: Agent 4 created `second_revision_submission_package` with S1-S3 supplementary tables, S1-S4 supplementary figures, source-file copies, and `supplementary_materials_manifest.md`; calibration and DCA are explicitly labeled as internal classical-baseline evidence only, not final multimodal-model clinical-utility proof.
- 2026-06-14: Project Lead assigned the next two integration tasks: Agent 4 will prepare the second-revision supplementary tables/figures package from Agent 2 outputs, and Agent 3 will update reproducibility notes so `second_revision_analysis.py` can be rerun from the local project.
- 2026-06-14: Agent 3 updated `aki-master\aki-master\README_REPRODUCIBILITY.md` for `second_revision_analysis.py`, documenting run commands, local-only raw data/image requirements, dependencies, reviewer-facing files in `second_revision_results`, and `.gitignore` behavior for scripts, results, raw data, model weights, and archives.

## Immediate Next Steps

1. Agent 4 is preparing the supplementary tables/figures package for the second revision.
2. Agent 3 is updating reproducibility notes for `second_revision_analysis.py`.
3. The Project Lead should review Agent 4 and Agent 3 outputs, then integrate the formal `Response to Reviewers` document.
4. The Project Lead should revise the manuscript using Agent 1's edit map and only verified Agent 2 evidence.
5. The Project Lead should commit and push every meaningful checkpoint to GitHub.
