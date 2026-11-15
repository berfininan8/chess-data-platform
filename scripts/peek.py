from pathlib import Path

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

schemas = {}
for f in sorted(Path("data/raw").glob("yellow_tripdata_*.parquet")):
    rows = duckdb.sql(f"DESCRIBE SELECT * FROM '{f.as_posix()}'").fetchall()
    schemas[f.name] = [(r[0], r[1]) for r in rows]

base = schemas["yellow_tripdata_2026-01.parquet"]
print("Sema karsilastirmasi (Ocak'a gore):")
for name, cols in schemas.items():
    print(name, "ayni" if cols == base else "FARKLI")


jun_name = "yellow_tripdata_2026-06.parquet"
jan = dict(base)
jun = dict(schemas[jun_name])

print("Haziran farklari:")
for col in sorted(set(jan) | set(jun)):
    if jan.get(col) != jun.get(col):
        print(f"  {col}: Ocak={jan.get(col)}  Haziran={jun.get(col)}")

print("Kolon sirasi ayni mi:", [c for c, _ in base] == [c for c, _ in schemas[jun_name]])

JUN = "data/raw/yellow_tripdata_2026-06.parquet"

print("request_source degerleri (Haziran):")
print(
    duckdb.sql(
        f"""
        SELECT request_source, count(*) AS n
        FROM '{JUN}'
        GROUP BY 1
        ORDER BY n DESC
        LIMIT 10
        """
    )
)
print("Haziran kolon sirasi:", [c for c, _ in schemas[jun_name]])