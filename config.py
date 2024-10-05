
import argparse
import logging
from selenium import webdriver


# Setup command line arguments
parser = argparse.ArgumentParser(description='Automate LinkedIn Job Applications.')
parser.add_argument('--username', type=str, required=True, help='LinkedIn username (email).')
parser.add_argument('--password', type=str, required=True, help='LinkedIn password.')
parser.add_argument('--keyword', type=str, required=True, help='Job title to search for (e.g., "Software Developer").')
parser.add_argument('--location', type=str, required=True, help='Location to filter job search (e.g., "Ottawa, ON").')
parser.add_argument('--amount', type=int, default=3, help='Number of jobs to apply to.')
# Parse the arguments
arguments = parser.parse_args()

# Setup chrome-driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('linkedin-applier.log')]
)

