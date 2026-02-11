# EU Parliament Transport Discussions Analysis

This project analyzes EU Parliamentary discussions focusing on transport-related topics from 1996 to 2025. It combines web scraping, natural language processing, topic modeling, and sentiment analysis to identify and examine how transport-related topics have been discussed across nearly three decades of EU parliamentary transcripts.

## Project Overview

The analysis identifies 417 transport-related transcripts from a corpus of 23,408 parliamentary discussions, spanning 282 unique calendar dates. The project uses a consensus-based approach combining multiple topic modeling methods (BERTopic, LDA, NMF, Top2Vec) and keyword-based filtering to reliably identify transport-related discussions.

## Requirements

- Python 3.10 or higher (tested on Python 3.12)
- Chrome/Chromium browser (for web scraping)
- ChromeDriver matching your Chrome version
- CUDA-capable GPU (optional, for faster processing)

## Installation

1. Clone this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Download NLTK data (if not automatically downloaded):

```python
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
```

## Project Structure

```
.
├── scraping_no_transl.py              # Main web scraping script (recommended)
├── EU_web_scraping_sections.py        # Alternative scraper with translation (deprecated)
├── data_preparation.ipynb             # Step 1: Data preprocessing and translation
├── topic_modeling.ipynb               # Step 2: Topic modeling (BERTopic, LDA, NMF, Top2Vec)
├── keyword_matching.ipynb             # Step 3: Keyword-based filtering
├── evaluation.ipynb                   # Step 4: Model evaluation and consensus classification
├── sentiment_analysis.ipynb           # Step 5: Sentiment analysis using VADER and transformers
├── exploratory_analysis.ipynb         # Step 6: Final analysis and visualizations
├── data/
│   ├── jsonl/                        # Raw scraped data by parliamentary term
│   ├── csv/                          # Processed datasets
│   ├── keywords_full.json            # Full transport keywords list
│   └── custom_stopwords.json         # Custom parliamentary stopwords
└── requirements.txt                   # Python dependencies
```

## Web Scraping Setup

### Important Notes
- Web scraping requires manual setup and cannot be fully automated due to website restrictions
- The EU Parliament website displays a maximum of 1,000 results per date range
- Scraping must be done in segments for each parliamentary term

### Setup Instructions

1. **Install ChromeDriver**
   - Download ChromeDriver matching your Chrome version: https://chromedriver.chromium.org/
   - For Windows: Place in `C:/chromedriver/chromedriver.exe`
   - For macOS: Place in `/opt/homebrew/bin/chromedriver`
   - For Linux: Place in `/usr/bin/chromedriver`

2. **Start Chrome in Debug Mode**
   
   **Windows:**
   ```bash
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\chrome"
   ```
   
   **macOS:**
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
   ```
   
   **Linux:**
   ```bash
   google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
   ```

3. **Navigate to EU Parliament Transcripts Page**
   - Go to: https://www.europarl.europa.eu/plenary/en/debates-video.html#sidesForm
   - Set filters:
     - **Parliamentary Term**: Select one term (e.g., 2019-2024)
     - **Settings from**: Set start date (work backwards from end of term)
     - **Settings to**: Set end date (ensure <1000 results)
   - Click **Search**

4. **Configure Scraping Script**
   - Open `scraping_no_transl.py`
   - Update the `jsonl_file` variable (line 46) to match the term you're scraping:
     ```python
     jsonl_file = "parliament_transcripts_19_24.jsonl"  # Change as needed
     ```
   - Update the ChromeDriver path (lines 11-15) if necessary

5. **Run the Scraper**
   ```bash
   python scraping_no_transl.py
   ```
   - The script will process each date sequentially
   - Progress is saved to `seen_dates.txt` (checkpoint file)
   - Output is appended to the specified `.jsonl` file
   - You can stop and resume at any time

6. **Repeat for Each Term**
   - Adjust date range filters to get the next batch (<1000 results)
   - Continue until the entire term is scraped
   - Repeat for all seven parliamentary terms (1994-1999, 1999-2004, 2004-2009, 2009-2014, 2014-2019, 2019-2024, 2024-2025)

### Alternative Scraper (Not Recommended)
The `EU_web_scraping_sections.py` script includes real-time translation during scraping. This approach is deprecated as it significantly slows down the process. Translation is now handled separately in the data preparation notebook.

## Workflow: Running the Analysis

The analysis follows a sequential pipeline. Run the notebooks in this order:

### 1. Data Preparation (`data_preparation.ipynb`)
- Loads raw JSONL files from web scraping
- Translates non-English text using `googletrans` and `langdetect`
- Cleans and preprocesses transcripts:
  - Removes empty/irrelevant topics
  - Merges duplicate sections
  - Concatenates paragraphs into single text documents
- Outputs cleaned CSV files by term and a combined dataset

### 2. Topic Modeling (`topic_modeling.ipynb`)
- Applies four topic modeling approaches:
  - **BERTopic**: Transformer-based clustering with UMAP and HDBSCAN
  - **LDA**: Latent Dirichlet Allocation with bag-of-words
  - **NMF**: Non-negative Matrix Factorization with TF-IDF
  - **Top2Vec**: Embedding-based topic discovery
- Identifies transport-related topics for each model
- Assigns topic labels and probabilities to each transcript

### 3. Keyword Matching (`keyword_matching.ipynb`)
- Implements two keyword-based filtering approaches:
  - **Full keyword list**: 423 transport-related terms (exploratory)
  - **Shortened keyword list**: 358 refined terms (used in final classification)
- Matches keywords against transcript text
- Flags documents based on keyword count thresholds

### 4. Evaluation (`evaluation.ipynb`)
- Compares all five approaches (4 topic models + shortened keywords)
- Computes pairwise agreement and Jaccard similarity
- Analyzes consensus distribution across methods
- **Final classification**: Documents identified by ≥3 out of 5 methods
- Outputs final transport-related dataset (417 transcripts)

### 5. Sentiment Analysis (`sentiment_analysis.ipynb`)
- Evaluates three sentiment analysis approaches:
  - VADER (document-level)
  - VADER (sentence-level with length weighting)
  - **Transformer-based** (XLM-RoBERTa - selected for final analysis)
- Applies transformer model to identify positive, neutral, and negative sentiment
- Adds sentiment labels to final dataset

### 6. Exploratory Analysis (`exploratory_analysis.ipynb`)
- Temporal trends: frequency of transport discussions over time
- Sentiment evolution: how tone changes across years and terms
- Keyword frequency: most common transport themes
- Term-specific analysis: top keywords per parliamentary term
- Generates visualizations: line charts, bar charts, heatmaps, area charts

## Key Findings

- **417 transport-related transcripts** identified from 23,408 total discussions (1.78%)
- Transport discussed on **282 unique dates** out of 1,698 total dates
- **Neutral sentiment dominates** (58.0%), with 23.3% positive and 18.7% negative
- Most frequent keywords: road transport, rail transport, transport infrastructure, freight transport
- Peak activity in terms 2004-2009, 2009-2014, and 2014-2019
- Decline in recent terms (potentially due to incomplete translation)

## Data Sources

### EU Parliament Transcripts
- **Source**: https://www.europarl.europa.eu/plenary/en/debates-video.html
- **Coverage**: 1996-2025 (seven parliamentary terms)
- **Format**: Full-text plenary debate transcripts with metadata

### Transport Keywords
Compiled from:
- CH4LLENGE Glossary on Sustainable Urban Mobility (2016)
- Glossary for Transport Statistics, 5th Edition (2019)
- European Commission: Transport in the European Union (2019)
- EU Transport and Legislation websites

## Technical Notes

- **GPU Acceleration**: Topic modeling and sentiment analysis benefit from CUDA-enabled GPUs
- **Memory Requirements**: Processing the full dataset requires ~8GB RAM minimum
- **Processing Time**: 
  - Web scraping: Several hours per term
  - Translation: Very time-consuming (main bottleneck)
  - Topic modeling: 30-60 minutes per model (with GPU)
  - Sentiment analysis: 15-30 minutes (with GPU)

## Limitations

- Translation process was slow and incomplete for the most recent terms
- BERTopic truncates documents to 512 tokens (long transcripts lose information)
- No ground-truth labels available (relies on consensus-based classification)
- Keyword lists may not capture all transport-related nuances

## Future Work

- Complete translation for 2019-2024 and 2024-2025 terms
- Hyperparameter tuning for topic models
- Manual validation of a subset for evaluation
- Analysis of specific policy events or time periods
- Extension to other policy domains beyond transport

## Citation

If you use this dataset or methodology, please cite:

```
Bajrovic, B. (2025). Analysis of EU Parliamentary Discussions About Transport-Related Topics.
Interdisciplinary Project in Data Science, TU Wien.
```

## License

This project is for academic and research purposes. The EU Parliament transcripts are publicly available under EU open data policies.

## Contact

For questions or collaborations, please contact: bakir.13.bajrovic@student.tuwien.ac.at or bajrovicbake@gmail.com
