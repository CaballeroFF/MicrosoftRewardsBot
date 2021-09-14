import rewardsbot.util as util

from selenium.webdriver.remote.webdriver import WebDriver


class SignIn:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def sign_in(self):
        util.wait(5)
        sign_in_button = self.driver.find_element_by_id('id_l')
        sign_in_button.click()

    def enter_email(self, email):
        util.wait_random()
        email_input = self.driver.find_element_by_css_selector('#i0116')
        email_input.clear()
        email_input.send_keys(email)

        util.wait_random()
        submit_button = self.driver.find_element_by_css_selector('#idSIButton9')
        submit_button.click()

    def enter_password(self, password):
        util.wait_random()
        password_input = self.driver.find_element_by_css_selector('#i0118')
        password_input.clear()
        password_input.send_keys(password)

        util.wait_random()
        submit_button = self.driver.find_element_by_css_selector('#idSIButton9')
        submit_button.click()

    def stay_signed_in(self, arg):
        util.wait_random()
        try:
            button = self.driver.find_element_by_css_selector(f'input[value="{arg.title()}"]')
            button.click()
        except:
            print('no stay signed in dialog available.')
