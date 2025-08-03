CSVS = [
    "e_spoken_pronunciation_lexicon.csv",
    "e_written_pronunciation_lexicon.csv",
    "n_spoken_pronunciation_lexicon.csv",
    "n_written_pronunciation_lexicon.csv",
    "sw_spoken_pronunciation_lexicon.csv",
    "sw_written_pronunciation_lexicon.csv",
    "t_spoken_pronunciation_lexicon.csv",
    "t_written_pronunciation_lexicon.csv",
    "w_spoken_pronunciation_lexicon.csv",
    "w_written_pronunciation_lexicon.csv",
]
import sqlite3
import csv

# for each CSV file, create a table with the same name as the file (without extension)
# the table should have the following columns:
# word (position 0 in CSV), ipa (position 6 in CSV)
# given that all input CSVs have the same list of words, we can create the merged table directly 
def create_merged_table_directly():
    conn = sqlite3.connect('pronunciation.db')
    cursor = conn.cursor()

    ipa_columns = [csv_file.split("_pronunciation_lexicon.csv")[0] for csv_file in CSVS]

    # read from all files simultaneously
    files = [open(csv_file, 'r', encoding='utf-8') for csv_file in CSVS]
    readers = [csv.reader(f) for f in files]
    headers = [next(reader) for reader in readers]  # skip headers
    output_table = 'merged_ipa'
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {output_table} (
            word TEXT PRIMARY KEY,
            {', '.join([f'"{col}" TEXT' for col in ipa_columns])}
        )
    ''')
    for row in zip(*readers):
        word = row[0][0]
        ipa_values = [r[6] for r in row]
        cursor.execute(f'''
            INSERT OR REPLACE INTO {output_table} (word, {', '.join(ipa_columns)})
            VALUES (?, {', '.join(['?' for _ in ipa_columns])})
        ''', (word, *ipa_values))
    conn.commit()
    for f in files:
        f.close()

    conn.close()

# print some lines from the merged table
def print_merged_table_sample():
    conn = sqlite3.connect('pronunciation.db')
    cursor = conn.cursor()

    # print header
    cursor.execute('PRAGMA table_info(merged_ipa)')
    headers = cursor.fetchall()
    print("Headers:")
    for header in headers:
        print(header)

    cursor.execute('SELECT * FROM merged_ipa LIMIT 10')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    create_merged_table_directly()
    print_merged_table_sample()