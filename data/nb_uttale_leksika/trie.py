import marisa_trie
import sqlite3

def create_trie_from_db(db_path='pronunciation.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all words from the merged table
    cursor.execute('SELECT word FROM merged_ipa')
    words = cursor.fetchall()
    words = [x[0] for x in words]

    # Create a trie from the words
    trie = marisa_trie.Trie(words)

    conn.close()

    return trie

def lookup_in_trie(trie, prefix):
    """Lookup words in the trie that start with the given prefix."""
    return list(trie.keys(prefix))

if __name__ == "__main__":
    # Create the trie from the database
    trie = create_trie_from_db()

    # Example usage: lookup words starting with 'h'
    prefix = 'rev'
    results = lookup_in_trie(trie, prefix)
    print(f"Words starting with '{prefix}': {results}")
