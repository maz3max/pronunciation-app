import argparse
import sqlite3

def get_ipa(word, db_conn):
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM merged_ipa WHERE word = ?', (word,))
    result = cursor.fetchone()

    if result:
        # Convert the result to a dictionary for easier access
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, result))
    else:
        return None
    
def main():
    parser = argparse.ArgumentParser(description='Lookup IPA for a word in the pronunciation database.')
    parser.add_argument('word', type=str, help='The word to look up in the database.')
    args = parser.parse_args()

    db_conn = sqlite3.connect('pronunciation.db')
    result = get_ipa(args.word, db_conn)

    if result:
        print(f"Word: {result['word']}")
        for column in result:
            if column != 'word':
                print(f"{column}: {result[column]}")
    else:
        print(f"No IPA found for the word: {args.word}")

if __name__ == "__main__":
    main()