# Chess Data Platform

An end-to-end data pipeline built on Lichess monthly game files.

**Status: work in progress.**

## The problem
Lichess publishes every rated game as one large monthly PGN file. The files
are not cumulative, some fields are missing or unknown, and a monthly file
can contain games dated in the previous month. This project loads these
files into a warehouse in a repeatable way, keeps bad rows in a quarantine
table with the reason, and builds analytics tables on top.

## What it will show
- Idempotent loading: running the same file twice gives the same result
- Schema drift detection when new header fields appear
- Data quality rules with a quarantine table
- Incremental loads, backfill, and anomaly detection on daily game counts

## Data
Lichess open database, 2015 monthly files (CC0). Older files are used because
recent monthly files are too large for a laptop.

## Stack
Python, DuckDB, dbt, Airflow, GitHub Actions.