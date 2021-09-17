import rewardsbot.constants as const

from selenium import webdriver
from rewardsbot.signin import SignIn
from rewardsbot.dailysearch import DailySearch
from rewardsbot.dailyset import DailySet


class RewardsBot(webdriver.Chrome):
    def __init__(self, driver_path, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        super(RewardsBot, self).__init__(executable_path=self.driver_path, options=chrome_options)
        self.implicitly_wait(7)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def landing_page(self):
        self.get(const.BASE_URL)

    def test(self):
        self.get('https://www.bing.com/search?q=nora%20ephron%20movies&rnoreward=1&mkt=EN-US&FORM=ML12JG&skipopalnative=true&rqpiodemo=1&filters=BTEPOKey:%22REWARDSQUIZ_ENUS_MicrosoftRewardsQuizCB_20210914%22%20BTROID:%22Gamification_DailySet_20210914_Child2%22%20BTROEC:%220%22%20BTROMC:%2230%22')

    def sign_in(self, account):
        print('Signing in...')
        bot_sign_in = SignIn(self)
        bot_sign_in.sign_in()
        bot_sign_in.enter_email(account[0])
        bot_sign_in.enter_password(account[1])
        bot_sign_in.stay_signed_in('no')
        print('Signed in.')

    def do_daily_search(self):
        print('Searching...')
        bot_daily_search = DailySearch(self)
        bot_daily_search.fill_input()
        bot_daily_search.search()
        print('search done.')

    def do_daily_set(self):
        print('Attempting Daily set...')
        bot_daily_set = DailySet(self)
        # bot_daily_set.daily_article()
        # bot_daily_set.daily_quiz()
        # bot_daily_set.daily_trivia()
        bot_daily_set.test()
        print('Daily set complete.')