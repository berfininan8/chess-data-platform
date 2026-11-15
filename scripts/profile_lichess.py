import duckdb

SRC = "data/raw/lichess_2015-06.parquet"


def show(title, sql):
    print(f"\n== {title}")
    print(duckdb.sql(sql))


show(
    "Toplam ve tarih araligi",
    f"""
    SELECT count(*) AS games, min(UTCDate) AS first_day, max(UTCDate) AS last_day
    FROM '{SRC}'
    """,
)

show(
    "Aya gore oyun sayisi (UTCDate'den)",
    f"""
    SELECT substr(UTCDate, 1, 7) AS ym, count(*) AS games
    FROM '{SRC}'
    GROUP BY 1
    ORDER BY 1
    """,
)

show(
    "Tekrar eden oyun (ayni Site)",
    f"""
    SELECT count(*) - count(DISTINCT Site) AS duplicate_rows
    FROM '{SRC}'
    """,
)

show(
    "Bitis nedeni ve eksik puan farki",
    f"""
    SELECT Termination, count(*) AS games,
           count_if(WhiteRatingDiff IS NULL) AS no_rating_diff
    FROM '{SRC}'
    GROUP BY 1
    ORDER BY games DESC
    """,
)

show(
    "Beyaz kazandi ama beyazin puan farki negatif",
    f"""
    SELECT count(*) AS games
    FROM '{SRC}'
    WHERE Result = '1-0' AND TRY_CAST(WhiteRatingDiff AS INTEGER) < 0
    """,
)

show(
    "Bilinmeyen degerler",
    f"""
    SELECT
        count_if(Opening = '?') AS opening_unknown,
        count_if(TimeControl IN ('-', '?')) AS time_control_unknown,
        count_if(TRY_CAST(WhiteElo AS INTEGER) IS NULL) AS white_elo_not_number,
        count_if(TRY_CAST(BlackElo AS INTEGER) IS NULL) AS black_elo_not_number
    FROM '{SRC}'
    """,
)