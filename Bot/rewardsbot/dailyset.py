import rewardsbot.util as util
import random

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DailySet:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.complete = False

    def open_drawer(self):
        util.wait(3)

        drawer = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#id_rh')
            )
        )
        print('clicking menu')
        drawer.click()

    def open_nth_promo(self, n):
        self.open_drawer()

        print('attempting to grab element')
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, 'bepfm')
            )
        )

        try:
            article = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'.mfo_c_ds > .promo_cont:nth-child({n})')
                )
            )
            article.click()
        except Exception as e:
            self.complete = True
            print('daily set complete', e)

        util.wait(2)
        self.driver.switch_to.default_content()
        util.wait(2)

    def start_quiz(self):
        try:
            quiz_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#rqStartQuiz')
                ), "can't get quiz"
            )
            quiz_button.click()
        except Exception as e:
            print('could not open quiz', e)

    def close_quiz(self):
        try:
            close = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'rqCloseBtn')), "can't get close button")
            close.click()
        except Exception as e:
            print('could not close quiz', e)

    def generic_quiz(self):
        self.start_quiz()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'rqHeaderCredits')), "can't get questions")
        question_count = self.driver.find_elements_by_css_selector('#rqHeaderCredits span.emptyCircle')

        for _ in range(len(question_count)+1):
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.ID, 'rqAnsStatus')
                ), "hint not found"
            )
            print('hint hidden')

            util.wait(1.5)
            print('starting question')
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.ID, 'currentQuestionContainer')
                ), "can't get answers"
            )
            util.wait_random()
            answers = self.driver.find_elements_by_class_name('rq_button')
            print('clicking answer')
            random.choice(answers).click()
            util.wait_random()

    def daily_article(self):
        self.open_nth_promo(1)

    def daily_quiz(self):
        if self.complete:
            return None

        self.open_nth_promo(2)
        try:
            self.lightspeed_quiz()
        except Exception as e:
            print('could not complete quiz', e)

        self.close_quiz()

    def lightspeed_quiz(self):
        self.generic_quiz()

    def daily_trivia(self):
        if self.complete:
            return None

        self.open_nth_promo(3)
        try:
            self.who_said_it()
        except Exception as e:
            print('could not complete trivia', e)

        self.close_quiz()

    def who_said_it(self):
        self.generic_quiz()