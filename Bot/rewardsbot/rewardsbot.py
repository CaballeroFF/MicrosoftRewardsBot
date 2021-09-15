import rewardsbot.constants as const

from selenium import webdriver
from rewardsbot.signin import SignIn
from rewardsbot.dailysearch import DailySearch


class RewardsBot(webdriver.Chrome):
    def __init__(self, driver_path, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        super(RewardsBot, self).__init__(executable_path=self.driver_path, options=chrome_options)
        self.implicitly_wait(20)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def landing_page(self):
        self.get(const.BASE_URL)

    def sign_in(self, account):
        bot_sign_in = SignIn(self)
        bot_sign_in.sign_in()
        bot_sign_in.enter_email(account[0])
        bot_sign_in.enter_password(account[1])
        bot_sign_in.stay_signed_in('no')

    def do_daily_search(self):
        bot_daily_search = DailySearch(self)
        bot_daily_search.fill_input()
        bot_daily_search.search()