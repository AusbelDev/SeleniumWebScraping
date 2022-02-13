from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException 
import pandas as pd

from concurrent.futures import ProcessPoolExecutor
import concurrent.futures

driver_option = webdriver.FirefoxOptions()
driver_option.add_argument("-- incognito")

urlarray = ["https://github.com/collections/machine-learning"]

def create_webdriver():
    return webdriver.Firefox()

def scrape_url(url):
    new_browser = create_webdriver()
    new_browser.get(url)
 
 # Extract required data here
 # ...
    projects = new_browser.find_elements_by_xpath("//h1[@class='h3 lh-condensed']")

    project_list = {}
    for proj in projects:
        proj_name = proj.text # Project name
        proj_url = proj.find_elements_by_xpath("a")[0].get_attribute('href') # Project URL
        project_list[proj_name] = proj_url

    new_browser.quit()
 
    return project_list

with ProcessPoolExecutor(max_workers=4) as executor:
    future_results = {executor.submit(scrape_url, url) for url in urlarray}

results = []
for future in concurrent.futures.as_completed(future_results):
    results.append(future.result())



project_df = pd.DataFrame.from_dict(results, orient = 'index')

project_df['project_name'] = project_df.index
project_df.columns = ['project_url', 'project_name']
project_df = project_df.reset_index(drop=True)

project_df.to_csv('project_list.csv')