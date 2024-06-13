# Arxiv Text Fetcher

## Overview

This project fetches text from a specified section of an HTML page at a given URL and saves it to a local file.

## Project Structure

```
arxiv_text_fetcher/
│
├── data/
│   └── output.txt
│
├── src/
│   ├── __init__.py
│   ├── fetcher.py
│   └── saver.py
│
├── tests/
│   ├── __init__.py
│   ├── test_fetcher.py
│   └── test_saver.py
│
├── scripts/
│   └── run_fetch_and_save.py
│
├── docs/
│   └── README.md
│
├── config/
│   └── config.yaml
│
├── requirements.txt
├── dev-requirements.txt
├── .pre-commit-config.yaml
└── venv/
```

## Installation

```bash
git clone <repository-url>
cd arxiv_text_fetcher
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

## Configuration

Create a `config.yaml` file in the `config` directory with the following content:

```yaml
# config/config.yaml

fetcher:
  url: "https://arxiv.org/html/2403.08299v1#S2"

saver:
  output_path: "data/output.txt"
```

## Usage

To fetch text from a URL and save it to a file, use the following script:

```python
# scripts/run_fetch_and_save.py

import yaml
from src.fetcher import Fetcher
from src.saver import Saver

with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

url = config['fetcher']['url']
output_file = config['saver']['output_path']

text = Fetcher.fetch_text_from_url(url)
Saver.save_text_to_file(text, output_file)
```

Run the script:

```bash
python scripts/run_fetch_and_save.py
```