# NYC Taxi Data Platform

Work in progress. An end-to-end incremental batch pipeline over NYC TLC
yellow taxi data. Raw monthly files are ingested idempotently, validated
with automated data-quality rules, and bad records are quarantined instead
of dropped. Planned stack: Python, SQL, DuckDB, dbt, Airflow, Docker,
GitHub Actions.

## Why this project
Monthly public data arrives dirty and its schema can change. This project
guarantees that every raw row ends up either in a clean table or in a
quarantine table with the reason it was rejected.
