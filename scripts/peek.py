import duckdb

FILE = "data/raw/yellow_tripdata_2026-01.parquet"

print("Kolonlar ve tipler:")
print(duckdb.sql(f"DESCRIBE SELECT * FROM '{FILE}'"))

print("Satir sayisi:")
print(duckdb.sql(f"SELECT count(*) AS rows FROM '{FILE}'"))

print("Ilk 5 satir:")
print(duckdb.sql(f"SELECT * FROM '{FILE}' LIMIT 5"))

print("Aylara gore satir sayisi:")
print(
    duckdb.sql(
        """
        SELECT filename, count(*) AS rows
        FROM read_parquet('data/raw/yellow_tripdata_*.parquet',
                          filename = true, union_by_name = true)
        GROUP BY filename
        ORDER BY filename
        """
    )
)