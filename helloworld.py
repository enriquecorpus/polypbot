import slack
import slackhelper
import polypbot
import schedule
import time
import asyncio


def start_daily_stand_up():
    _slack = slackhelper.SlackHelper()
    _slack.send_notification_to_users(message=polypbot.Constants.GREETINGS,
                                      blocks=polypbot.Constants.GREETINGS_BLOCK)
    #schedule.cancel_job(start_daily_stand_up)
    _slack.run_rtm()
    print('im alive')


# schedule.every().day.at("08:33").do(start_daily_stand_up)
schedule.every(10).seconds.do(start_daily_stand_up)
while True:
    schedule.run_pending()
    time.sleep(1)
