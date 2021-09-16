import rewardsbot.util as util
import random
import rewardsbot.constants as const

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class QuizSolver:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def start_quiz(self):
        try:
            quiz_button = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#rqStartQuiz')
                ), "can't get quiz"
            )
            quiz_button.click()
        except Exception as e:
            print('could not open quiz', e)

    def close_quiz(self):
        try:
            close = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.element_to_be_clickable(
                    (By.ID, 'rqCloseBtn')
                ),"can't get close button"
            )
            close.click()
        except Exception as e:
            print('could not close quiz', e)

    def generic_quiz(self):
        self.start_quiz()

        WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.ID, 'rqHeaderCredits')
            ),"can't get questions"
        )
        question_count = self.driver.find_elements_by_css_selector('#rqHeaderCredits span.emptyCircle')

        for _ in range(len(question_count) + 1):
            util.wait(1.5)
            print('starting question')
            WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.visibility_of_element_located(
                    (By.ID, 'currentQuestionContainer')
                ), "can't get answers"
            )
            util.wait_random()
            answers = self.driver.find_elements_by_class_name('rq_button')
            print('clicking answer')
            random.choice(answers).click()
            util.wait_random()

            WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.invisibility_of_element_located(
                    (By.ID, 'rqAnsStatus')
                ), "hint not found"
            )
            print('hint hidden')

    def this_or_that(self):
        self.start_quiz()

        questions_element = WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="currentQuestionContainer"]/div/div/div[2]/div[4]')
            )
        )
        question_count = questions_element.get_attribute('textContent')

        for _ in range(10):
            print('starting question')

            util.wait(2)
            WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'btOptionCard')
                )
            )
            print('answers located')
            util.wait_random()
            answers = self.driver.find_elements_by_class_name('btOptionCard')
            print('picking answer from', len(answers))
            util.wait_random()
            index = random.randint(0, 1)
            answers[index].click()
            util.wait_random()

            questions_element = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="currentQuestionContainer"]/div/div/div[2]/div[4]')
                )
            )
            while question_count == questions_element.get_attribute('textContent'):
                print('loading...')
                util.wait(1)
                questions_element = WebDriverWait(self.driver, const.WAIT_TIME).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="currentQuestionContainer"]/div/div/div[2]/div[4]')
                    )
                )
            question_count = questions_element.get_attribute('textContent')

    def supersonic_quiz(self):
        self.start_quiz()

        WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.ID, 'rqHeaderCredits')
            ),"can't get questions"
        )
        question_count = self.driver.find_elements_by_css_selector('#rqHeaderCredits span.emptyCircle')

        for _ in range(len(question_count) + 1):
            util.wait(4)
            print('starting question')
            ss_score = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#currentQuestionContainer > div > div.rqQuestion > span > span')
                )
            )
            score = str(ss_score.get_attribute('textContent'))
            print(score)
            div = score.split('/')
            current = ''.join([i for i in div[0].split() if i.isdigit()])
            total = ''.join([i for i in div[1].split() if i.isdigit()])
            util.wait_random()
            answers = self.driver.find_elements_by_css_selector('#slideexp1_7ECCF2 > div > div.slide')
            index = 0

            while int(current) != int(total):
                answers[index].click()
                index += 1

                ss_score = WebDriverWait(self.driver, const.WAIT_TIME).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, '#currentQuestionContainer > div > div.rqQuestion > span > span')
                    )
                )
                score = str(ss_score.get_attribute('textContent'))
                print(score)
                div = score.split('/')
                current = ''.join([i for i in div[0].split() if i.isdigit()])
                total = ''.join([i for i in div[1].split() if i.isdigit()])
                util.wait_random()
                answers = self.driver.find_elements_by_css_selector('#slideexp1_7ECCF2 > div > div.slide')

    def lightspeed_quiz(self):
        self.generic_quiz()

    def who_said_it(self):
        self.generic_quiz()

    def word_for_word(self):
        self.start_quiz()

        index = 0
        condition = True
        while condition:
            answers = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'rq_button')
                )
            )

            util.wait_random()
            answers[index].click()
            index += 1
            util.wait(2)

            hint = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.presence_of_element_located(
                    (By.ID, 'rqAnsStatus')
                )
            )
            print(hint.is_displayed(), hint.get_attribute('textContent'))
            condition = hint.is_displayed() and ('Oops, try again!' == hint.get_attribute('textContent').strip())
