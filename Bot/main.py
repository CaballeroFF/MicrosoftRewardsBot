#!.\venv\Scripts\python.exe
from rewardsbot.rewardsbot import RewardsBot


def main():
    with RewardsBot(r"C:/SeleniumDrivers/chromedriver.exe") as bot:
        bot.landing_page()
        bot.sign_in(["email", "password"])


if __name__ == '__main__':
    main()
