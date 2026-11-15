import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://d37ci6vzurychx.cloudfront.net"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]

def download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"skip  {dest.name} (already exists)")
        return
    tmp = dest.with_name(dest.name + ".part")
    print(f"get   {dest.name}")
    request = urllib.request.Request(url, headers={"User-Agent": "taxi-platform/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=60) as resp, open(tmp, "wb") as out:
            while chunk := resp.read(1024 * 1024):
                out.write(chunk)
    except urllib.error.URLError as e:
        tmp.unlink(missing_ok=True)
        print(f"FAIL  {dest.name}: {e}")
        return
    tmp.replace(dest)
    print(f"done  {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    download(f"{BASE}/misc/taxi_zone_lookup.csv", RAW_DIR / "taxi_zone_lookup.csv")
    for month in MONTHS:
        name = f"yellow_tripdata_{month}.parquet"
        download(f"{BASE}/trip-data/{name}", RAW_DIR / name)


if __name__ == "__main__":
    main()