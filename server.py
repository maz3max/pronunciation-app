# webserver

# serve /data and /static
# special functions for api calls

# queries to "/api/suggest" return a list of words that match the input
# queries to "/api/word/<word>" returns { word, ipa, examples }
# where ipa is a dictionary with keys as dialects and values as their IPA transcriptions
# where examples is a list of { transcription, file_name, dialect }

from flask import Flask, jsonify, request, send_from_directory, g
from data.nb_uttale_leksika.autocomplete_lookup import get_suggestions
from data.nb_uttale_leksika.ipa_lookup import get_ipa
from data.nb_samtale.get_audio import get_audio_entry
from convert_pa import nofabet_to_ipa
import phonetisaurus_g2p_py
import sqlite3
import threading

SAMTALE_DB = 'data/nb_samtale/wordlist.db'
UTTALE_DB = 'data/nb_uttale_leksika/pronunciation.db'

g2p_model = phonetisaurus_g2p_py.PhonetisaurusModel('data/g2p-nb/nb_e_written.fst')

app = Flask(__name__, static_folder='static', static_url_path='/')

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
    suggestions = get_suggestions(query, get_uttale_db())
    return jsonify(suggestions)

@app.route('/api/word/<word>', methods=['GET'])
def word(word):
    ipa = get_ipa(word, get_uttale_db())
    if not ipa:
        word_nofabet = g2p_model.phonemize_word(word).phonemes
        word_ipa = nofabet_to_ipa(word_nofabet)
        ipa = { 'g2p' : word_ipa }

    samtale_entries = get_audio_entry(word, get_samtale_db())
    
    examples = []
    for word, transcription, file_name, dialect in samtale_entries:
        examples.append({
            'sentence': transcription,
            'audio': "data/nb_samtale/" + file_name,
            'dialect': dialect
        })
    return jsonify({ 'word': word, 'ipa': ipa, 'examples': examples })

@app.route('/data/<path:filename>', methods=['GET'])

def data(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)