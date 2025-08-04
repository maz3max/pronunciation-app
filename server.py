# webserver

# serve /data and /static
# special functions for api calls

# queries to "/api/suggest" return a list of words that match the input
# queries to "/api/word/<word>" returns { word, ipa, examples }
# where ipa is a dictionary with keys as dialects and values as their IPA transcriptions
# where examples is a list of { transcription, file_name, dialect }

from flask import Flask, jsonify, request, send_from_directory, abort
from data.nb_uttale_leksika.autocomplete_lookup import get_suggestions
from data.nb_uttale_leksika.ipa_lookup import get_ipa
from data.nb_samtale.get_audio import get_audio_entry
from convert_pa import nofabet_to_ipa
import phonetisaurus_g2p_py
import sqlite3
import threading
import re
from urllib.parse import unquote

SAMTALE_DB = 'data/nb_samtale/wordlist.db'
UTTALE_DB = 'data/nb_uttale_leksika/pronunciation.db'

g2p_model = phonetisaurus_g2p_py.PhonetisaurusModel('data/g2p-nb/nb_e_written.fst')

app = Flask(__name__, static_folder='static', static_url_path='/')

# Input sanitization functions
def sanitize_word(query):
    """Sanitize search query input"""
    if not query:
        return ''
    
    # Remove potentially dangerous characters, keep letters, numbers, and common punctuation
    sanitized = re.sub(r'[^\w\-\'æøåÆØÅ]', '', query)
    
    # Limit length to prevent DoS
    return sanitized[:100].strip()

def sanitize_filename(filename):
    """Lightweight filename sanitization focused on URL decoding and basic validation"""
    if not filename:
        return ''
    
    # URL decode the filename (this is the main security issue)
    filename = unquote(filename)
    
    # Remove null bytes which can cause issues
    filename = filename.replace('\0', '')
    
    # Limit length to prevent potential DoS
    return filename[:255].strip()

# Thread-local storage for database connections
_thread_locals = threading.local()

def get_uttale_db():
    """Get or create a thread-local connection to the uttale database"""
    if not hasattr(_thread_locals, 'uttale_conn'):
        _thread_locals.uttale_conn = sqlite3.connect(UTTALE_DB, check_same_thread=False)
    return _thread_locals.uttale_conn

def get_samtale_db():
    """Get or create a thread-local connection to the samtale database"""
    if not hasattr(_thread_locals, 'samtale_conn'):
        _thread_locals.samtale_conn = sqlite3.connect(SAMTALE_DB, check_same_thread=False)
    return _thread_locals.samtale_conn

@app.teardown_appcontext
def close_db_connections(error):
    """Close database connections when the request context is torn down"""
    if hasattr(_thread_locals, 'uttale_conn'):
        _thread_locals.uttale_conn.close()
        delattr(_thread_locals, 'uttale_conn')
    if hasattr(_thread_locals, 'samtale_conn'):
        _thread_locals.samtale_conn.close()
        delattr(_thread_locals, 'samtale_conn')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/suggest', methods=['GET'])
def suggest():
    query = request.args.get('q', '')
    sanitized_query = sanitize_word(query)

    # Return empty list if query is empty after sanitization
    if not sanitized_query:
        return jsonify([])
    
    suggestions = get_suggestions(sanitized_query, get_uttale_db())
    return jsonify(suggestions)

@app.route('/api/word/<word>', methods=['GET'])
def word(word):
    sanitized_word = sanitize_word(word)
    
    # Return 400 if word is empty after sanitization
    if not sanitized_word:
        abort(400, description="Invalid word parameter")
    
    ipa = get_ipa(sanitized_word, get_uttale_db())
    if not ipa:
        try:
            word_nofabet = g2p_model.phonemize_word(sanitized_word).phonemes
            word_ipa = nofabet_to_ipa(word_nofabet)
            ipa = { 'g2p' : word_ipa }
        except Exception as e:
            # Handle potential errors from g2p model
            ipa = { 'error': 'Could not generate pronunciation' }

    samtale_entries = get_audio_entry(sanitized_word, get_samtale_db())
    
    examples = []
    for entry_word, transcription, file_name, dialect in samtale_entries:
        # Sanitize the file_name from database as well
        safe_filename = sanitize_filename(file_name)
        if safe_filename:  # Only add if filename is valid after sanitization
            examples.append({
                'sentence': transcription,
                'audio': "data/nb_samtale/" + safe_filename,
                'dialect': dialect
            })
    return jsonify({ 'word': sanitized_word, 'ipa': ipa, 'examples': examples })

@app.route('/data/<path:filename>', methods=['GET'])
def data(filename):
    sanitized_filename = sanitize_filename(filename)
    
    # Return 400 if filename is empty after sanitization
    if not sanitized_filename:
        abort(400, description="Invalid filename")
    
    # Let Flask's send_from_directory handle the rest of the security
    # It will automatically prevent directory traversal and validate the path
    try:
        return send_from_directory('data', sanitized_filename)
    except FileNotFoundError:
        abort(404, description="File not found")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
