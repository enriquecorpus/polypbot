import slack
import slackhelper
import slackbot
import schedule
import time


def start_daily_stand_up():
    _slack = slackhelper.SlackHelper()
    _slack.send_notification_to_users(message=slackbot.PolypBot.GREETINGS,
                                      blocks=slackbot.PolypBot.GREETINGS_BLOCK)
    # schedule.cancel_job(start_daily_stand_up)
    _slack.start_rtm()


# schedule.every().day.at("08:33").do(start_daily_stand_up)
schedule.every(5).seconds.do(start_daily_stand_up)
while True:
    schedule.run_pending()
    time.sleep(1)
