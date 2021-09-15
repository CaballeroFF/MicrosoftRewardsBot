#!.\venv\Scripts\python.exe
import accounts as a

from rewardsbot.rewardsbot import RewardsBot


def main():
    for account in a.accounts:
        with RewardsBot(r"C:/SeleniumDrivers/chromedriver.exe") as bot:
            bot.landing_page()
            bot.sign_in(account)
            bot.do_daily_search()


if __name__ == '__main__':
    main()
