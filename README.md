# News Scraping, Segmentation, and Valence Analysis Pipeline

This repository contains a modular Python-based pipeline designed to automate the extraction of web news articles, sentence-level linguistic segmentation, and subsequent valence analysis using Large Language Models (LLMs) via the Groq API.

Developed through the lens of Computational Social Sciences, this toolkit provides a structured method for analyzing compleax digital media discourses regarding technology within academic research contexts.

## Institutional Framework & Project Info

**Author:** Agustín Nielsen

**Affiliation:** Equipo Sociedad, Internet y Cultura (ESIC) - Instituto de Investigaciones Gino Germani (IIGG) - Facultad de Ciencias Sociales - Universidad de Buenos Aires (FSOC-UBA).

**Research Framework:** UBACyT "Sociabilidad y Plataformas digitales. Nuevas formas de vinculación, construcción de lazos y tensiones en la cultura digital".

**Director:** Dra. Silvia Lago Martínez.

**Target Corpus Language:** Spanish (ES).

## Pipeline Architecture

### The workflow is divided into three sequential modules:
```bash
[Target URLs] ──► 1. Scraper (trafilatura) ──► articulos_scrapeados.csv
                                                             │
oraciones_para_clasificar.csv ◄── 2. Segmenter (NLTK) ◄──────┘
            │
            ▼
3. Classifier (Groq API) ──► analisis_valencia_final.csv
```

**scraper.py:** Leverages the trafilatura library to extract clean text, titles, dates, and main contents from web news outlets, bypassing noisy HTML structural layouts and advertisements.

**segmentador.py:** Splits raw articles into discrete sentences using NLTK's grammar tokenizers customized for Spanish (punkt). It normalizes whitespaces, removes newline artifacts, and drops short sentences (<10 characters) to filter out interface noise and social media buttons.

**clasificador.py:** Batches sentences into groups of 20 and runs structured inference tasks using llama-3.1-8b-instant via the Groq API. The model assigns a valence class (positiva, negativa, no se identifica valencia) and a confidence score using strict JSON formatting. It contains local filters and resume-on-failure capabilities to manage API interruptions safely.

## Installation & Setup

### 1. Clone the Repository and Install Dependencies
```bash
git clone https://github.com/agustinnielsen/news_scraping_segmenter_valence_analsys.git
cd news_scraping_segmenter_valence_analsys
pip install -r requirements.txt
```


Note on NLTK: The script automatically checks and downloads required components (punkt and punkt_tab). If you run into an SSL: CERTIFICATE_VERIFY_FAILED error (common in macOS or restricted academic proxy networks), update your local Python certificates before launching the process:
``` bash
/Applications/Python\ 3.X/Install\ Certificates.command
```
(Replace 3.X with your active Python environment version).

### 2. Environment Variables Configuration

To guarantee security and avoid exposing API credentials publicly on GitHub, the classifier fetches your token from the system's environment variables.

On Linux / macOS:
```bash
export GROQ_API_KEY="your_api_key_here"
```
On Windows (Command Prompt):
```bash
set GROQ_API_KEY="your_api_key_here"
```
## Data Schema Definitions
### Module 1: Scraper

**Input:** Target web URLs list (mis_urls inside scraper.py).

**Output (articulos_scrapeados.csv):** Semi-colon (;) separated text encoded in utf-8-sig.

#### Schema:
**url:** The source link.

**titulo:** The extracted headline.

**fecha:** Publication date metadata.

**texto_completo:** The stripped, raw body text of the article.

### Module 2: Segmenter

**Input:** articulos_scrapeados.csv

**Output (oraciones_para_clasificar.csv):** Semi-colon (;) separated sentences.

#### Schema:

**url_origen:** Inherited source URL.

**nro_oracion:** Sequential chronological index within the original article (base 0).

**texto_oracion:** The cleaned, isolated sentence text.

### Module 3: LLM Valence Classifier

**Input:** oraciones_para_clasificar.csv

**Output (analisis_valencia_final.csv):** Enriched datasets featuring the final text evaluations.

#### Schema:

**id:** Batch inner index (mapping back to original batch order).

**clase:** Classified sentiment category (positiva / negativa / no se identifica valencia).

**score:** Probability/confidence metric (float value between 0.0 and 1.0).

**url_origen:** Source URL of the article.

**texto_original:** The original sentence evaluated by the model.
