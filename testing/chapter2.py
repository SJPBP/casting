import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class PythonOrgSearch(unittest.TestCase):

    # Runned before anything to set up for test
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.python.org")

    # Test method starts with test
    # This test check if Python is in Title
    def test_python_in_title(self):
        driver = self.driver

        # Check if page title have Python
        self.assertIn("Python", driver.title)

    # This test check if message is in searched page
    def test_search_in_python_org(self):
        driver = self.driver

        searchBar = driver.find_element(By.ID, "id-search-field")
        searchBar.clear()
        searchBar.send_keys("pycon")
        searchBar.send_keys(Keys.RETURN)

        # Check if message is in page source
        self.assertNotIn("No results found.", driver.page_source)

    # This test get all the cookies from page
    def test_get_cookie(self):
        driver = self.driver
        print(driver.get_cookies())

    # Runned after the test to do clean up
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
