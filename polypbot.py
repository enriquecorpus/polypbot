class Constants:
    GREETINGS = "Kamusta <@{user}>! It's time for our stand up meeting {dept} Standup. " \
                "When you are ready please answer the following question: \n\n*{first_standup_question}*"

    GREETINGS_BLOCK = [{"type": "section", "text": {"type": "mrkdwn",
                                                    "text": "YOUR_MESSAGE_WILL_APPAER_HERE"}},
                       {"type": "divider"}, {"type": "actions", "elements": [
            {"type": "button", "text": {"type": "plain_text", "text": ":neutral_face:", "emoji": True}, "value": "meh"},
            {"type": "button", "text": {"type": "plain_text", "text": ":slightly_smiling_face:", "emoji": True},
             "value": "slightly_smiling"},
            {"type": "button", "text": {"type": "plain_text", "text": ":smiley:", "emoji": True}, "value": "smiley"}]}]

    STAND_UP_QUESTIONS = {1: 'How are you feeling today?',
                          2: 'What did you do since yesterday?',
                          3: 'What will you do today?',
                          4: 'Anything blocking your progress?',
                          5: 'Anything you want to share?'}


class Standup:
    def __init__(self, account_id, account_name, photo_url):
        self.account_id = account_id
        self.account_name = account_name
        self.photo_url = photo_url
        self.stand_up_answers = []
        self.submitted = False

    def add_user_answer(self, phrase: str):
        if not self.user_answered_all_questions and phrase:
            self.stand_up_answers.append(phrase)
        return

    @property
    def user_answered_all_questions(self):
        return len(self.stand_up_answers) >= len(Constants.STAND_UP_QUESTIONS)

    @property
    def get_next_stand_up_question(self) -> str:
        return str(Constants.STAND_UP_QUESTIONS[len(self.stand_up_answers) + 1])

    @property
    def result(self):
        res = ''
        stand_up_q = Constants.STAND_UP_QUESTIONS
        for v in stand_up_q:
            res += '*{Question}*\n>{Answer}\n\n'.format(Question=str(stand_up_q[v]),
                                                        Answer=str(self.stand_up_answers[v - 1]))
        return res
