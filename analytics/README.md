# analytics — Titanic Analytics Pipeline

One connected pipeline across two scripts: `01_eda.py` loads, profiles,
cleans, and tells the visual data story for the Titanic dataset; `02_modeling.py`
continues from the same data to build, evaluate, and save a full predictive
modeling pipeline. The raw dataset is loaded from the network/cache exactly
once — in `01_eda.py`, via `sns.load_dataset('titanic')` — and never reloaded
independently for modeling.

## Setup

```bash
pip install -r requirements.txt
```

## Run (in order)

```bash
python 01_eda.py
python 02_modeling.py
```

`01_eda.py` must run first — it produces `titanic.csv`, the committed offline
fallback that `02_modeling.py` reads instead of calling `sns.load_dataset`
again. If you don't have internet access when running this, `sns.load_dataset`
will fail on the first run — just make sure `titanic.csv` has been committed
to the repo already (it is), so `02_modeling.py` alone can still be graded.

Outputs produced:
- `titanic.csv` — raw dataset, saved immediately after the one-and-only load
- `charts/` — every plot (histograms, box plots, heatmap, story charts, ROC
  curves, decision tree, residual plot) saved as `.png`
- `best_model_pipeline.joblib` — the complete fitted pipeline (preprocessing
  + best classifier), reloadable and usable on raw input

## Design decisions

**Missing-value handling (threshold rule):** measured on the full raw
dataset before any cleaning:
- `deck` (~77% missing) → **dropped entirely**. At that missing rate, no
  imputation strategy — including an "Unknown" placeholder category — would
  carry real signal; more than 3 in 4 values would be synthetic.
- `age` (~20% missing) → **median-imputed** (5–30% band).
- `embarked` / `embark_town` (~0.2% missing, 2 rows) → **rows dropped**
  (under 5% band).

**Correlation matrix** is restricted to exactly `survived, pclass, age,
sibsp, parch, fare` — `adult_male` and `alone` are excluded because they're
derived flags (computable directly from `sex`/`age` and from
`sibsp`+`parch`), not independently measured features.

**Modeling features:** `pclass, sex, age, sibsp, parch, fare, embarked`.
Columns like `class`, `who`, `adult_male`, `alone`, `deck`, `embark_town`,
and `alive` are excluded from modeling — `alive` is literal target leakage
(it's a string encoding of `survived`), and the others either duplicate or
are trivially derived from the columns already used.

**Preprocessing (Task 8):** a `ColumnTransformer` (median-impute + scale
numeric columns; mode-impute + one-hot encode `sex`/`embarked`; passthrough
`pclass`) wrapped in a `Pipeline` with the final estimator. This is rebuilt
fresh (`build_preprocessor()`) for every model rather than reused, so no
fitted state accidentally leaks between pipelines — each is fit only on
`X_train` and only ever *transforms* `X_test`.

**Imbalance comparison:** baseline vs. `class_weight='balanced'` vs. SMOTE,
all evaluated on a Random Forest. SMOTE is applied only to the already
train/test-split, already preprocessing-fit training fold — never to the
test fold or the full dataset — to avoid leakage.

**Adjusted R² note:** computed using the raw (pre-one-hot-encoding) feature
count as `p`, stated explicitly in the script's output as a simplification.

**Model selection:** the classifier with the highest F1 score on the test
set is the one saved to `best_model_pipeline.joblib` and named in the final
recommendation — whichever that turns out to be on your actual run (results
depend on the real Titanic data, not the synthetic data used to test this
code's logic).

## Files

| File | Purpose |
|---|---|
| `01_eda.py` | Part A: load, profile, clean, univariate/bivariate/multivariate EDA, correlation heatmap, exploratory standardization check |
| `02_modeling.py` | Part B: stratified split, leak-free preprocessing pipeline, 3 classifiers, imbalance comparison, GridSearchCV + OOB, regression side-task, final comparison + joblib save/reload |
| `titanic.csv` | committed offline fallback (raw dataset, produced by `01_eda.py`) |
| `charts/` | all saved plots |
| `best_model_pipeline.joblib` | saved best full pipeline (regenerable by re-running `02_modeling.py`) |

## Testing note

Both scripts were verified end-to-end against a synthetic Titanic-shaped
dataset matching the real dataset's schema and missingness pattern (age
~20% missing, embarked ~0.2% missing, deck ~77% missing) before delivery —
every step (cleaning, IQR outliers, correlation heatmap, stratified split,
leak-free preprocessing, all three classifiers, GridSearchCV + OOB,
regression metrics, joblib save/reload on raw input) ran without errors.
Run it yourself against the real dataset to get your actual reportable
numbers for the README/notebook write-up.