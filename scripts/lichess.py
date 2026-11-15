import io
import sys
from collections import Counter

import chess.pgn
import zstandard

path = sys.argv[1]
limit = 5000

results = Counter()
termination = Counter()
missing = Counter()
samples = []

with open(path, "rb") as fh:
    reader = zstandard.ZstdDecompressor().stream_reader(fh)
    text = io.TextIOWrapper(reader, encoding="utf-8")
    for _ in range(limit):
        headers = chess.pgn.read_headers(text)
        if headers is None:
            break
        results[headers.get("Result", "MISSING")] += 1
        termination[headers.get("Termination", "MISSING")] += 1
        for key in ("WhiteElo", "BlackElo", "Opening", "TimeControl"):
            if headers.get(key, "?") in ("?", "", "-"):
                missing[key] += 1
        if len(samples) < 3:
            samples.append(dict(headers))

print("Ornek basliklar:")
for s in samples:
    print(s)
print("Sonuclar:", dict(results))
print("Bitis nedenleri:", dict(termination))
print("Eksik/bilinmeyen alanlar:", dict(missing))