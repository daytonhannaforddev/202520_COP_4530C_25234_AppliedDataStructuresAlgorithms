#
# Load plane (JAERO-format) CSV into a Pandas datafrane for analysis
#
# Usage: python3 main.py <input_csv_file>
# example: python3 main.py test.csv
#
import sys
import pandas as pd

def main():
    fname = sys.argv[1]

    df = pd.read_csv(
        fname,
        on_bad_lines="warn",
        names=[
            "time_stamp", "date_stamp", "utc", "hex_code",
            "ground_air", "station", "unkn1", "registration",
            "unkn2", "unkn3", "manf", "model", "unkn4",
            "main_carrier", "carrier2", "carrier3", "msg_text",
            "useless1", "useless2", "useless3"
        ]
    )

    # A.
    df['datetime'] = pd.to_datetime(
        df['date_stamp'] + ' ' + df['time_stamp'],
        format='%d-%m-%y %H:%M:%S',
        dayfirst=True,
        errors='coerce'
    )
    df = df.dropna(subset=['datetime'])
    df['epoch'] = df['datetime'].astype('int64') // 10**9

    # B.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"B: Number of row: {len(df)}")
    # C.
    print(f"C: Number of columns: {len(df.columns)}")

    # D.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("D: *****First 20 rows:*****")
    print(df.head(20))

    # E.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("E: *****Last 20 rows:*****")
    print(df.tail(20))


    # F.
    snippet = df.head(100).to_html(index=False)
    out_html = "snippet.html"
    with open(out_html, 'w') as f:
        f.write(snippet)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"F: HTML snippet (first 100 rows) written to {out_html}")

    # G.
    for col in ('main_carrier', 'carrier2'):
        df[col] = df[col].fillna('').str.split(';', n=1).str[0].str.strip()

    df['carrier_full'] = df['main_carrier']
    mask = df['carrier2'] != ''
    df.loc[mask, 'carrier_full'] = df.loc[mask, 'main_carrier'] + ' ' + df.loc[mask, 'carrier2']
    df['carrier_full'] = df['carrier_full'].replace('', pd.NA)

    counts = df['carrier_full'].dropna().value_counts()
    counts = counts.drop(labels=['Airlines'], errors='ignore') # was getting 'Airlines' as the answer, when that's not an airline.
    most = counts.idxmax()
    least = counts[counts > 0].idxmin()

    print("\nG: Carrier by popularity:")
    print(f"Most popular:  {most} ({counts[most]})")
    print(f"Least popular: {least} ({counts[least]})")

    # H.
    nouns = set(w.strip().lower() for w in open('nounlist.txt'))
    words_series = df['msg_text'].fillna('').str.lower().str.findall(r'\b\w+\b')
    exploded    = words_series.explode()
    noun_counts = exploded[exploded.isin(nouns)].value_counts()

    most = noun_counts.idxmax()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"H: Most common noun:  {most} ({noun_counts[most]})")

    min_noun = noun_counts[noun_counts>0].min()
    least  = noun_counts[noun_counts == min_noun].index[0]
    print(f"H: Least common noun: {least} ({min_noun})")

    # J.
    top3 = df['hex_code'].value_counts().head(3)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\nJ: Top 3 hex codes and models:")
    for code, cnt in top3.items():
        models = df.loc[df['hex_code'] == code, 'model'] \
            .dropna() \
            .unique() \
            .tolist()
        print(f"{code} ({cnt} times mentioned): {', '.join(models) or 'unknown'}")


if __name__ == "__main__":
    main()
