# AKI code reproducibility notes

These notes cover the runnable Python code under `D:\AKI\aki-master\aki-master`.
They do not change the original experimental design or manuscript claims.

## Paths

`config.py` resolves paths relative to this code directory by default:

- data workbook: `data\data.xlsx`
- image and YOLO annotation files: `data\images`
- saved model checkpoint: `model\aki_model（0.816）.pt`
- generated outputs: `result`

The default checkpoint can be changed without editing code:

```powershell
$env:AKI_MODEL_FILE = "aki_model.pt"
```

`AKI_CODE_ROOT` can also be set if the code directory is copied elsewhere.

## Environment

Use Python 3.9+ with the packages listed in `requirements-repro.txt`.
For GPU runs, install the PyTorch build that matches the local CUDA driver.
The code also runs on CPU for smoke checks, but full training and SHAP image
analysis can be slow.

The second-revision clinical baseline script is CPU-oriented and uses:

- Python 3.9+
- pandas
- openpyxl
- numpy
- scikit-learn
- matplotlib

```powershell
cd D:\AKI\aki-master\aki-master
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-repro.txt
```

## Entry points

Quick syntax/import check:

```powershell
cd D:\AKI\aki-master\aki-master
python -m py_compile config.py main.py evaluate_nested_cv01.py evaluate_nested_cv02.py hyperparam_search.py dual_input_model.py optimized_model.py augmentation_utils.py second_revision_analysis.py
```

Second-revision reviewer analysis:

```powershell
cd D:\AKI
python aki-master\aki-master\second_revision_analysis.py
```

Equivalent command from the code directory:

```powershell
cd D:\AKI\aki-master\aki-master
python second_revision_analysis.py
```

Default inputs:

- `D:\AKI\aki-master\aki-master\data\data.xlsx`
- `D:\AKI\aki-master\aki-master\data\images`

Default output directory:

- `D:\AKI\aki-master\aki-master\second_revision_results`

Optional arguments:

```powershell
python second_revision_analysis.py --help
python second_revision_analysis.py --data data\data.xlsx --image-dir data\images --output-dir second_revision_results
python second_revision_analysis.py --feature-set all_preop
```

The committed `second_revision_results\analysis_manifest.json` records the
settings used for the current reviewer-facing run: random seed `20260614`,
5 outer folds, 3 inner folds, 5 robustness repeats, and 1000 bootstrap
replicates.

Model training entry point:

```powershell
python main.py
```

This trains a model and writes `model\aki_model.pt`. It is a heavy run and
prompts whether to use tabular augmentation.

Nested cross-validation/evaluation entry points:

```powershell
python evaluate_nested_cv01.py
python evaluate_nested_cv02.py
```

Both scripts prompt whether to use augmentation. `evaluate_nested_cv02.py`
adds more output plots such as calibration and precision-recall summaries.

SHAP pipeline:

```powershell
cd D:\AKI\aki-master\aki-master\shap
python shap_runner.py
```

`shap_runner.py` now changes into its own directory, imports the project root
explicitly, and lists generated files using Python so it works on Windows.
`3_run_shap.py` remains interactive because it asks whether to include image
SHAP and whether to run slower pixel-level SHAP.

## Data availability and local-only inputs

The raw clinical workbook and case image/annotation files are intentionally
not pushed to GitHub:

- `aki-master\aki-master\data\data.xlsx`
- `aki-master\aki-master\data\images`

The complete second-revision analysis requires those local paths to exist.
This is deliberate because the workbook and images are private/raw clinical
materials. The script will fail early if it cannot locate `data\data.xlsx`.
Model checkpoints (`*.pt`, `*.pth`, `*.ckpt`, `*.pkl`) and archive files are
also intentionally excluded from Git.

## Reviewer-facing second-revision outputs

`second_revision_results` is tracked in Git and contains the outputs intended
for reviewer-response/manuscript-support use:

- `baseline_model_performance.csv`: pooled out-of-fold performance, calibration,
  and threshold metrics for the classical baselines.
- `baseline_fold_metrics.csv`: fold-level nested-CV metrics and selected
  hyperparameters.
- `robustness_repeated_cv_summary.csv` and
  `robustness_repeated_cv_metrics.csv`: repeated stratified 5-fold robustness
  results.
- `case_flow_audit.csv`: raw rows, exclusions, analyzed rows, and outcome
  counts.
- `image_availability_audit.csv`: local image/annotation availability audit.
- `feature_missingness.csv`: missingness by clinical predictor.
- `decision_curve_net_benefit.csv`: decision-curve net benefit values.
- `cross_validated_probabilities_deidentified.csv`: deidentified out-of-fold
  probabilities without patient IDs or sequence numbers.
- `baseline_roc_curves.png`, `baseline_precision_recall_curves.png`,
  `baseline_calibration_curves.png`, and `decision_curve_analysis.png`:
  reviewer-facing figures.
- `baseline_results_notes.md`: short methods/results notes for the revision
  package.
- `analysis_manifest.json`: run settings and feature list.

The outputs are internal cross-validation evidence only. Do not describe them
as external validation.

## Git tracking check

Current `.gitignore` behavior is intentional:

- tracked/committable: `second_revision_analysis.py`,
  `README_REPRODUCIBILITY.md`, `requirements-repro.txt`, and
  `second_revision_results`.
- ignored: raw `data\`, model/checkpoint files (`*.pt`, `*.pth`, `*.ckpt`,
  `*.pkl`), archives (`*.zip`, `*.7z`, `*.rar`), caches, and IDE metadata.

## Encoding notes

The Python source files are UTF-8 and contain Chinese column names that match
`data\data.xlsx`. If PowerShell displays mojibake, run:

```powershell
chcp 65001
$env:PYTHONUTF8 = "1"
```

Do not replace the Chinese column names unless the workbook schema changes.

## Current audit summary

- Hard-coded legacy paths in `config.py` were replaced with paths derived from
  this code directory.
- The existing checkpoint filename is `aki_model（0.816）.pt`; the missing
  legacy `aki_model.pt` is no longer the default for evaluation.
- The SHAP runner no longer depends on Unix `ls` or on being launched from the
  `shap` directory.
- `second_revision_analysis.py` can be run from either `D:\AKI` or
  `D:\AKI\aki-master\aki-master`; it writes reproducible reviewer-facing
  outputs under `second_revision_results`.
- Existing results, data, checkpoints, and experimental logic were left intact.
