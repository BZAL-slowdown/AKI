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
python -m py_compile config.py main.py evaluate_nested_cv01.py evaluate_nested_cv02.py hyperparam_search.py dual_input_model.py optimized_model.py augmentation_utils.py
```

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
- Existing results, data, checkpoints, and experimental logic were left intact.
