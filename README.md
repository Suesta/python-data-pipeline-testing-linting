# python-data-pipeline-testing-linting

A lightweight, reproducible Python project that loads two university-level datasets (performance rate and first-year dropout rate), cleans and aggregates them, merges them into a single analytical table, generates trend visualizations, and exports a structured JSON statistical report.

The project is organized as a small data pipeline with basic quality checks: unit tests, coverage, linting (pylint), and auto-generated module documentation (pydoc).

---

## Project Overview

**Inputs**
- `rendiment_estudiants.xlsx`: performance indicators (e.g., *Taxa rendiment*).
- `taxa_abandonament.xlsx`: first-year dropout indicators (e.g., *% Abandonament a primer curs*).

**Outputs**
- A merged analysis table (created in-memory during execution).
- A trend figure saved to `src/img/`.
- A JSON report saved to `src/report/`.

**Quality evidence**
- Unit tests in `tests/`.
- Coverage and linting evidence stored as screenshots in `screenshots/`.
- Module documentation generated with `pydoc` in `doc/`.

---

## Repository Structure

```

PEC4_python_project/
├─ data/
│  ├─ rendiment_estudiants.xlsx
│  └─ taxa_abandonament.xlsx
├─ doc/
│  ├─ src.modules.load_eda.html
│  ├─ src.modules.clean_merge.html
│  ├─ src.modules.visualization.html
│  └─ src.modules.analysis_report.html
├─ screenshots/
│  ├─ 01_tests_ok.png
│  ├─ 02_coverage_ok.png
│  ├─ 03_doc_ok.png
│  └─ 04_pylint_ok.png
├─ src/
│  ├─ **init**.py
│  ├─ img/
│  │  └─ evolucion_nombre_alumno.png
│  ├─ modules/
│  │  ├─ **init**.py
│  │  ├─ load_eda.py
│  │  ├─ clean_merge.py
│  │  ├─ visualization.py
│  │  └─ analysis_report.py
│  └─ report/
│     └─ analisi_estadistic.json
├─ tests/
│  ├─ **init**.py
│  ├─ test_clean_merge.py
│  └─ test_analysis_report.py
├─ main.py
├─ requirements.txt
└─ LICENSE

````

> Note: a local virtual environment (e.g., `venv/`) should **not** be committed to GitHub.

---

## Requirements

- Python **3.11+** (tested with Python 3.11)
- Packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## How to Run

The project exposes a minimal CLI through `main.py`.

### Run all steps (Exercises 1 → 4)

```bash
python main.py
```

### Run only up to a specific exercise

* Up to Exercise 1:

```bash
python main.py -ex 1
```

* Up to Exercise 2:

```bash
python main.py -ex 2
```

* Up to Exercise 3:

```bash
python main.py -ex 3
```

### Show CLI help

```bash
python main.py -h
```

---

## Execution Flow (What Each Exercise Does)

### Exercise 1 — Load + Basic EDA

* Loads one of the two Excel datasets from `data/`.
* Prints:

  * first rows (`head`)
  * column names
  * `DataFrame.info()` summary

### Exercise 2 — Cleaning + Aggregation + Merge

* Loads both datasets.
* Standardizes and selects relevant columns.
* Aggregates to a common granularity (e.g., by academic year, university type, branch, gender, center type).
* Merges performance and dropout into a single dataset.

### Exercise 3 — Visualization

* Builds trend plots for:

  * first-year dropout (%)
  * performance rate
* Saves the figure to:

`src/img/evolucion_nombre_alumno.png`

### Exercise 4 — Statistical Analysis + JSON Report

* Computes global descriptive statistics (means).
* Computes Pearson correlation between dropout and performance.
* Computes per-branch summaries and simple linear trend information.
* Saves the output JSON to:

`src/report/analisi_estadistic.json`

---

## Outputs

### Figure

* `src/img/evolucion_nombre_alumno.png`

### JSON report

* `src/report/analisi_estadistic.json`

The JSON report includes:

* metadata (date, record count, time period)
* global statistics
* correlation results (Pearson r and p-value)
* per-branch descriptive stats and trend classification
* rankings (best/worst performance, highest/lowest dropout)

---

## Testing

Run unit tests:

```bash
python -m unittest discover -s tests -v
```

---

## Coverage

Install and run coverage:

```bash
pip install coverage
coverage run -m unittest discover -s tests -v
coverage report -m
```

Evidence is captured in:

* `screenshots/02_coverage_ok.png`

---

## Linting (pylint)

Install and run pylint:

```bash
pip install pylint
pylint main.py src/modules/*.py tests/*.py
```

Evidence is captured in:

* `screenshots/04_pylint_ok.png`

---

## Module Documentation (pydoc)

Generate HTML documentation for modules:

```bash
python -m pydoc -w src.modules.load_eda src.modules.clean_merge src.modules.visualization src.modules.analysis_report
```

Move generated HTML files into `doc/`:

```bash
move *.html doc\
```

Evidence is captured in:

* `screenshots/03_doc_ok.png`

---

## Reproducibility Notes

* The code uses **relative paths** (project-root based).
* The project is intended to be executed from the repository root (where `main.py` is located).
* Avoid committing local artifacts such as `venv/`, `__pycache__/`, and `.coverage`.

---

## License

This project is released under the license included in the repository (see `LICENSE`).

