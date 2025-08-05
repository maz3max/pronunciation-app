# 🔊 Norwegian Pronunciation Lookup

A web application for looking up Norwegian word pronunciations with dialect-specific IPA transcriptions and audio examples.

## Features

- **Real-time word search** with autocomplete suggestions
- **Dialect-specific pronunciations** for five Norwegian dialects:
  - Eastern (Formal/Spoken)
  - Northern (Formal/Spoken)
  - South-Western (Formal/Spoken)
  - Trøndelag (Formal/Spoken)
  - Western (Formal/Spoken)
- **IPA transcriptions** from Språkbanken's nb_uttale dataset
- **G2P fallback** using Phonetisaurus models for unknown words
- **Audio examples** from the nb_samtale speech corpus
- **Responsive design** optimized for desktop and mobile

## Demo

![Norwegian Pronunciation Lookup](https://img.shields.io/badge/Demo-Live-brightgreen)

Try it at: `http://localhost:3000` (after setup)

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Databases**: SQLite (pronunciation data, audio metadata)
- **Speech Processing**: Phonetisaurus G2P models
- **Data Sources**:
  - [nb_uttale](https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-79/) - IPA pronunciation database
  - [nb_samtale](https://huggingface.co/datasets/Sprakbanken/nb_samtale) - Speech audio corpus
  - [g2p-nb](https://github.com/Sprakbanken/g2p-nb) - Grapheme-to-phoneme models

## Quick Start

### Prerequisites

- Python 3.9+
- Git
- 2GB+ free disk space (for models and data)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/maz3max/pronunciation-app.git
   cd pronunciation-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download required data and models:**
   ```bash
   chmod +x download_resources.bash
   ./download_resources.bash
   ```

   This will download:
   - G2P models for all dialects (~500MB)
   - Pronunciation database (~50MB)
   - Audio examples and metadata (~1GB)

4. **Run the application:**
   ```bash
   python server.py
   ```

5. **Open in browser:**
   ```
   http://localhost:3000
   ```

## API Documentation

### Endpoints

#### `GET /api/suggest?q=<query>`
Get autocomplete suggestions for word search.

**Parameters:**
- `q` (string): Search query

**Response:**
```json
["hei", "heia", "heier", "heies"]
```

#### `GET /api/word/<word>?dialect=<dialect>`
Get pronunciation and examples for a word.

**Parameters:**
- `word` (string): Word to look up
- `dialect` (string, optional): Dialect code (default: `e_written`)

**Dialect codes:**
- `e_written` - Eastern (Formal)
- `e_spoken` - Eastern (Spoken)
- `n_written` - Northern (Formal)
- `n_spoken` - Northern (Spoken)
- `sw_written` - South-Western (Formal)
- `sw_spoken` - South-Western (Spoken)
- `t_written` - Trøndelag (Formal)
- `t_spoken` - Trøndelag (Spoken)
- `w_written` - Western (Formal)
- `w_spoken` - Western (Spoken)

**Response:**
```json
{
  "word": "hei",
  "ipa": {
    "e_written": "ˈhɑɪ",
    "g2p": "ˈhɑɪ (generated)"
  },
  "examples": [
    {
      "sentence": "Hei, hvordan har du det?",
      "audio": "data/nb_samtale/data/train/bm/example.wav",
      "dialect": "bm"
    }
  ]
}
```

#### `GET /data/<path:filename>`
Serve audio files and other data assets.

## Development

### Project Structure

```
pronunciation-app/
├── server.py                 # Flask web server
├── static/                   # Frontend assets
│   ├── index.html           # Main HTML page
│   ├── script.js            # Frontend JavaScript
│   └── style.css            # Responsive CSS
├── data/                    # Data and models
│   ├── g2p-nb/             # G2P model files (*.fst)
│   ├── nb_uttale_leksika/  # Pronunciation database
│   └── nb_samtale/         # Audio corpus and metadata
├── requirements.txt         # Python dependencies
├── download_resources.bash  # Data download script
└── README.md               # This file
```

### Local Development

1. **Set up development environment:**
   ```bash
   python -m venv .env
   source .env/bin/activate  # Linux/Mac
   # or
   .env\Scripts\activate     # Windows
   ```

2. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run with debugging:**
   ```bash
   export DEBUG=true
   python server.py
   ```

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions using Docker.

### Quick Production Setup

```bash
# Build and deploy with Docker
./deploy.sh

# Access the application
open http://localhost:8000
```

## Data Sources & Attribution

This application uses several open-source datasets from Språkbanken:

- **[nb_uttale](https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-79/)**: Pronunciation database with IPA transcriptions
- **[nb_samtale](https://huggingface.co/datasets/Sprakbanken/nb_samtale)**: Norwegian speech corpus for audio examples
- **[g2p-nb](https://github.com/Sprakbanken/g2p-nb)**: Grapheme-to-phoneme models for Norwegian dialects
- **[convert_nofabet](https://github.com/Sprakbanken/convert_nofabet)**: Conversion between Nofabet and IPA notation

Special thanks to [Språkbanken](https://www.nb.no/sprakbanken/) for providing these comprehensive language resources.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

For security considerations in production deployments, see [DEPLOYMENT.md](DEPLOYMENT.md#security-considerations).

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page for known problems
2. Review the [DEPLOYMENT.md](DEPLOYMENT.md) for deployment troubleshooting
3. Create a new issue with detailed information about your problem

