import slack
import polypbot
import constants
import asyncio
import concurrent.futures
import schedule
import time
import secret
import services


class SlackHelper:

    def __init__(self):
        self.slack_token = secret.SLACK_BOT_ACCESS_TOKEN
        self.client = slack.WebClient(token=self.slack_token)
        self.loop = None
        self.executor = None
        self.rtm_client = None
        self.check_ins = {}

        # self.rtm_client.stop()

    def run(self):
        self.send_notification_to_users()
        asyncio.run(self.start_rtm())

    def schedule_checker(self):
        # schedule.every().day.at("08:33").do(self.send_notification_to_users)
        schedule.every(120).seconds.do(self.send_notification_to_users)
        while True:
            schedule.run_pending()
            time.sleep(5)

    async def start_rtm(self):
        self.loop = asyncio.get_event_loop()
        self.rtm_client = slack.RTMClient(token=self.slack_token, run_async=True, loop=self.loop)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        await asyncio.gather(self.loop.run_in_executor(self.executor, self.schedule_checker), self.rtm_client.start())

    def post_message_with_block_template(self, blocks, uid: str) -> bool:
        response = self.client.chat_postMessage(
            channel=uid,
            blocks=blocks,
            as_user=True)
        if response["ok"]:
            # print('success {uid} {blocks}'.format(uid=uid,blocks=blocks))
            return True

    def post_message(self, message, channel: str) -> bool:
        response = self.client.chat_postMessage(
            channel=channel,
            text=message,
            as_user=True)
        if response["ok"]:
            return True

    def send_notification_to_users(self):
        constants.CHECK_INS = {}
        message = polypbot.Constants.GREETINGS
        blocks = polypbot.Constants.GREETINGS_BLOCK
        users_list = self.client.users_list().get('members', None)
        if users_list:
            for u in users_list:
                try:
                    user_id = u['id']
                    if user_id and user_id not in constants.CHECK_INS and not u['deleted'] and not u['is_bot']:
                        message_ = message.format(user=user_id, dept='IT DEPT',
                                                  first_standup_question=polypbot.Constants.STAND_UP_QUESTIONS[1])
                        blocks[0]['text']['text'] = message_
                        # print('{blocks}'.format(blocks=blocks))
                        if self.post_message_with_block_template(uid=user_id,
                                                                 blocks=blocks):
                            constants.CHECK_INS[user_id] = polypbot.Standup(account_id=user_id,
                                                                            account_name=u.get('profile').get(
                                                                                'real_name',
                                                                                'polypbot'),
                                                                            photo_url=u.get('profile').get('image_48',
                                                                                                           ''))
                except KeyError:
                    pass

    @slack.RTMClient.run_on(event='message')
    async def parse_slack_message(**payload):
        message = ''
        channel = ''
        username = ''
        icon_url = ''
        as_user = False
        data = payload['data']
        web_client = payload['web_client']
        rtm_client = payload['rtm_client']
        user_id = data.get('user','')
        if user_id in constants.CHECK_INS:
            user_check_in = constants.CHECK_INS[user_id]
            user_check_in.add_user_answer(data.get('text'))
            if user_check_in.user_answered_all_questions and not user_check_in.submitted:
                message = '<@{user}> posted an update for *IT Daily Standup*. \n\n {result}'.format(
                    user=user_id, result=user_check_in.result)
                channel = '#random'
                username = user_check_in.account_name
                icon_url = user_check_in.photo_url
                user_check_in.submitted = True
                # EWW This code is ugly...
                random_facts = services.random_facts()
                print(random_facts)
                if random_facts:
                    faq_ = 'Thank you for submitting your daily stand up. \n _Here''s a tiny fact that' \
                           ' im going to share with you._\n*Did you know?* \n\n*_{faq}_*\n`source: `{source}'.format(
                            faq=random_facts['text'],
                            source=random_facts['source'])
                    web_client.chat_postMessage(channel=user_id, text=faq_, as_user=True)
            elif not user_check_in.user_answered_all_questions:
                message = '*{}*'.format(user_check_in.get_next_stand_up_question)
                channel = user_id
                as_user = True
            try:
                web_client.chat_postMessage(channel=channel, text=message, as_user=as_user, username=username,
                                            icon_url=icon_url)
            except():
                raise Exception("Unknown Err")
