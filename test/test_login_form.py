from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestLoginForm(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/login')

    def tearDown(self):
        self.driver.quit()

    def test_loading_spinner_visible_on_submit(self):
        driver = self.driver
        username_input = driver.find_element(By.ID, 'username')
        password_input = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'login-button')

        username_input.send_keys('user')
        password_input.send_keys('pass')

        login_button.click()
        
        # Wait for the spinner to be visible once the login button is clicked
        spinner = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'loading-spinner'))
        )
        
        self.assertTrue(spinner.is_displayed(), "Spinner should be visible after login submission")

if __name__ == '__main__':
    unittest.main()