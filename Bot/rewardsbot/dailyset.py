import rewardsbot.util as util
import rewardsbot.constants as const

from rewardsbot.quizsolver import QuizSolver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DailySet:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.quiz_solver = QuizSolver(self.driver)
        self.complete = False

    def open_drawer(self):
        util.wait(3)

        drawer = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#id_rh')
            )
        )
        print('clicking menu')
        drawer.click()

    def open_nth_promo(self, n):
        self.open_drawer()

        print('attempting to grab element')
        WebDriverWait(self.driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, 'bepfm')
            )
        )

        try:
            article = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'.mfo_c_ds > .promo_cont:nth-child({n})')
                )
            )
            title_element = article.find_element_by_css_selector('p.promo-title')
            title = title_element.get_attribute('textContent')
            print(title)
            article.click()
        except Exception as e:
            title = None
            self.complete = True
            print('daily set complete', e)

        util.wait(2)
        print("switching to default frame")
        self.driver.switch_to.default_content()
        util.wait(2)
        return title

    def quiz_type(self, title):
        if title == "This or That?":
            self.quiz_solver.this_or_that()
        elif title == "Supersonic quiz":
            self.quiz_solver.supersonic_quiz()
        elif title == "Lightspeed quiz":
            self.quiz_solver.lightspeed_quiz()
        else:
            # title == "Test your smarts" "Show what you know"
            self.quiz_solver.test_your_smarts()

    def trivia_type(self, title):
        if title == "Who said it":
            print("who said it")
        elif title == "Word for word":
            self.quiz_solver.word_for_word()
        elif title == "Daily poll":
            self.quiz_solver.daily_poll()

    def daily_article(self):
        self.open_nth_promo(1)

    def daily_quiz(self):
        if self.complete:
            return None

        title = self.open_nth_promo(2)

        try:
            self.quiz_type(title)
        except Exception as e:
            print('could not complete quiz', e)

    def daily_trivia(self):
        if self.complete:
            return None

        title = self.open_nth_promo(3)

        try:
            self.trivia_type(title)
        except Exception as e:
            print('could not complete trivia', e)

    def check_for_completion(self):
        if not self.complete:
            self.open_drawer()

        try:
            print('attempting to grab element')
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.ID, 'bepfm')
                )
            )
            WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="modern-flyout"]/div/div[3]/div[2]/div[1]/div[2]/div/div/div[2]')
                ), "could not find complete hint"
            )
            days_to_go = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="modern-flyout"]/div/div[3]/div[2]/div[1]/div[2]/div/div/p')
                ), "could not complete text"
            )
            print(days_to_go.get_attribute('textContent'))
            util.wait(2)
            print("switching to default frame")
            self.driver.switch_to.default_content()
        except Exception as e:
            print("daily set failed", e)

    def test(self):
        self.driver.get('https://www.bing.com/search?q=chicago&rnoreward=1&mkt=EN-US&FORM=ML12JG&skipopalnative=true&rqpiodemo=1&filters=BTEPOKey:%22REWARDSQUIZ_ENUS_MicrosoftRewardsQuizDS_PartPoints_20210915%22%20BTROID:%22Gamification_DailySet_20210915_Child2%22%20BTROEC:%220%22%20BTROMC:%2240%22%20BTROQN:%220%22')
        util.wait(3)
        self.quiz_solver.lightspeed_quiz()
