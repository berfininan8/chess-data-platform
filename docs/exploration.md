# Data exploration (Jan-Jun 2026)

Source: NYC TLC Yellow Taxi monthly Parquet files (Jan-Jun 2026) and the taxi zone lookup table.

## What I found
- 6 files, 20 columns in Jan-May, including `cbd_congestion_fee` (added in 2025).
- About 22.8M rows in total, 3.4M to 4.1M per month.
- February looks low (3.40M rows) only because it has 28 days. Rows per day are
  120k-132k in every month, so anomaly detection will use daily counts.
- Schema drift: June has one extra column, `request_source` (VARCHAR), at the end.
  It is NULL for 2,824,068 of 3,837,248 rows (73.6%). Other values: HV0003, A, EH0004, CC.
- Many of the first sample rows have `passenger_count = 0`. To be measured.

## What this means for the pipeline
- Load columns by name, not by position.
- When a new column appears in a file, add it to bronze and log it.
- Anomaly checks run on daily row counts, not monthly totals.

## Open questions
- What does `request_source` mean? Not found in the TLC data dictionary I checked (March 2025 version).
- How common are zero passengers, negative amounts, or dropoff before pickup? (Day 3)
- Is `cbd_congestion_fee` charged on every trip? (Day 3)