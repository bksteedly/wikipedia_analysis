# Wikipedia Algorithm Analysis

A study of algorithm coverage on Wikipedia, comparing our dataset collected from textbooks to the algorithms present on Wikipedia. We use page views as a measure of importance in an effort to validate the textbooks dataset.

## Repository Structure

```
wikipedia_analysis/
├── data/                          # CSVs used and produced 
                                   # by the pipeline

├── figures/                       # Output figure options
                                   # for the paper

├── authors_figures/               # Output figures for the
                                   # authors analysis

├── scrape_data.py                 # Scrapes Wikipedia 
                                   # search results to CSV

├── figures.ipynb                  # Code to generate 
                                   # figure options for the 
                                   # paper

├── authors_figures.ipynb          # Code to generate
                                   # authors figures
└── README.md
```

## Dependencies

- `pandas`, `numpy`, `requests`, `beautifulsoup4`, `scikit-learn`, `statsmodels`, `matplotlib`, `habanero`, `crossref-commons`, `pdf2doi`, `tqdm`
