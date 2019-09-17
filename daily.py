import slackbot


class Standup:
    def __init__(self, account_id, account_name, photo_url):
        self.account_id = account_id
        self.account_name = account_name
        self.photo_url = photo_url
        self.stand_up_answers = []
        self.is_done = False

    def add_user_answer(self, phrase: str):
        if not self.user_answered_all_questions and phrase:
            self.stand_up_answers.append(phrase)
        return

    @property
    def user_answered_all_questions(self):
        return len(self.stand_up_answers) >= len(slackbot.PolypBot.STAND_UP_QUESTIONS)

    @property
    def get_next_stand_up_question(self) -> str:
        return str(slackbot.PolypBot.STAND_UP_QUESTIONS[len(self.stand_up_answers) + 1])

    @property
    def result(self):
        res = ''
        stand_up_q = slackbot.PolypBot.STAND_UP_QUESTIONS
        for v in stand_up_q:
            res += '*{Question}*\n>{Answer}\n\n'.format(Question=str(stand_up_q[v]),
                                                        Answer=str(self.stand_up_answers[v - 1]))
        return res
