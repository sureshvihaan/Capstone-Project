# Capstone-Project
The Zepto Data &amp; AI Platform is an enterprise-grade ecosystem built for Zepto's analytics guild. It unifies three core capabilities in a single repo: automated data collection, predictive ML modeling, and a grounded GenAI support assistant designed to answer internal policy queries directly from company documents..
# Zepto Data & AI Platform

An end-to-end Artificial Intelligence and Machine Learning capstone project built for the **Zepto Data & AI Platform**.

This repository brings together data engineering, analytics and machine learning, and a grounded GenAI support assistant into one connected project. The objective is to demonstrate how raw data can be collected and transformed into structured data, how customer-style data can be explored and modeled, and how company documents can be used to build a grounded AI support experience.

> **Project:** Certificate Program in Artificial Intelligence and Machine Learning
> **Organization:** Zepto Data & AI Platform
> **Repository:** `sureshvihaan/Capstone-Project`

---

## Table of Contents

* [Project Overview](#project-overview)
* [Project Objectives](#project-objectives)
* [Repository Structure](#repository-structure)
* [Technology Stack](#technology-stack)
* [Prerequisites](#prerequisites)
* [Environment Setup](#environment-setup)
* [Module 1 — Data Pipeline](#module-1--data-pipeline)
* [Module 2 — Analytics and Machine Learning](#module-2--analytics-and-machine-learning)
* [Module 3 — GenAI Support Assistant](#module-3--genai-support-assistant)
* [Overall Architecture](#overall-architecture)
* [Design Decisions](#design-decisions)
* [Outputs](#outputs)
* [Testing and Validation](#testing-and-validation)
* [Git Workflow](#git-workflow)
* [Reproducibility](#reproducibility)
* [Limitations](#limitations)
* [Submission Checklist](#submission-checklist)

---

# Project Overview

The Zepto Data & AI Platform is designed as a single repository containing three complementary capabilities:

1. **Data Pipeline**
   Scrapes publicly available book-catalog data, cleans and transforms the data, converts prices from GBP to INR, stores the result in a normalized SQLite database, and performs SQL and pandas-based analysis.

2. **Analytics & Machine Learning**
   Performs exploratory data analysis on the Titanic dataset and builds an end-to-end machine learning workflow including preprocessing, classification, imbalance handling, hyperparameter tuning, evaluation, and model persistence.

3. **GenAI Support Assistant**
   Provides a document-grounded support assistant intended to answer policy questions using Zepto's internal documentation through retrieval-augmented generation and a structured API.

The three modules are intended to demonstrate an end-to-end AI/ML engineering workflow rather than three unrelated exercises.

---

# Project Objectives

The project focuses on the following engineering capabilities:

* Web data extraction
* Data cleaning and type conversion
* Relational database design
* SQL querying
* Exploratory data analysis
* Data visualization
* Feature engineering and preprocessing
* Machine learning model development
* Model evaluation and comparison
* Handling class imbalance
* Prevention of data leakage
* Model serialization
* Retrieval-augmented generation
* Document-grounded question answering
* Structured AI outputs
* API development
* Reproducible project organization

---

# Repository Structure

```text
Capstone-Project/
│
├── data_pipeline/
│   ├── pipeline.py
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── best_model_pipeline.joblib
│   ├── charts/
│   ├── requirements.txt
│   └── README.md
│
├── support_assistant/
│   └── ...
│
└── README.md
```

> The `support_assistant/` directory should be present in the final submission because it is a required module of the capstone. The current repository version should be updated with the completed implementation before submission.

---

# Technology Stack

## Data Pipeline

* Python
* Requests
* BeautifulSoup
* Pandas
* SQLite
* SQL

## Analytics & Machine Learning

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Imbalanced-learn / SMOTE
* Joblib
* Jupyter Notebook

## GenAI Support Assistant

The final implementation is expected to use:

* Python
* FastAPI
* LangGraph
* Embeddings
* Vector retrieval
* Structured outputs
* Document-grounded generation

The GenAI module should remain compatible with the assignment's deterministic offline/mock evaluation requirements.

---

# Prerequisites

Recommended environment:

* Python 3.10+
* Git
* pip
* Jupyter Notebook or JupyterLab for the analytics module

Clone the repository:

```bash
git clone https://github.com/sureshvihaan/Capstone-Project.git
cd Capstone-Project
```

It is recommended to use a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

# Environment Setup

This repository currently uses **module-level `requirements.txt` files** rather than one consolidated dependency file.

Install dependencies separately for each module.

## Data Pipeline

```bash
cd data_pipeline
pip install -r requirements.txt
```

## Analytics

```bash
cd analytics
pip install -r requirements.txt
```

## Support Assistant

Install the dependencies listed in:

```text
support_assistant/requirements.txt
```

after the GenAI module has been added to the repository.

---

# Module 1 — Data Pipeline

## Purpose

The data pipeline demonstrates an end-to-end ETL workflow:

```text
Public Web Data
      │
      ▼
   Scraping
      │
      ▼
Data Cleaning
      │
      ▼
Type Conversion
      │
      ▼
GBP → INR Conversion
      │
      ▼
Normalized SQLite Database
      │
      ▼
SQL Queries
      │
      ▼
Pandas Validation
```

The implementation uses `books.toscrape.com`, a public website designed for scraping practice. The pipeline does not require login credentials, an API key, or a paid service.

---

## Data Pipeline Technologies

* `requests` — HTTP requests
* `BeautifulSoup` — HTML parsing
* `pandas` — transformation and analysis
* `sqlite3` — relational storage

The module's requirements file currently contains Requests, BeautifulSoup4, and Pandas.

---

## Running the Data Pipeline

Navigate to the module:

```bash
cd data_pipeline
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python pipeline.py
```

The actual executable in the current repository is `pipeline.py`.

---

## Pipeline Steps

### 1. Web Scraping

The pipeline currently targets three book categories:

* Philosophy
* Mystery
* Historical Fiction

It iterates through category pages until no further page is available.

For every book, the pipeline extracts:

* Title
* Price
* Star rating
* Availability
* Category

---

### 2. Data Cleaning

The scraped price is converted into a numeric GBP value.

Star ratings such as:

```text
One
Two
Three
Four
Five
```

are converted into integer values from `1` to `5`.

Availability is converted into a boolean/integer representation.

Rows with unparseable required fields are removed.

---

### 3. Currency Conversion

The project uses the fixed assignment conversion rate:

```text
1 GBP = 105.50 INR
```

Therefore:

```text
price_inr = price_gbp × 105.50
```

This is a project-defined fixed rate rather than a live currency exchange rate.

---

### 4. SQLite Database

The pipeline creates:

```text
zepto_books.db
```

The database contains two normalized tables:

```text
categories
-----------
category_id       PRIMARY KEY
category_name     UNIQUE


books
-----------
book_id           PRIMARY KEY
title
price_gbp
price_inr
rating
in_stock
category_id       FOREIGN KEY
```

The categories table is populated first, and the generated category IDs are mapped to the books before inserting the book records.

---

## SQL Analysis

The pipeline demonstrates several SQL concepts:

* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* `BETWEEN`
* `IN`
* `JOIN`

Examples include:

* In-stock books below £20
* Five cheapest books
* Distinct categories
* Books within an INR price range
* Books rated 3–5 stars
* Five-star books joined with category information

The SQL JOIN result is also reproduced using `pandas.merge()` and compared against the SQL result.

---

# Module 2 — Analytics and Machine Learning

## Purpose

The analytics module provides an end-to-end data science workflow using the Titanic dataset.

The workflow is divided into two notebooks:

```text
01_eda.ipynb
      │
      ▼
Exploration + Cleaning
      │
      ▼
02_modeling.ipynb
      │
      ▼
Preprocessing + Modeling
      │
      ▼
Evaluation + Model Selection
      │
      ▼
best_model_pipeline.joblib
```

The repository currently contains:

* `01_eda.ipynb`
* `02_modeling.ipynb`
* `titanic.csv`
* `best_model_pipeline.joblib`
* `charts/`
* `requirements.txt`

---

## Running the Analytics Module

Navigate to:

```bash
cd analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the notebooks in this order:

```text
01_eda.ipynb
02_modeling.ipynb
```

The EDA stage should be completed before the modeling stage.

---

## Exploratory Data Analysis

The EDA workflow includes:

* Dataset loading
* Dataset profiling
* Missing-value analysis
* Univariate analysis
* Bivariate analysis
* Multivariate analysis
* Correlation analysis
* Outlier analysis
* Visualization
* Exploratory standardization checks

The generated visualizations are stored in:

```text
analytics/charts/
```

---

## Missing-Value Strategy

The implementation applies a threshold-based strategy:

| Column        | Missingness | Strategy           |
| ------------- | ----------: | ------------------ |
| `deck`        |        ~77% | Drop column        |
| `age`         |        ~20% | Median imputation  |
| `embarked`    |       ~0.2% | Drop affected rows |
| `embark_town` |       ~0.2% | Drop affected rows |

The rationale is to avoid introducing artificial information where a feature contains excessive missing data while preserving useful information from moderately incomplete features.

---

# Machine Learning Pipeline

The modeling workflow uses the following features:

```text
pclass
sex
age
sibsp
parch
fare
embarked
```

Columns that duplicate the target or contain derived/redundant information are excluded.

In particular, `alive` is excluded because it directly encodes the target `survived`, which would constitute target leakage.

---

## Preprocessing

The project uses a Scikit-learn `ColumnTransformer` and `Pipeline`.

The preprocessing includes:

### Numerical Features

* Median imputation
* Scaling

### Categorical Features

* Mode/most-frequent imputation
* One-hot encoding

### Passthrough Features

* `pclass`

The preprocessing pipeline is fitted only on the training data and then applied to the test data to prevent leakage.

---

## Class Imbalance

The implementation compares different approaches to class imbalance:

1. Baseline Random Forest
2. Random Forest with `class_weight="balanced"`
3. Random Forest with SMOTE

SMOTE is applied only to the training portion after the train/test split, ensuring that information from the test set does not leak into model training.

---

## Model Evaluation

The modeling workflow includes:

* Multiple classifiers
* Stratified train/test splitting
* Cross-validation
* `GridSearchCV`
* Random Forest OOB evaluation
* F1-score comparison
* Classification evaluation
* Regression side-task
* Final model comparison

The model with the highest F1 score on the test set is selected as the final model.

---

## Saved Model

The final fitted pipeline is stored as:

```text
analytics/best_model_pipeline.joblib
```

Because preprocessing and the classifier are stored together, the saved artifact can be reloaded and used on raw input data.

---

# Module 3 — GenAI Support Assistant

## Purpose

The third module is designed to demonstrate a grounded GenAI support service for Zepto.

The intended flow is:

```text
User Question
      │
      ▼
FastAPI Endpoint
      │
      ▼
LangGraph Router
      │
      ├── Relevant Policy Query
      │          │
      │          ▼
      │      Retriever
      │          │
      │          ▼
      │      Grounded Context
      │          │
      │          ▼
      │      LLM / Mock LLM
      │
      └── Other Query
                 │
                 ▼
              Response
      │
      ▼
Structured Output
```

The capstone requires this module to provide document-grounded answers, use a LangGraph-orchestrated flow, guarantee structured output, and expose the service through FastAPI.

---

## Expected Components

The completed module should contain the relevant implementation for:

* Policy/document corpus
* Document loading
* Text chunking
* Embedding generation
* Vector index
* Retrieval
* LangGraph workflow
* Query routing
* Grounded response generation
* Structured response schema
* Offline/mock LLM mode
* FastAPI endpoint
* Tests

> **Important:** The current GitHub `main` branch does not yet show a `support_assistant/` directory. Add the completed module before treating this repository as final submission-ready.

---

# Overall Architecture

The complete project can be viewed as three connected engineering layers:

```text
                    ZEpto Data & AI Platform
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 Data Engineering       Analytics / ML       GenAI Assistant
        │                    │                    │
        ▼                    ▼                    ▼
 Web Scraping           EDA + Cleaning       Documents
        │                    │                    │
        ▼                    ▼                    ▼
 Data Cleaning          Preprocessing        Chunking
        │                    │                    │
        ▼                    ▼                    ▼
 SQLite Database        ML Models            Embeddings
        │                    │                    │
        ▼                    ▼                    ▼
 SQL Analysis           Evaluation           Retrieval
                             │                    │
                             ▼                    ▼
                        Saved Model          LangGraph
                                                  │
                                                  ▼
                                               FastAPI
```

Together, these components demonstrate data collection, structured storage, analysis, predictive modeling, and grounded AI application development.

---

# Design Decisions

## Data Pipeline

### Public data source

A public scraping-practice website was selected so that the pipeline can run without authentication, paid APIs, or API credentials.

### Normalized relational schema

The database separates categories and books into two tables and connects them using a foreign key.

This avoids repeating category names across every book record.

### Fixed currency conversion

A fixed GBP-to-INR conversion rate is used to satisfy the project requirement without introducing dependency on a live currency API.

### Drop invalid rows

Rows that fail to provide valid title, price, or rating information are removed instead of generating artificial values through imputation.

---

## Analytics

### Threshold-based missing-value handling

The missing-value strategy is based on the proportion of missing values rather than applying one method indiscriminately to every column.

### Leakage prevention

Features that duplicate the target or are derived from other selected variables are excluded.

### Pipeline-based preprocessing

Preprocessing is kept inside a Scikit-learn pipeline so that transformations are learned from training data only.

### Imbalance evaluation

Multiple imbalance strategies are compared instead of assuming that one technique will always produce the best model.

### Model persistence

The complete preprocessing and modeling pipeline is saved as a Joblib artifact so that the final model can be reused.

---

## GenAI

### Retrieval-grounded generation

The support assistant is designed to answer policy questions using retrieved company documents rather than relying entirely on model memory.

### Graph-based orchestration

LangGraph is used to make routing and retrieval steps explicit and controllable.

### Structured responses

The API is designed around a defined response schema so that downstream applications can reliably consume the result.

### Offline evaluation

The implementation should support deterministic mock LLM behavior so that the pipeline can be evaluated without requiring paid external model APIs.

---

# Outputs

## Data Pipeline

Expected output:

```text
zepto_books.db
```

The terminal also displays the results of the SQL queries and the SQL-vs-pandas validation.

---

## Analytics

Expected outputs include:

```text
titanic.csv
charts/
best_model_pipeline.joblib
```

The analytics module also produces evaluation results and visualizations during notebook execution.

---

## GenAI Support Assistant

The completed module should provide:

```text
FastAPI service
Structured JSON response
Retrieved document context
Grounded answer
```

---

# Testing and Validation

The project should be validated module by module.

## Data Pipeline

Verify:

* Scraping completes successfully
* Expected categories are collected
* Price conversion succeeds
* Invalid rows are handled
* SQLite database is created
* Both tables exist
* Foreign-key relationship is populated
* SQL queries execute successfully
* SQL JOIN and pandas JOIN produce equivalent results

The current implementation explicitly compares the SQL JOIN result against a pandas merge and prints whether the outputs match.

---

## Analytics

Verify:

* EDA notebook runs successfully
* Missing values are handled correctly
* Train/test split is performed correctly
* Preprocessing is fitted only on training data
* Models train without leakage
* Imbalance methods are evaluated correctly
* Hyperparameter search completes
* Final model is saved
* Saved model can be reloaded

---

## GenAI

Verify:

* Documents are indexed
* Retrieval returns relevant context
* Routing works correctly
* Responses follow the required schema
* Mock/offline mode is deterministic
* FastAPI endpoint responds successfully
* Unsupported/unanswerable queries are handled safely

---

# Reproducibility

The project is designed so that each module can be executed independently.

### Data Pipeline

```bash
cd data_pipeline
pip install -r requirements.txt
python pipeline.py
```

### Analytics

```bash
cd analytics
pip install -r requirements.txt
```

Then execute:

```text
01_eda.ipynb
02_modeling.ipynb
```

### GenAI Support Assistant

After the module is added:

```bash
cd support_assistant
pip install -r requirements.txt
```

Then follow the module-specific instructions for starting the FastAPI application.

---

# Git Workflow

Git history is part of the capstone evaluation.

The required workflow includes:

1. Create a feature branch from `main`
2. Make and commit changes on the feature branch
3. Make at least two commits on that branch
4. Merge the feature branch back into `main`
5. Preserve the merge history

Example:

```bash
git checkout main

git checkout -b feature/project-improvements

git add .
git commit -m "Add project improvements"

git add .
git commit -m "Update documentation and validation"

git checkout main
git merge feature/project-improvements
```

Verify the history:

```bash
git log --graph --oneline --all
```

The assignment specifies that the branch and merge activity is evaluated across the repository rather than separately for each module.

---

# Limitations

### Data Pipeline

The pipeline uses a public scraping-practice website and therefore should not be interpreted as a production Zepto catalog ingestion system.

The currency conversion uses a fixed project-defined rate rather than a live exchange rate.

### Analytics

The Titanic dataset is used as the customer/passenger-style modeling dataset for the assignment. Model metrics can vary depending on the exact dataset version and execution environment.

### GenAI

The support assistant is intended to answer questions grounded in the supplied document corpus. It should not be treated as a general-purpose knowledge system.

---

# Submission Checklist

Before submitting the repository, verify the following:

* [ ] Repository is public
* [ ] One root `README.md` exists
* [ ] `data_pipeline/` exists
* [ ] `analytics/` exists
* [ ] `support_assistant/` exists
* [ ] Each module contains its required dependencies
* [ ] Data pipeline runs end-to-end
* [ ] SQLite database is generated correctly
* [ ] Analytics EDA runs successfully
* [ ] Analytics modeling runs successfully
* [ ] Saved model can be reloaded
* [ ] GenAI support assistant runs locally
* [ ] FastAPI endpoint works
* [ ] Structured output is enforced
* [ ] Offline/mock evaluation works
* [ ] Git feature branch exists
* [ ] Feature branch contains at least two commits
* [ ] Feature branch was merged into `main`
* [ ] `git log --graph --all` shows the required workflow
* [ ] No unnecessary screenshots, PDFs, slides, or videos are included
* [ ] No API keys or secrets are committed
* [ ] Final GitHub repository contains all required deliverables

---

# Current Repository Status

The repository currently contains the data pipeline and analytics modules. The data pipeline uses `pipeline.py` and the analytics module contains the EDA and modeling notebooks.

The final capstone submission requires the third `support_assistant/` module as well. Therefore, this README should be kept as the root project documentation and updated once the GenAI module is added and tested.

---

# Project Summary

This capstone demonstrates an end-to-end AI/ML engineering workflow:

```text
Collect
   ↓
Clean
   ↓
Store
   ↓
Analyze
   ↓
Model
   ↓
Evaluate
   ↓
Retrieve
   ↓
Generate
   ↓
Serve
```

The project combines traditional data engineering, analytics and machine learning, and modern retrieval-grounded GenAI into a single Zepto-focused platform.

---

## Repository

**GitHub:** `sureshvihaan/Capstone-Project`

**Main branch:** `main`

---

## License

This repository was created as an academic capstone project for the Certificate Program in Artificial Intelligence and Machine Learning.
