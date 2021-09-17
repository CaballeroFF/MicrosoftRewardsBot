#!.\venv\Scripts\python.exe
import accounts as a

from rewardsbot.rewardsbot import RewardsBot


def main():
    for account in a.accounts:
        with RewardsBot(r"C:/SeleniumDrivers/chromedriver.exe", teardown=False) as bot:
            bot.landing_page()
            bot.sign_in(account)
            # bot.do_daily_search()
            bot.do_daily_set()


if __name__ == '__main__':
    main()
