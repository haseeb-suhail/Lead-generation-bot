import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import logging
import undetected_chromedriver as uc
from us_pb_ohio import main
from selenium.webdriver.chrome.options import Options

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_driver():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    driver.get('https://dnsleaktest.com')
    sleep(1)
    driver.maximize_window()
    return driver


# get_driver()
def run_selenium_task(file, output_file):
    sleep(3)
    print('Processing file:', file)
    driver = get_driver()

    try:

        main(file, output_file, driver)

    except:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting the WebDriver: {e}")
        print('Processing complete for file:', file)


if __name__ == "__main__":
    # Enter yout input file no need to give output file name as they will be already genereted
    files = ["input.csv"]

    # Generate a sequence of profile names based on the number of files
    profile_names = [f"102K_1stHalf_Done{i}.csv" for i in range(0, len(files))]
    print(len(profile_names), len(files))
    processes = []

    for file, profile_name in zip(files, profile_names):
        process = multiprocessing.Process(target=run_selenium_task, args=(file, profile_name))
        processes.append(process)
        process.start()
        sleep(25)

    for process in processes:
        process.join()


