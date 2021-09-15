import rewardsbot.util as util

from selenium.webdriver.remote.webdriver import WebDriver


class DailySearch:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def fill_input(self):
        util.wait_random()
        input_field = self.driver.find_element_by_css_selector('#sb_form_q')
        input_field.clear()
        input_field.send_keys(util.random_letter())

        util.wait_random()
        search = self.driver.find_element_by_css_selector('#search_icon')
        search.click()

    def search(self):
        util.wait_random()

        for _ in range(30):
            util.wait_random()
            input_field = self.driver.find_element_by_css_selector('#sb_form_q')
            input_field.send_keys(util.random_letter())
            search = self.driver.find_element_by_css_selector('#sb_form_go')
            search.click()
