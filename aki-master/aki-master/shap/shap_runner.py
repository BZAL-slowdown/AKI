# shap/shap_runner.py
import os
import subprocess
import sys
from pathlib import Path


SHAP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SHAP_DIR.parent
os.chdir(SHAP_DIR)
sys.path.insert(0, str(PROJECT_ROOT))


SCRIPTS = [
    "1_load_model.py",
    "2_prepare_data.py",
    "3_run_shap.py",
    "4_visualize_shap.py",
]


def run(script, interactive=False):
    print(f"\n>>> Running {script}")
    cmd = [sys.executable, str(SHAP_DIR / script)]
    if interactive:
        proc = subprocess.run(cmd)
        if proc.returncode != 0:
            sys.exit(proc.returncode)
    else:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            print("[ERROR] Script failed:")
            print(result.stderr)
            sys.exit(result.returncode)
        print(result.stdout.strip())


def validate_outputs():
    required_inputs = ["X_val.npy", "X_tab_sample.npy"]
    if (SHAP_DIR / "X_img_sample.npy").exists():
        required_inputs.append("X_img_sample.npy")

    missing = [name for name in required_inputs if not (SHAP_DIR / name).exists()]
    if missing:
        print(f"[ERROR] Missing required input files: {missing}")
        sys.exit(1)

    shap_outputs = [
        name for name in ("shap_tab_values.npy", "shap_img_values.npy")
        if (SHAP_DIR / name).exists()
    ]
    if not shap_outputs:
        print("[ERROR] No SHAP output files were generated; check 3_run_shap.py.")
        sys.exit(1)

    print(
        "[OK] Required inputs and SHAP outputs are present:\n"
        f"  inputs: {required_inputs}\n"
        f"  outputs: {shap_outputs}"
    )


def print_matching_files(*patterns):
    for pattern in patterns:
        for path in sorted(SHAP_DIR.glob(pattern)):
            if path.is_file():
                print(f"{path.name}\t{path.stat().st_size} bytes")


if __name__ == "__main__":
    full_visualization = len(sys.argv) > 1 and sys.argv[1] in ("--full", "-f")
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Usage:")
        print("  python shap_runner.py")
        print("  python shap_runner.py --full")
        sys.exit(0)

    print("Starting SHAP analysis pipeline...")
    if full_visualization:
        print("Mode: full visualization")

    for idx, script in enumerate(SCRIPTS):
        run(script, interactive=(script == "3_run_shap.py"))
        if idx == 2:
            validate_outputs()

    if full_visualization:
        print("\nGenerating extra visualizations...")
        run("4_visualize_shap.py")

    print("\n[OK] SHAP analysis pipeline finished.")
    print("Generated files:")
    print_matching_files("shap_*", "X_*")
    plot_dir = SHAP_DIR / "shap_img_plots"
    if full_visualization and plot_dir.exists():
        print("\nImage SHAP plots:")
        for path in sorted(plot_dir.glob("*")):
            if path.is_file():
                print(f"{path.name}\t{path.stat().st_size} bytes")
