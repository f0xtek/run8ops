import urllib.request
import urllib.error
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys

URL = "https://www.thedepotserver.com/reference/destinationtags/view/socal"
OUTPUT_FILE = "run8ops.xlsx"
SHEET_NAME = "socal_destination_tags"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching {url}: {e.code} {e.reason}", file=sys.stderr)
        raise
    except urllib.error.URLError as e:
        print(f"Failed to reach {url}: {e.reason}", file=sys.stderr)
        raise


def parse_table(html: bytes, base_url: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if table is None:
        raise ValueError("No table found in HTML")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if not tds:
            continue
        cells = []
        for i, td in enumerate(tds):
            if i == 0:
                continue  # Drop row ID column
            elif i == 1:
                # Image column: extract the link URL rather than text
                a = td.find("a", href=True)
                href = str(a["href"]) if a else ""
                cells.append(urllib.parse.urljoin(base_url, href) if href else "")
            else:
                cells.append(td.get_text(strip=True))
        rows.append(cells)

    if not rows:
        raise ValueError("Table found but contains no data rows")

    num_cols = len(rows[0])
    if headers:
        # Pad headers on the left if the first column(s) have no <th>
        while len(headers) < num_cols:
            headers.insert(0, "")
        columns = headers[:num_cols]
        columns[0] = "Image URL"
    else:
        columns = None

    return pd.DataFrame(rows, columns=columns)


def fetch_table(url: str) -> pd.DataFrame:
    base_url = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(url))
    html = fetch_html(url)
    return parse_table(html, base_url)


def save_sheet(df: pd.DataFrame, output_file: str, sheet_name: str) -> None:
    if os.path.exists(output_file):
        with pd.ExcelWriter(
            output_file, engine="openpyxl", mode="a", if_sheet_exists="replace"
        ) as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)


if __name__ == "__main__":
    df = fetch_table(URL)
    save_sheet(df, OUTPUT_FILE, SHEET_NAME)
    print(f"Saved {len(df)} rows to '{OUTPUT_FILE}' (sheet: '{SHEET_NAME}')")
