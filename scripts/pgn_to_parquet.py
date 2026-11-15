import io
import sys
from collections import Counter
from pathlib import Path

import chess.pgn
import pyarrow as pa
import pyarrow.parquet as pq
import zstandard

COLUMNS = [
    "Event", "Site", "White", "Black", "Result", "UTCDate", "UTCTime",
    "WhiteElo", "BlackElo", "WhiteRatingDiff", "BlackRatingDiff",
    "ECO", "Opening", "TimeControl", "Termination",
]
CHUNK = 200_000

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
schema = pa.schema([(c, pa.string()) for c in COLUMNS])


def flush(writer, rows):
    columns = {c: [r.get(c) for r in rows] for c in COLUMNS}
    writer.write_table(pa.table(columns, schema=schema))


seen_keys = Counter()
total = 0
rows = []

with open(src, "rb") as fh, pq.ParquetWriter(dst, schema) as writer:
    reader = zstandard.ZstdDecompressor().stream_reader(fh)
    text = io.TextIOWrapper(reader, encoding="utf-8", errors="replace")
    while True:
        headers = chess.pgn.read_headers(text)
        if headers is None:
            break
        seen_keys.update(headers.keys())
        rows.append(dict(headers))
        total += 1
        if len(rows) >= CHUNK:
            flush(writer, rows)
            rows = []
            print(f"{total:,} games")
    if rows:
        flush(writer, rows)

print(f"done: {total:,} games")
print("Basliklar:", dict(seen_keys))