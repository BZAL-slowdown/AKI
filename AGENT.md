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

## Immediate Next Steps

1. Agent 2 should produce baseline, calibration, DCA, and robustness evidence first.
2. Agent 3 should prepare reproducibility notes and minimal path/encoding fixes.
3. Agent 1 should draft the response using only verified evidence.
4. Agent 4 should update figure/submission checklists after new evidence exists.
5. The Project Lead should integrate accepted outputs, commit them, and push every meaningful checkpoint to GitHub.
