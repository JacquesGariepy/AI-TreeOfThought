import yaml
from datetime import datetime
from urllib.parse import quote

from src.fetcher import Fetcher
from src.saver import Saver

with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

url = config['fetcher']['url']

# Get current date and time
now = datetime.now()

# Format date and time
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Make url safe for file name
safe_url = quote(url, safe='')

# Add url and date time to file name
output_file = f"{config['saver']['output_path']}/{safe_url}_{date_time}.txt"

#output_file = config['saver']['output_path']

text = Fetcher.fetch_text_from_url(url)
Saver.save_text_to_file(text, output_file)