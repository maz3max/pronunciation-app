import argparse
import sqlite3

def get_suggestions(word, db_conn):
    cursor = db_conn.cursor()

    # Case-insensitive search, ordered by length to prioritize closer matches
    cursor.execute('''
        SELECT word FROM merged_ipa 
        WHERE LOWER(word) LIKE LOWER(?) 
        ORDER BY LENGTH(word), LOWER(word)
        LIMIT 10
    ''', (word + '%',))
    results = cursor.fetchall()
    
    return [result[0] for result in results]

def main():
    parser = argparse.ArgumentParser(description='Autocomplete words from the pronunciation database.')
    parser.add_argument('word', type=str, help='The word to autocomplete.')
    args = parser.parse_args()

    db_conn = sqlite3.connect('pronunciation.db')
    results = get_suggestions(args.word, db_conn)

    if results:
        print("Autocomplete suggestions:")
        for word in results:
            print(word)
    else:
        print("No suggestions found.")

if __name__ == "__main__":
    main()