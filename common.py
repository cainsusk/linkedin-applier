
import random
import time
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for(web_driver, search_method, criteria, time=10):
    return WebDriverWait(web_driver, time).until(EC.presence_of_element_located((search_method, criteria)))

def is_visible(web_driver, search_method, criteria) -> bool:
    try:
        wait_for(web_driver, search_method, criteria)
        return True
    except:
        return False

        


# Function to add random delay
def random_delay(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

# Function to simulate human-like typing
def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Random delay between keystrokes


