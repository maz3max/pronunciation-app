import json
from collections import defaultdict
import sqlite3

metadata_files = [
    "data/test_metadata.jsonl",
    "data/train_metadata.jsonl",
    "data/validation_metadata.jsonl"
]

# output format
# list of tuples (word, verbatim_transcription, sound_file)

def make_wordlist(metadata_files):
    wordlist = []
    for metadata_file in metadata_files:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                text = data.get('verbatim', '')
                text_filtered = text.replace(',', ' ').replace('.', ' ').replace('?', ' ').replace('!', ' ')
                words = [x.lower() for x in text_filtered.split()]
                for word in words:
                    wordlist.append((word, text, data.get('file_name', ''), data.get('dialect', '')))
    return wordlist

def save_wordlist_to_db(wordlist):
    conn = sqlite3.connect('wordlist.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wordlist (
            word TEXT,
            transcription TEXT,
            file_name TEXT,
            dialect TEXT
        )
    ''')
    
    cursor.executemany('''
        INSERT INTO wordlist (word, transcription, file_name, dialect)
        VALUES (?, ?, ?, ?)
    ''', wordlist)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    wordlist = make_wordlist(metadata_files)

    dict_wordlist = defaultdict(list)

    for word, transcription, file_name, dialect in wordlist:
        dict_wordlist[word].append((transcription, file_name, dialect))

    with open('wordlist.json', 'w', encoding='utf-8') as f:
        json.dump(dict_wordlist, f, ensure_ascii=False, indent=4)
    print("Wordlist created and saved to 'wordlist.json'.")

    save_wordlist_to_db(wordlist)
    print("Wordlist saved to 'wordlist.db'.")