import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver():
    """
    Pytest fixture to set up and tear down the Selenium WebDriver.
    Configures the WebDriver to ignore SSL certificate errors.
    """
    # Set up Chrome options to handle SSL certificate issues
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--start-maximized")  # Maximize the browser

    # Set up the WebDriver service
    service = Service('../driver/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver  # Provide the WebDriver to the test
    driver.quit()  # Ensure the browser is closed after the test


def test_check_login_ui(driver):
    url = "https://amaderit.net/demo/hr/login"
    driver.get(url)

    # Verify the logo redirects to the homepage
    logo = driver.find_element(By.XPATH, "//img[@alt='AmaderHR']")
    logo.click()
    WebDriverWait(driver, 2).until(
        lambda driver: driver.current_url != url
    )


def test_login_invalid_email(driver):

    # Open the target website
    url = "https://amaderit.net/demo/hr/login"
    driver.get(url)
    print("Navigated to the login page.")
    print("Page title before login:", driver.title)

    try:
        # Locate and interact with the username and password fields
        username_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.NAME, "password")
        print("Username and password fields located.")

        # Enter the login credentials
        username_field.send_keys("961876385")
        password_field.send_keys("12345678")

        # Locate and click the login button
        login_button = driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']")
        login_button.click()
        # Alternatively, if you want to check the URL after login
        WebDriverWait(driver, 2).until(
            lambda driver: driver.current_url != url
        )
        print("Page URL after login:", driver.current_url)
    except NoSuchElementException:
        raise AssertionError("Test failed: Username or password field is not available.")





def test_login_invalid_password(driver):
    # Open the target website
    url = "https://amaderit.net/demo/hr/login"
    driver.get(url)
    print("Navigated to the login page.")
    print("Page title before login:", driver.title)

    try:
        # Locate and interact with the username and password fields
        username_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.NAME, "password")
        print("Username and password fields located.")

        # Enter the login credentials
        username_field.send_keys("12345678")
        password_field.send_keys("78555678")

        # Locate and click the login button
        login_button = driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']")
        login_button.click()
        # Alternatively, if you want to check the URL after login
        WebDriverWait(driver, 2).until(
            lambda driver: driver.current_url != url
        )
        print("Page URL after login:", driver.current_url)
    except NoSuchElementException:
        raise AssertionError("Test failed: Username or password field is not available.")


def test_login(driver):
    """
    Test case to validate the login functionality.
    """
    print("Starting the test.")

    # Open the target website
    url = "https://amaderit.net/demo/hr/login"
    driver.get(url)
    print("Navigated to the login page.")
    print("Page title before login:", driver.title)

    try:
        # Locate and interact with the username and password fields
        username_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.NAME, "password")
        print("Username and password fields located.")
    except NoSuchElementException:
        raise AssertionError("Test failed: Username or password field is not available.")

    # Enter the login credentials
    username_field.send_keys("12345678")
    password_field.send_keys("12345678")

    # Locate and click the login button
    login_button = driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']")
    login_button.click()

    try:
        # Check for a login error message
        error_message = driver.find_element(By.XPATH, "//div[@class='message alert alert-danger']")
        if error_message.text == "Invalid UserID or Password":
            raise AssertionError("Test failed: Invalid UserID or Password.")
    except NoSuchElementException:
        # If no error, wait for the page to load and validate the post-login state
        time.sleep(1)  # Adjust time if necessary based on your application
        print("Login attempt complete. Checking page details.")
        print("Page title after login:", driver.title)
        print("Current URL after login:", driver.current_url)


