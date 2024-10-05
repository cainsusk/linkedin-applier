import chromedriver_autoinstaller
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from logging import info

from common import human_typing, wait_for, random_delay, is_visible
from config import arguments, chrome_options, logging

# Install and set up ChromeDriver
chromedriver_autoinstaller.install()

# Initialize WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)

try:
    info('Navigating to LinkedIn login page.')
    driver.get('https://www.linkedin.com/login')
    random_delay(2, 5)

    info('Entering username and password.')
    username_input = driver.find_element(By.ID, 'username')
    human_typing(username_input, arguments.username)
    
    password_input = driver.find_element(By.ID, 'password')
    human_typing(password_input, arguments.password)
    
    info('Submitting login form.')
    password_input.send_keys(Keys.RETURN)
    random_delay(2, 5)

    # Wait for the page to load after logging in
    wait_for(driver, By.CLASS_NAME, 'global-nav__primary-link', time=5)

    info('Navigating to LinkedIn Jobs page.')
    driver.get('https://www.linkedin.com/jobs')
    random_delay(2, 5)

    info(f'Searching for jobs with the keyword: {arguments.keyword}.')
    search_box = wait_for(driver, By.CSS_SELECTOR, 'input.jobs-search-box__text-input[aria-label="Search by title, skill, or company"]')
    human_typing(search_box, arguments.keyword)
    search_box.send_keys(Keys.RETURN)

    info(f'Searching for jobs in the location: {arguments.location}')
    location_box = wait_for(driver, By.CSS_SELECTOR, 'input.jobs-search-box__text-input[aria-label="City, state, or zip code"]')
    location_box.clear() # clear default location
    human_typing(location_box, arguments.location)
    location_box.send_keys(Keys.RETURN)

    info('Adding "easy-apply" filter')
    easy_apply_filter = driver.find_element(By.XPATH, '//button[@aria-label="Easy Apply filter."]')
    easy_apply_filter.click()

    # Wait for search results to load
    random_delay(5, 8)

    info('Finding job listings on the search results page using data-view-name="job-card".')
    jobs = driver.find_elements(By.XPATH, '//div[@data-view-name="job-card"]')

    # Initialize counters
    total_jobs_to_apply = arguments.amount
    jobs_applied = 0
    current_job_index = 0

    # Loop until we reach the target number of job applications
    while jobs_applied < total_jobs_to_apply and current_job_index < len(jobs):
        try:
            job = jobs[current_job_index]
            data_job_id = job.get_attribute('data-job-id')
            info(f'Found job listing {current_job_index + 1} with job ID: {data_job_id}.')

            info(f'Scrolling to job listing {current_job_index + 1}.')
            driver.execute_script("arguments[0].scrollIntoView();", job)
            random_delay(1, 2)

            info(f'Clicking on job listing {current_job_index + 1}.')
            job.click()
            random_delay(3, 6)

            info(f'Checking for "Easy Apply" button for job ID: {data_job_id}.')
            # Only Easy Apply buttons have the data-job-id attribute
            try:
                easy_apply_button = wait_for(driver, By.XPATH, f'//button[@data-job-id="{data_job_id}"]', time=3)
                easy_apply_button.click()
            except:
                info(f'"Easy Apply" button not found for job listing {current_job_index + 1}. Skipping to next job.')
                current_job_index += 1
                continue  # Skip to the next job if "Easy Apply" button is not found
            random_delay()

            # While there is no "Submit application" button
            while not is_visible(driver, By.XPATH, '//button[@aria-label="Submit application"]'):
                try:
                    info('Moving to next page')
                    next_button = driver.find_element(By.XPATH, '//button[@aria-label="Continue to next step"]')
                    next_button.click()
                except:
                    info('Moving to review page')
                    review_button = driver.find_element(By.XPATH, '//button[@aria-label="Review your application"]')
                    review_button.click()
            random_delay()

            info('Toggle "follow company"')
            follow_company_toggle = driver.find_element(By.XPATH, '//label[@for="follow-company-checkbox"]')
            follow_company_toggle.click()

            info('Submitting application')
            submit_button = driver.find_element(By.XPATH, '//button[@aria-label="Submit application"]')
            submit_button.click()

            random_delay()

            info('Dismissing application confirmation')
            dismiss_button = driver.find_element(By.XPATH, '//div[@role="dialog"]')
            dismiss_button.send_keys(Keys.ESCAPE)

            info(f'Application for job listing {current_job_index + 1} with job ID: {data_job_id} submitted successfully.')
            jobs_applied += 1  # Increment the count of successful applications

        except Exception as e:
            logging.warning(f"An error occurred while processing job listing {current_job_index + 1}: {e}")

        current_job_index += 1

    info('Job application process completed. Closing the browser.')
    random_delay(3, 6)
finally:
    driver.quit()
    info('Browser closed.')
