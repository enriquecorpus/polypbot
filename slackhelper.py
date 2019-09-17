import slack
import daily
import constants


class SlackHelper:

    def __init__(self):
        self.slack_token = 'xoxb-761143478773-760710426068-TBDVs3VQgt3PUMmDtZmYvjfj'  # bot_token
        self.client = slack.WebClient(token=self.slack_token)
        self.rtm_client = slack.RTMClient(token=self.slack_token)
        self.users = {}

    def start_rtm(self):
        self.rtm_client.start()

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

    def send_notification_to_users(self, message, blocks):
        constants.CHECK_INS = {}
        users_list = self.client.users_list().get('members', None)
        if users_list:
            for u in users_list:
                print(u)
                try:
                    user_id = u['id']
                    if user_id and user_id not in constants.CHECK_INS and not u['deleted'] and not u['is_bot']:
                        message_ = message.format(user=user_id, dept='IT DEPT')
                        blocks[0]['text']['text'] = message_
                        # print('{blocks}'.format(blocks=blocks))
                        if self.post_message_with_block_template(uid=user_id,
                                                                 blocks=blocks):
                            constants.CHECK_INS[user_id] = daily.Standup(account_id=user_id,
                                                                         account_name=u.get('profile').get('real_name',
                                                                                                           'polypbot'),
                                                                         photo_url=u.get('profile').get('image_48',
                                                                                                        ''))
                except KeyError:
                    pass

    #   TODO MAKE IT ASYNC? LOOKS LIKE ITS A BLOCKING PROCESS
    @slack.RTMClient.run_on(event='message')
    def parse_slack_message(**payload):
        data = payload['data']
        web_client = payload['web_client']
        rtm_client = payload['rtm_client']
        user_id = data['user']
        if user_id in constants.CHECK_INS:
            user_check_in = constants.CHECK_INS[user_id]
            user_check_in.add_user_answer(data.get('text'))
            if user_check_in.user_answered_all_questions and not user_check_in.is_done:
                print('{user_id}, is_done={done},answered all = {ans} \n {res}'.format(user_id=user_id,
                                                                                       done=user_check_in.is_done,
                                                                                       ans=user_check_in.user_answered_all_questions,
                                                                                       res=user_check_in.result))
                # self.post_message(channel='#random', message='tapos na si <@{user}>!'.format(user=user_id))
                web_client.chat_postMessage(
                    channel='#random',
                    text='<@{user}> posted an update for *IT Daily Standup*. \n\n {txt}'.format(user=user_id,
                                                                                                txt=user_check_in.result),
                    username=user_check_in.account_name,
                    icon_url=user_check_in.photo_url
                )
                user_check_in.is_done = True
            elif not user_check_in.user_answered_all_questions:
                # self.post_message(channel='#???????', message=user.get_next_stand_up_question)
                web_client.chat_postMessage(
                    channel=user_id,
                    text=user_check_in.get_next_stand_up_question,
                    as_user=True,
                )
