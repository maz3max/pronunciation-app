import sqlite3
import argparse

# for a given word, get the audio file path from the database

def get_audio_entry(word, db_conn):
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM wordlist WHERE word = ?', (word,))
    result = cursor.fetchall()

    if result:
        # Convert the result to a list for easier access
        return [list(row) for row in result]
    else:
        return []

def main():
    parser = argparse.ArgumentParser(description='Get audio file path for a word from the wordlist database.')
    parser.add_argument('word', type=str, help='The word to look up in the database.')
    args = parser.parse_args()

    db_conn = sqlite3.connect('wordlist.db')
    entry = get_entry(args.word, db_conn)
    if entry:
        for i, row in enumerate(entry):
            print(f"Entry {i + 1}:")
            print(f"Word: {row[0]}")
            print(f"Transcription: {row[1]}")
            print(f"File Name: {row[2]}")
            print(f"Dialect: {row[3]}")
    else:
        print(f"No entry found for '{args.word}'.")

if __name__ == "__main__":
    main()
