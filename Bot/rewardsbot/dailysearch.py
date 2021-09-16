import rewardsbot.util as util

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DailySearch:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.complete = False
        self.count = 30

    def open_drawer(self):
        util.wait(3)

        drawer = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#id_rh')
            ), "menu not found"
        )
        print('clicking menu')
        drawer.click()

    def look_for_completion(self):
        self.open_drawer()

        print('looking for completed searches')
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, 'bepfm')
            ), "Frame not found"
        )

        points = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[aria-label^="PC search:"]')
            ), "score not found"
        )
        score = str(points.get_attribute('aria-label'))
        print(score)
        div = score.split('/')
        current = ''.join([i for i in div[0].split() if i.isdigit()])
        total = ''.join([i for i in div[1].split() if i.isdigit()])
        self.complete = int(current) == int(total)
        self.count = int(total) // 5

        util.wait(2)
        self.driver.switch_to.default_content()
        util.wait(2)

        self.open_drawer()

    def fill_input(self):
        self.look_for_completion()
        if self.complete:
            return None

        util.wait_random()
        input_field = self.driver.find_element_by_css_selector('#sb_form_q')
        input_field.clear()
        input_field.send_keys(util.random_letter())

        util.wait_random()
        search = self.driver.find_element_by_css_selector('#search_icon')
        search.click()

    def search(self):
        if self.complete:
            return None

        util.wait_random()

        for _ in range(self.count):
            util.wait_random()
            input_field = self.driver.find_element_by_css_selector('#sb_form_q')
            input_field.send_keys(util.random_letter())
            search = self.driver.find_element_by_css_selector('#sb_form_go')
            search.click()
