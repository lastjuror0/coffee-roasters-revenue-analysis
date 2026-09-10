# Product Optimization & Revenue Contribution Analysis

Analyzes transaction-level sales data for Afficionado Coffee Roasters to uncover product popularity vs. revenue contribution, category-level revenue dependency, and underperforming menu items.

**Key finding:** Coffee and Tea account for 67% of total revenue; popularity and revenue are only moderately correlated (0.61), meaning high sales volume doesn't always translate to strong revenue.

## Repo Structure

```
├── notebooks/
│   └── product_analysis.ipynb         # Data cleaning, normalization, EDA
├── dashboard/
│   └── app.py                         # Streamlit product performance dashboard
├── Coffee_Roasters_Project.docx       # Full write-up (methodology, results, limitations)
└── README.md
```

## Setup

```bash
git clone <repo-url>
cd coffee-roasters-analysis
pip install -r requirements.txt
```

## Usage

```bash
jupyter notebook notebooks/product_analysis.ipynb
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Tech Stack

Python · pandas · matplotlib · DuckDB · Streamlit

## Key Insights

| Area | Finding |
|---|---|
| Category Dependency | Coffee (39%) + Tea (28%) = 67% of total revenue |
| Top Products (Revenue) | Barista Espresso, Brewed Chai Tea, Hot Chocolate |
| Top Products (Volume) | Brewed Chai Tea, Gourmet Brewed Coffee |
| Popularity vs Revenue | Moderate correlation (0.61) — volume doesn't always predict revenue |
| Pareto Analysis | ~40 of 80 products drive 80% of revenue (flatter than typical 80/20) |

Full methodology, normalization approach, and limitations are documented in [`Coffee_Roasters_Project.docx`](./Coffee_Roasters_Project.docx).

## Status

Analysis and dashboard complete.
