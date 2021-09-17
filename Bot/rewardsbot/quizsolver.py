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

        self.close_quiz()

    def test_your_smarts(self):
        print("attempting 'test your smarts'")

        answers = self.test_your_smarts_grab_answers()
        answer_count = len(answers)

        question_count = WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div[class*="FooterText"]')
            ), "could not get question count"
        )
        print(question_count.get_attribute('textContent'))
        div = str(question_count.get_attribute('textContent')).split('of')
        current = ''.join([i for i in div[0] if i.isdigit()])
        total = ''.join([i for i in div[1] if i.isdigit()])
        count = int(total) - int(current) + 1
        print(current, total, count)
        print("questions counted")

        for _ in range(count):
            print("preparing answer")
            answers = self.test_your_smarts_grab_answers()
            index = random.randint(0, answer_count-1)
            answers[index].click()
            print(len(answers), "answers")
            util.wait_random()

            submit_button = WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[value="Next question"]')
                ), "can't find submit button"
            )
            submit_button.click()
            util.wait_random()

    def test_your_smarts_grab_answers(self):
        question_panel = WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.ID, 'ListOfQuestionAndAnswerPanes')
            ), "could not find question panel"
        )
        answers = question_panel.find_elements_by_css_selector('div[id*="QuestionPane"] > div.b_vPanel.b_loose > div:nth-child(2) > a')
        return answers

    def this_or_that(self):
        print("attempting 'this or that'")
        self.start_quiz()

        questions_element = WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="currentQuestionContainer"]/div/div/div[2]/div[4]')
            )
        )
        question_count = questions_element.get_attribute('textContent')
        count = 10 - int(question_count.split('of')[0].strip()) + 1
        print(count, "questions to do")

        for _ in range(count):
            print('starting question')

            util.wait(1)
            WebDriverWait(self.driver, const.WAIT_TIME).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'btOptionCard')
                )
            )
            print('answers located')
            answers = self.driver.find_elements_by_class_name('btOptionCard')
            print('picking answer from', len(answers))
            index = random.randint(0, 1)
            answers[index].click()
            util.wait_random()

            try:
                WebDriverWait(self.driver, const.WAIT_TIME).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="currentQuestionContainer"]/div/div/div[2]/div[4]')
                    )
                )
            except Exception as e:
                print("quiz finished before getting elements")

        self.close_quiz()

    def supersonic_quiz(self):
        print("attempting 'supersonic'")
        self.start_quiz()

        print('starting quiz')
        WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.ID, 'rqHeaderCredits')
            ),"can't get questions"
        )

        question_count = self.driver.find_elements_by_css_selector('#rqHeaderCredits span.emptyCircle')
        print('questions counted', (len(question_count) + 1))
        answers = self.driver.find_elements_by_css_selector('div[id^="slideex"] > div > div.slide')
        count = len(answers)
        print(count, 'possible answers')

        for _ in range(len(question_count) + 1):
            util.wait(1.5)
            print('starting question')

            answers, current, total = self.supersonic_quiz_grab_elements()
            index = 0
            correct = 0

            try:
                while index < count and correct != int(total):
                    print("clicking answer", index)
                    answers[index].click()
                    util.wait_random()

                    answers, current, total = self.supersonic_quiz_grab_elements()
                    answer = answers[index].find_element_by_tag_name('div')
                    print('correct?', answer.get_attribute('iscorrectoption'))
                    if answer.get_attribute('iscorrectoption') == "True":
                        correct += 1
                    print("correct answers", correct)
                    index += 1
            except Exception as e:
                print("quiz finished before getting elements")
            print("question done....")

        self.close_quiz()

    def supersonic_quiz_grab_elements(self):
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
        answers = self.driver.find_elements_by_css_selector('div[id^="slideex"] > div > div.slide')
        print('getting answers', len(answers))
        return answers, current, total

    def lightspeed_quiz(self):
        print("attempting 'lightspeed'")
        self.generic_quiz()

    def who_said_it(self):
        self.generic_quiz()

    def word_for_word(self):
        print("attempting 'word for word'")
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

        self.close_quiz()

    def daily_poll(self):
        print("attempting 'Daily poll'")

        poll = WebDriverWait(self.driver, const.WAIT_TIME).until(
            EC.visibility_of_element_located(
                (By.ID, 'btPollOverlay')
            ), "could not find poll"
        )
        print("poll ready")

        options = WebDriverWait(poll, const.WAIT_TIME).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'div > div.btOptions2.bt_pollOptions > div')
            ), "could not find options"
        )
        print(len(options), "options")
        random.choice(options).click()
        util.wait_random()
        self.close_quiz()
