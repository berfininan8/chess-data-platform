"""Download Lichess monthly standard rated game files into data/raw/."""
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://database.lichess.org/standard"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
MONTHS = ["2015-01", "2015-02", "2015-03", "2015-04", "2015-05", "2015-06"]
CHUNK = 1024 * 1024


def download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"skip  {dest.name} (already exists)")
        return
    tmp = dest.with_name(dest.name + ".part")
    print(f"get   {dest.name}")
    request = urllib.request.Request(url, headers={"User-Agent": "chess-platform/0.1"})
    chunks = 0
    try:
        with urllib.request.urlopen(request, timeout=60) as resp, open(tmp, "wb") as out:
            while chunk := resp.read(CHUNK):
                out.write(chunk)
                chunks += 1
                if chunks % 100 == 0:
                    print(f"      {chunks} MB")
    except urllib.error.URLError as e:
        tmp.unlink(missing_ok=True)
        print(f"FAIL  {dest.name}: {e}")
        return
    tmp.replace(dest)
    print(f"done  {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for month in MONTHS:
        name = f"lichess_db_standard_rated_{month}.pgn.zst"
        download(f"{BASE}/{name}", RAW_DIR / name)


if __name__ == "__main__":
    main()